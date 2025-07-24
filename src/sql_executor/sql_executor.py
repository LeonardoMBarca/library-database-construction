import os
import sqlite3
from pathlib import Path

class SqlExecutor:
    def __init__(self, logger_console, logger_file):
        self.logger_console = logger_console
        self.logger_file = logger_file
        base_dir = Path(__file__).resolve().parents[2]
        self.db_path = base_dir / "database" / "library.db"
        self.tables_sql = base_dir / "sql" / "tables"
        self.insert_dir = base_dir / "sql" / "inserts"

    def _log(self, msg: str, level="info"):
        getattr(self.logger_console, f"log_{level}")(msg)
        getattr(self.logger_file, f"log_{level}")(msg)

    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        try:
            self._log("[CREATE TABLE] Create tables process started")

            with self._connect() as conn, open(os.path.join(self.tables_sql, "create_tables.sql"), "r") as f:
                conn.executescript(f.read())

            self._log(f"[CREATE TABLE] Process Finished")

        except Exception as e:
            self._log(f"[CREATE TABLE] {e}", "error")

    def insert_data(self):
        try:
            self._log("[INSERT DATA] Insert data process started")

            with self._connect() as conn:
                for file in os.listdir(self.insert_dir):
                    with open(self.insert_dir / file, "r") as f:
                        conn.executescript(f.read())
            
            self._log(f"[INSERT DATA] Process Finished")

        except Exception as e:
            self._log(f"[INSERT DATA] {e}", "error")

    def delete_tables(self):
        try:
            self._log("[DELETE TABLE] Delete tables process started")
            
            tables = ["authors", "genres", "books", "comments"]
            
            with self._connect() as conn:
                for table in tables:
                    conn.execute(f"DROP TABLE IF EXISTS {table};")

            self._log(f"[DELETE TABLE] Process Finished")

        except Exception as e:
            self._log(f"[DELETE TABLE] {e}", "error")
    
    def execute(self):
        self.delete_tables()
        self.create_tables()
        self.insert_data()