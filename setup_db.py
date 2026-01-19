import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "orders.db")


def setup():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    # All data is synthetic (written by simulate.py), so always start from a clean file
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Database deleted.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE orders (
            row_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp    TEXT,
            customer_id  TEXT,
            order_amount REAL,
            status       TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


if __name__ == "__main__":
    setup()
