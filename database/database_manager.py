import sqlite3
import os
import sys


class GameDatabase:
    def __init__(self):
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        db_dir = os.path.join(base_path, "database")
        os.makedirs(db_dir, exist_ok=True)

        self.db_file = os.path.join(db_dir, "records.db")
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS winners (name TEXT, score INTEGER, time REAL)"
        )
        conn.commit()
        conn.close()

    def save_winner(self, name, score, time):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO winners VALUES (?, ?, ?)", (name, score, time))
        conn.commit()
        conn.close()

    def get_top_winners(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT name, score, time FROM winners ORDER BY time ASC LIMIT 5")
        results = cur.fetchall()
        conn.close()
        return results
