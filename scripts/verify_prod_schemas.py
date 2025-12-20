import sqlite3
import os
import sys
from datetime import datetime

def verify_stage_prod_schemas(stage_db_path, prod_db_path):
    """Проверяет соответствие схем STAGE и PROD баз"""
    
    print(f"Verifying STAGE and PROD database schemas")
    print(f"STAGE: {stage_db_path}")
    print(f"PROD: {prod_db_path}")
    print(f"Time: {datetime.now()}")
    print("=" * 60)
    
    # Проверяем существование файлов
    if not os.path.exists(stage_db_path):
        print(f"STAGE database not found: {stage_db_path}")
        return False
    if not os.path.exists(prod_db_path):
        print(f"PROD database not found: {prod_db_path}")
        return False
    
    def get_schema_summary(db_path):
        """Получает краткую информацию о схеме"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Количество таблиц
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        table_count = cursor.fetchone()[0]
        
        # Список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Общее количество записей
        total_records = 0
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            total_records += cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'table_count': table_count,
            'tables': tables,
            'total_records': total_records
        }
    
    # Получаем информацию о схемах
    stage_info = get_schema_summary(stage_db_path)
    prod_info = get_schema_summary(prod_db_path)
    
    # Выводим информацию
    print(f"\nSTAGE Database Summary:")
    print(f"   Tables: {stage_info['table_count']}")
    print(f"   Total records: {stage_info['total_records']:,}")
    print(f"   Table list: {', '.join(stage_info['tables'])}")
    
    print(f"\nPROD Database Summary:")
    print(f"   Tables: {prod_info['table_count']}")
    print(f"   Total records: {prod_info['total_records']:,}")
    print(f"   Table list: {', '.join(prod_info['tables'])}")
    
    # Сравниваем
    is_identical = True
    differences = []
    
    if stage_info['table_count'] != prod_info['table_count']:
        is_identical = False
        differences.append(f"Table count differs: STAGE={stage_info['table_count']}, PROD={prod_info['table_count']}")
    
    if set(stage_info['tables']) != set(prod_info['tables']):
        is_identical = False
        diff_stage = set(stage_info['tables']) - set(prod_info['tables'])
        diff_prod = set(prod_info['tables']) - set(stage_info['tables'])
        if diff_stage:
            differences.append(f"Tables in STAGE but not in PROD: {diff_stage}")
        if diff_prod:
            differences.append(f"Tables in PROD but not in STAGE: {diff_prod}")
    
    # Вывод результата
    if is_identical:
        print(f"\nSUCCESS: STAGE and PROD schemas are identical!")
    else:
        print(f"\nFAILURE: Schema differences detected:")
        for diff in differences:
            print(f"   - {diff}")
    
    print("=" * 60)
    return is_identical

if __name__ == "__main__":
    # Получаем пути из переменных окружения
    stage_db = os.getenv('STAGE_DB_PATH', 'stage_student_portal.db')
    prod_db = os.getenv('PROD_DB_PATH', 'prod_student_portal.db')
    
    success = verify_stage_prod_schemas(stage_db, prod_db)
    
    # Возвращаем соответствующий код выхода
    sys.exit(0 if success else 1)