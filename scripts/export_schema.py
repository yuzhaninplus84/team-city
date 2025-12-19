import sqlite3
import os
from datetime import datetime

def export_schema():
    # Подключаемся к базе данных
    conn = sqlite3.connect('instance\student_portal.db')
    cursor = conn.cursor()
    
    # Создаем файл с timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    schema_file = f'database/schemas/schema_{timestamp}.sql'
    
    with open(schema_file, 'w', encoding='utf-8') as f:
        f.write(f'-- Database Schema Export\n')
        f.write(f'-- Generated: {datetime.now()}\n')
        f.write(f'-- Database: student_portal.db\n\n')
        
        # Экспортируем схему всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}';")
            schema_sql = cursor.fetchone()[0]
            f.write(f"{schema_sql};\n\n")
            
        # Экспортируем индексы
        f.write('-- Indexes\n')
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
        indexes = cursor.fetchall()
        
        for index in indexes:
            f.write(f"{index[1]};\n")
    
    conn.close()
    print(f"Schema exported to {schema_file}")
    return schema_file

if __name__ == "__main__":
    export_schema()