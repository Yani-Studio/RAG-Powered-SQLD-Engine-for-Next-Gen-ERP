import json
import itertools
import random

# Synthetic Data Templates for Data Augmentation
templates = {
    'department_store': {
        'KR': [
            "'{supplier}'가 공급하는 제품들의 총 금액을 알려주세요.",
            "결제 수단이 '{payment}'인 고객들은 총 몇 명인가요?",
            "'{product}' 제품을 공급하는 업체의 이름은 무엇인가요?",
            "가장 많이 사용된 결제 수단 상위 2개를 보여주세요.",
            "공급 업체별로 구매한 총 금액을 계산해주세요.",
            "'{supplier}'가 공급하는 모든 제품의 이름을 나열해주세요."
        ],
        'EN': [
            "What is the total amount purchased for products supplied by '{supplier}'?",
            "How many customers used '{payment}' as their payment method?",
            "What is the name of the supplier that provides '{product}'?",
            "Show me the top 2 most popular payment methods.",
            "Calculate the total purchase amount per supplier.",
            "List all product names supplied by '{supplier}'."
        ],
        'entities': {
            'supplier': ['Global Tech', 'Local Farms', 'Quick Electronics', 'Premium Brands'],
            'payment': ['PayPal', 'Credit Card', 'Cash', 'Apple Pay'],
            'product': ['Laptop', 'Apples', 'Smartphone', 'Desk Chair', 'Coffee Maker']
        }
    },
    'hr_management': {
        'KR': [
            "'{dept}' 부서의 평균 연봉은 얼마인가요?",
            "연봉이 {salary}달러 이상인 직원은 몇 명인가요?",
            "가장 연봉이 높은 직원이 속한 부서의 이름은 무엇인가요?",
            "'{dept}' 부서에 속한 모든 직원의 ID를 나열해주세요.",
            "부서별 직원 수를 알려주세요."
        ],
        'EN': [
            "What is the average salary in the '{dept}' department?",
            "How many employees have a salary greater than {salary} dollars?",
            "What is the name of the department with the highest paid employee?",
            "List all employee IDs in the '{dept}' department.",
            "Show me the number of employees per department."
        ],
        'entities': {
            'dept': ['Engineering', 'Sales', 'HR', 'Marketing'],
            'salary': ['50000', '70000', '100000', '120000']
        }
    },
    'financial_logs': {
        'KR': [
            "{year}년 {month}월의 총 매출은 얼마인가요?",
            "매출이 {revenue}달러를 초과하는 모든 달을 나열해주세요.",
            "{year}년의 연평균 매출은 얼마인가요?",
            "가장 매출이 높았던 해와 달을 알려주세요.",
            "모든 로그 중 매출액이 가장 낮은 달은 언제인가요?"
        ],
        'EN': [
            "What was the total revenue in {month} {year}?",
            "List all months where the revenue exceeded {revenue} dollars.",
            "What is the average monthly revenue for the year {year}?",
            "Which month and year had the highest revenue?",
            "Which month has the lowest revenue amount across all logs?"
        ],
        'entities': {
            'year': ['2022', '2023', '2024'],
            'month': ['Jan', 'Feb', 'Mar', 'Q1', 'Q2'],
            'revenue': ['500', '700', '1000', '1500']
        }
    }
}

def generate_dataset():
    dataset = []
    id_counter = 1
    
    for db_name, db_data in templates.items():
        entities = db_data['entities']
        # Extract keys and values for combinations
        keys, values = zip(*entities.items())
        combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        for lang in ['KR', 'EN']:
            for template in db_data[lang]:
                # Generate variations using combinations
                for combo in combinations:
                    try:
                        question = template.format(**combo)
                        # To avoid combinatorial explosion on non-parameterized strings, check if formatted
                        if question == template and combo != combinations[0]:
                            continue # Skip duplicates for parameter-less templates
                            
                        # Add some random ambiguity/noise occasionally
                        if random.random() < 0.1:
                            question += " (빠르게 알려주세요)" if lang == 'KR' else " (reply fast)"
                            
                        dataset.append({
                            "id": id_counter,
                            "db_name": db_name,
                            "language": lang,
                            "question": question
                        })
                        id_counter += 1
                    except KeyError:
                        pass

    # Shuffle to ensure realistic benchmark conditions
    random.shuffle(dataset)
    
    print(f"Total benchmark questions generated: {len(dataset)}")
    with open('benchmark_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_dataset()
