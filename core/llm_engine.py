import requests
import re
import pandas as pd

SCHEMAS = {
    'department_store': '''
CREATE TABLE Customers (customer_id INTEGER PRIMARY KEY, payment_method_code TEXT);
CREATE TABLE Customer_Orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
CREATE TABLE Suppliers (supplier_id INTEGER PRIMARY KEY, supplier_name TEXT);
CREATE TABLE Product_Suppliers (product_id INTEGER PRIMARY KEY, product_name TEXT, supplier_id INTEGER, total_amount_purchased INTEGER);
''',
    'hr_management': '''
CREATE TABLE Departments (Department_ID INTEGER PRIMARY KEY, Department_Name TEXT);
CREATE TABLE Employees (Employee_ID INTEGER PRIMARY KEY, Department_ID INTEGER, Salary INTEGER);
''',
    'financial_logs': '''
CREATE TABLE Financial_Logs (Log_ID INTEGER PRIMARY KEY, Log_Month TEXT, Log_Year INTEGER, Revenue_Amount INTEGER);
'''
}

def generate_sql(prompt: str, db_name: str, model_name: str, few_shot_examples: list = None, temperature: float = 0.0) -> str:
    """
    Sends the prompt and DB schema to the local Ollama instance and returns the generated SQL.
    If few_shot_examples is provided, they are injected into the system prompt.
    """
    base_name = db_name.split(' ')[0]
    schema = SCHEMAS.get(base_name, "")
    
    few_shot_text = ""
    if few_shot_examples:
        few_shot_text = "\nHere are some examples of valid SQL queries for this database:\n\n"
        for i, example in enumerate(few_shot_examples, 1):
            few_shot_text += f"Example {i}:\nQuestion: {example['question']}\nSQL:\n```sql\n{example['sql']}\n```\n\n"
    
    system_prompt = f"""You are an expert SQL data analyst.
Given the following database schema:
{schema}
{few_shot_text}
Write a valid SQLite SQL query to answer the user's question.

CRITICAL RULES FOR EXACT MATCH EVALUATION:
1. Output ONLY the minimum required columns to answer the question. DO NOT select extra columns.
2. DO NOT use the AS keyword to alias columns or tables unless absolutely necessary (e.g. for self-joins).
3. Do not include any explanations. Output ONLY the SQL code inside a markdown code block (```sql ... ```).
"""
    
    # Clean up model name from UI strings like "qwen2.5-coder:7b (Alibaba)"
    clean_model_name = model_name.split(' ')[0]
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": clean_model_name,
        "prompt": f"Question: {prompt}\nSQL Query:",
        "system": system_prompt,
        "stream": False,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        generated_text = data.get('response', '')
        
        # Extract SQL from markdown blocks (ignores the CoT text before it)
        match = re.search(r'```(?:sql)?(.*?)```', generated_text, re.DOTALL | re.IGNORECASE)
        if match:
            sql = match.group(1).strip()
        else:
            # Fallback if no code blocks are present
            sql = generated_text.strip()
            
        return sql
    except requests.exceptions.ConnectionError:
        return "-- [Error] Could not connect to Ollama. Please ensure 'ollama serve' is running."
    except Exception as e:
        return f"-- [Error] Validation request failed: {str(e)}"

def generate_data_analysis(prompt: str, sql_query: str, df: pd.DataFrame, model_name: str, language: str = "한국어"):
    """
    Takes the SQL query and the resulting DataFrame, and generates a natural language explanation.
    Streams the response back.
    """
    clean_model_name = model_name.split(' ')[0]
    
    df_str = df.head(10).to_markdown()
    if len(df) > 10:
        df_str += f"\n... (and {len(df) - 10} more rows)"
        
    lang_instruction = "You MUST answer the user's question entirely in KOREAN." if language == "한국어" else "You MUST answer the user's question entirely in ENGLISH."
        
    bot_name = "'제대리'" if language == "한국어" else "'Jay'"
    system_prompt = f"""You are {bot_name}, a professional data analyst. 
Your job is to answer the user's question by interpreting the provided data table.
CRITICAL RULES:
1. NEVER mention robotic phrases like "쿼리 실행 결과에서", "데이터에 따르면". Just state the facts directly.
2. DO NOT hallucinate fake units (like 원, 명, 달러) if they are not in the data.
3. Keep your response extremely concise (1-2 sentences maximum).
4. DO NOT use markdown tables UNLESS the user explicitly asks for a table format (e.g., "표로 달라고 하면", "테이블로 줘"). If requested, output a clean markdown table. Otherwise, output only plain natural text.
{lang_instruction}"""
    
    user_prompt = f"Question: {prompt}\n\nSQL Query Executed: {sql_query}\n\nData Result:\n{df_str}\n\nPlease explain this data to me."
    
    import json
    url = "http://localhost:11434/api/generate"
    try:
        res = requests.post(url, json={"model": clean_model_name, "prompt": user_prompt, "system": system_prompt, "stream": True}, stream=True, timeout=60)
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line)
                if 'response' in chunk:
                    yield chunk['response']
    except Exception as e:
        yield f"데이터 분석 중 오류가 발생했습니다: {str(e)}"

