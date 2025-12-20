import sqlite3
import os
import shutil
import zipfile
from datetime import datetime
import argparse
import json

class DatabaseBackup:
    def __init__(self, env='production'):
        self.env = env
        self.backup_dir = 'database/backups'
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Создаем директорию для бэкапов если её нет
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_sqlite(self, db_path):
        """Создает резервную копию SQLite базы данных"""
        if not os.path.exists(db_path):
            print(f"Database file not found: {db_path}")
            return None
        
        # Создаем имя файла бэкапа
        db_name = os.path.basename(db_path).replace('.db', '')
        backup_name = f"{db_name}_{self.env}_{self.timestamp}"
        backup_file = os.path.join(self.backup_dir, f"{backup_name}.db")
        
        print(f"   Creating backup of {db_path}")
        print(f"   Environment: {self.env}")
        print(f"   Backup file: {backup_file}")
        
        try:
            # Создаем соединение с исходной БД
            source_conn = sqlite3.connect(db_path)
            
            # Создаем файл бэкапа
            backup_conn = sqlite3.connect(backup_file)
            
            # Используем backup API SQLite
            source_conn.backup(backup_conn)
            
            # Закрываем соединения
            source_conn.close()
            backup_conn.close()
            
            # Добавляем метаданные
            self.add_metadata(backup_file, db_path)
            
            # Сжимаем бэкап
            compressed_file = self.compress_backup(backup_file)
            
            # Удаляем несжатый файл
            os.remove(backup_file)
            
            print(f"Backup created successfully: {compressed_file}")
            return compressed_file
            
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return None
    
    def add_metadata(self, backup_file, original_db):
        """Добавляет метаданные в файл бэкапа"""
        metadata = {
            'environment': self.env,
            'backup_time': self.timestamp,
            'original_database': original_db,
            'database_size': os.path.getsize(original_db),
            'backup_size': os.path.getsize(backup_file),
            'tables': self.get_table_info(original_db)
        }
        
        # Сохраняем метаданные в JSON файл
        metadata_file = backup_file.replace('.db', '_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def get_table_info(self, db_path):
        """Получает информацию о таблицах в БД"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        
        table_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            table_info[table_name] = row_count
        
        conn.close()
        return table_info
    
    def compress_backup(self, backup_file):
        """Сжимает файл бэкапа в ZIP архив"""
        zip_file = backup_file.replace('.db', '.zip')
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем файл БД
            zipf.write(backup_file, os.path.basename(backup_file))
            
            # Добавляем метаданные если есть
            metadata_file = backup_file.replace('.db', '_metadata.json')
            if os.path.exists(metadata_file):
                zipf.write(metadata_file, os.path.basename(metadata_file))
        
        return zip_file
    
    def cleanup_old_backups(self, keep_last=10):
        """Удаляет старые бэкапы, оставляя только последние N"""
        backup_files = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.zip'):
                backup_files.append(os.path.join(self.backup_dir, file))
        
        # Сортируем по времени изменения (новые первыми)
        backup_files.sort(key=os.path.getmtime, reverse=True)
        
        # Удаляем старые бэкапы
        if len(backup_files) > keep_last:
            for old_backup in backup_files[keep_last:]:
                print(f"Removing old backup: {os.path.basename(old_backup)}")
                os.remove(old_backup)
    
    def list_backups(self):
        """Выводит список доступных бэкапов"""
        print(f"\nAvailable backups in {self.backup_dir}:")
        print("-" * 60)
        
        backups = []
        for file in sorted(os.listdir(self.backup_dir)):
            if file.endswith('.zip'):
                file_path = os.path.join(self.backup_dir, file)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # в MB
                
                backups.append({
                    'name': file,
                    'time': file_time,
                    'size': file_size
                })
        
        for backup in backups:
            print(f"{backup['name']}")
            print(f"   Time: {backup['time'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Size: {backup['size']:.2f} MB")
            print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Database Backup Utility')
    parser.add_argument('--env', default='production', help='Environment name')
    parser.add_argument('--db-path', help='Path to database file')
    parser.add_argument('--list', action='store_true', help='List available backups')
    parser.add_argument('--keep', type=int, default=10, help='Number of backups to keep')
    
    args = parser.parse_args()
    
    backup_manager = DatabaseBackup(env=args.env)
    
    if args.list:
        backup_manager.list_backups()
    elif args.db_path:
        backup_file = backup_manager.backup_sqlite(args.db_path)
        if backup_file:
            backup_manager.cleanup_old_backups(keep_last=args.keep)
    else:
        print("Please specify database path with --db-path option")