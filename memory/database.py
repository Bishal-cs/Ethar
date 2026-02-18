import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ethar.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            name TEXT PRIMARY KEY,
            state TEXT
        )
    """)

    conn.commit()
    conn.close()


# 🔥 Call init immediately when file loads
init_db()


def save_device_state(name, state):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO devices (name, state)
        VALUES (?, ?)
        ON CONFLICT(name)
        DO UPDATE SET state=excluded.state
    """, (name, state))

    conn.commit()
    conn.close()


def load_device_state(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT state FROM devices WHERE name = ?", (name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None
