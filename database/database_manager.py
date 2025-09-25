import sqlite3

class GameDatabase:
    def __init__(self):
        self.db_file = "database/records.db"
        self.create_table()
    
    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)")
        conn.commit()
        conn.close()
    
    def save_score(self, name, score):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO scores VALUES (?, ?)", (name, score))
        conn.commit()
        conn.close()
    
    def get_top_scores(self):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 5")
        return cur.fetchall()
    
# Тест
'''if __name__ == "main":
    db = GameDatabase()
    db.save_score("Игрок1", 150)
    db.save_score("Игрок2", 200)
    print("Лучшие:", db.get_top_scores())'''