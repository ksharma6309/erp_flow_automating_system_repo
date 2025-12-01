import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "erp.db"
SEED_SQL = Path(__file__).parent / "seed_data.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    sql = SEED_SQL.read_text()
    cur.executescript(sql)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
