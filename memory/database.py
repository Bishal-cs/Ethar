import sqlite3
from pathlib import Path


DB_PATH = Path("memory/ethar.db")


class MemoryDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS device_states (
            device_name TEXT PRIMARY KEY,
            state TEXT NOT NULL
        )
        """)

        self.conn.commit()

    # -----------------------
    # Conversation memory
    # -----------------------

    def save_message(self, role: str, content: str):
        self.conn.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()

    def load_recent(self, limit=20):
        cursor = self.conn.execute("""
        SELECT role, content FROM conversations
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        rows.reverse()
        return [{"role": r[0], "content": r[1]} for r in rows]

    # -----------------------
    # Device state memory
    # -----------------------

    def save_device_state(self, device_name: str, state: str):
        self.conn.execute("""
        INSERT INTO device_states (device_name, state)
        VALUES (?, ?)
        ON CONFLICT(device_name)
        DO UPDATE SET state=excluded.state
        """, (device_name, state))
        self.conn.commit()

    def load_device_state(self, device_name: str):
        cursor = self.conn.execute("""
        SELECT state FROM device_states WHERE device_name = ?
        """, (device_name,))
        row = cursor.fetchone()
        return row[0] if row else None