def generate_app_response(prompt: str, db_name: str, model_name: str, language: str = "한국어") -> tuple[str, str]:
    """
    Used by app.py. Returns a tuple (response_type, content).
    response_type is either 'CHAT' or 'SQL'.
    """
    clean_model_name = model_name.split(' ')[0]
    
    # 1. Classify Intent
    base_name = db_name.split(' ')[0]
    classifier_system = f"""You are an intent classifier. The user is looking at a local database named '{base_name}'.
Respond with EXACTLY ONE WORD: 'SQL' or 'CHAT'. DO NOT output any other words.

Rules:
1. Output 'SQL' if the user is asking a natural language question to get data, metrics, counts, or records from the database (e.g., "'PayPal'로 결제된 주문은 몇 건인가요?", "총 매출은 얼마야?"). Also output 'SQL' if the user provides an explicit SQL query.
2. Output 'SQL' if the user asks for data and requests it in a specific format like a "table", "표", "markdown", etc.
3. Output 'CHAT' for EVERYTHING ELSE, including:
   - General knowledge, external companies, or stock prices (e.g., '하이닉스 주가', '애플 주가')
   - Casual greetings or vulgar slang (e.g., '안녕', '똥 마려워', '쓰읍')
   - Emotions or complaints (e.g., '짜증나네', '너 바보야?')
   - Career or coding advice

Examples:
User: "Find the employee ID and salary of all employees working in the 'Engineering' department. Please format the answer as a table." -> SQL
User: "What are the top 2 most popular payment methods, and how many times were they used? I want the result as a markdown table." -> SQL
User: "'PayPal'로 결제된 주문은 몇 건인가요?" -> SQL
User: "부서별 평균 급여 알려줘" -> SQL
User: "오늘 날씨 어때?" -> CHAT
User: "똥 마려워" -> CHAT
User: "하이닉스 주가가 얼마나 올라가나" -> CHAT"""
    url = "http://localhost:11434/api/generate"
    try:
        res = requests.post(url, json={"model": clean_model_name, "prompt": prompt, "system": classifier_system, "stream": False}, timeout=60)
        intent = res.json().get('response', '').strip().upper()
    except Exception as e:
        intent = 'CHAT'  # Default to chat if classification fails
        
    intent_clean = intent.replace('.', '').replace('"', '').replace("'", '').strip()
    
    # Strict Parsing: Route to SQL only if it strictly matches 'SQL' or starts with it and is extremely short.
    # This prevents long rambling refusals (like "I cannot provide an SQL query") from incorrectly triggering SQL mode.
    if intent_clean == 'SQL' or (intent_clean.startswith('SQL') and len(intent_clean) <= 5):
        return 'SQL', generate_sql(prompt, db_name, model_name)
    else:
        # 2. General Chat
        lang_instruction = "You speak Korean. You MUST reply entirely in KOREAN." if language == "한국어" else "You speak English. You MUST reply entirely in ENGLISH."
        bot_name = "'제대리'" if language == "한국어" else "'Jay'"
        chat_system = f"You are {bot_name}, a friendly and professional AI assistant at a company. Respond naturally to the user in a conversational tone. {lang_instruction} IMPORTANT: Keep your response extremely concise (under 2-3 sentences) to ensure fast response times."
        def chat_stream_generator():
            import json
            try:
                res = requests.post(url, json={"model": clean_model_name, "prompt": prompt, "system": chat_system, "stream": True}, stream=True, timeout=60)
                for line in res.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            yield chunk['response']
            except Exception as e:
                yield f"죄송합니다. 대화 처리 중 오류가 발생했습니다: {str(e)}"
        
        return 'CHAT', chat_stream_generator()

def generate_sql_with_self_correction(prompt: str, db_name: str, model_name: str, previous_sql: str, error_message: str, few_shot_examples: list = None, temperature: float = 0.0) -> str:
    """
    Reflexion Agent Prompt: Feeds the SQLite execution error back to the LLM to self-correct the SQL.
    """
    base_name = db_name.split(' ')[0]
    schema = SCHEMAS.get(base_name, "")
    
    few_shot_text = ""
    if few_shot_examples:
        few_shot_text = "\nHere are some examples of valid SQL queries for this database:\n\n"
        for i, example in enumerate(few_shot_examples, 1):
            few_shot_text += f"Example {i}:\nQuestion: {example['question']}\nSQL:\n```sql\n{example['sql']}\n```\n\n"
            
    system_prompt = f"""You are an expert SQL data analyst.
Given the following database schema:
{schema}
{few_shot_text}
You previously generated this SQL:
```sql
{previous_sql}
```
However, running it resulted in this SQLite Error: {error_message}

Fix the SQL query to resolve the error and answer the user's question correctly.

CRITICAL RULES FOR EXACT MATCH EVALUATION:
1. Output ONLY the minimum required columns to answer the question. DO NOT select extra columns.
2. DO NOT use the AS keyword to alias columns or tables unless absolutely necessary (e.g. for self-joins).
3. Do not include any explanations. Output ONLY the corrected SQL code inside a markdown code block (```sql ... ```).
"""
    clean_model_name = model_name.split(' ')[0]
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": clean_model_name,
        "prompt": f"Question: {prompt}\nCorrected SQL Query:",
        "system": system_prompt,
        "stream": False,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        generated_text = data.get('response', '')
        
        match = re.search(r'```(?:sql)?(.*?)```', generated_text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        else:
            return generated_text.strip()
    except:
        return previous_sql
