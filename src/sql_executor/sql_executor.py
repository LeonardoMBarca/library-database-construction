import os
import sqlite3

class SqlExecutor:
    def __init__(self, logger_console, logger_file):
        self.logger_console = logger_console
        self.logger_file = logger_file
    
    def create_tables(self):
        try:
            db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database")
            tb_sql = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sql", "tables")
            
            conn = sqlite3.connect(os.path.join(db_dir, "library.db"))
            cursor = conn.cursor()

            with open(os.path.join(tb_sql, "create_tables.sql"), "r") as f:
                sql_command = str(f.read())
            
            cursor.execute(sql_command)
        
        except Exception as e:
            self.logger_console.log_error(f"[CREATE TABLE] {e}")
            self.logger_console.log_error(f"[CREATE TABLE] {e}")
