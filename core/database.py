# =========================================================
# CORE/DATABASE.PY - TẦNG 8: LƯU TRỮ & QUẢN TRỊ SQLITE
# =========================================================
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join("data", "phcn_database.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Bảng quản lý hành chính bệnh nhân
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    age INTEGER,
                    job TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            # Bảng lưu trữ từng lần khám (Không ghi đè lịch sử cũ)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL,
                    visit_date TEXT NOT NULL,
                    region TEXT NOT NULL,
                    summary TEXT,
                    clinical_data TEXT,
                    FOREIGN KEY (phone) REFERENCES patients (phone)
                )
            """)
            conn.commit()
