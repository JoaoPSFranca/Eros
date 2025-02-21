import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        try:
            os.makedirs('data', exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                input TEXT,
                response TEXT
            )''')

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao configurar banco de dados: {e}")

    def save_interaction(self, user_input, response):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO history (timestamp, input, response)
            VALUES (?, ?, ?)
            ''', (datetime.now().isoformat(), user_input, response))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao salvar interação: {e}")

    def get_history(self, limit=5):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, input FROM history ORDER BY timestamp DESC LIMIT ?", (limit,))
            history = cursor.fetchall()
            conn.close()
            return history
        except Exception as e:
            print(f"Erro ao acessar histórico: {e}")
            return []
