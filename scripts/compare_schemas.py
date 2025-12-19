import sqlite3
import sys
import os

def get_schema(db_path):

    """Получаем схему базы данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем все таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}';")
        schema[table_name] = cursor.fetchone()[0]
    
    conn.close()
    return schema

def compare_schemas():
    test_schema = get_schema('test_student_portal.db')  # TEST БД
    stage_schema = get_schema('stage_student_portal.db')  # STAGE БД
    
    if test_schema == stage_schema:
        print("TEST and STAGE schemas are identical")
        return True
    else:
        print("Schemas differ!")
        
        # Находим различия
        test_tables = set(test_schema.keys())
        stage_tables = set(stage_schema.keys())
        
        if test_tables != stage_tables:
            print("Table differences:")
            print(f"TEST has: {test_tables - stage_tables}")
            print(f"STAGE has: {stage_tables - test_tables}")
        
        return False

if __name__ == "__main__":
    success = compare_schemas()
    sys.exit(0 if success else 1)
