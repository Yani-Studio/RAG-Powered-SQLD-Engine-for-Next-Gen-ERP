import sqlite3
import pandas as pd

def execute_sql(db_name: str, sql_query: str) -> pd.DataFrame:
    """
    Connects to the specified SQLite database and executes the SQL query.
    Returns the result as a Pandas DataFrame.
    """
    # Database mapping
    db_paths = {
        'department_store': 'databases/department_store.sqlite',
        'hr_management': 'databases/hr_management.sqlite',
        'financial_logs': 'databases/financial_logs.sqlite'
    }
    
    # Extract base name from UI strings like "department_store (Spider)"
    base_name = db_name.split(' ')[0]
    db_file = db_paths.get(base_name)
    
    if not db_file:
        raise ValueError(f"Unknown database: {db_name}")
        
    try:
        conn = sqlite3.connect(db_file)
        # We use pandas to safely execute and fetch data into a dataframe
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        raise e
