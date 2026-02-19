import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("memory/ethar.db")

class MemoryDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        # Conversation
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )""")

        # Devices
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS device_states (
            device_name TEXT PRIMARY KEY,
            state TEXT NOT NULL
        )""")

        # User Profile
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )""")

        # Scheduled Tasks
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            action TEXT,
            execute_at TEXT,
            status TEXT
        )""")
        self.conn.commit()

    # ------------------------
    # Conversation
    # ------------------------
    def save_message(self, role, content):
        self.conn.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()

    def load_recent(self, limit=20):
        cursor = self.conn.execute(
            "SELECT role, content FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        rows.reverse()
        return [{"role": r[0], "content": r[1]} for r in rows]

    # ------------------------
    # Devices
    # ------------------------
    def save_device_state(self, device_name, state):
        self.conn.execute("""
        INSERT INTO device_states (device_name, state)
        VALUES (?, ?)
        ON CONFLICT(device_name) DO UPDATE SET state=excluded.state
        """, (device_name, state))
        self.conn.commit()

    def load_device_state(self, device_name):
        cursor = self.conn.execute(
            "SELECT state FROM device_states WHERE device_name = ?",
            (device_name,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    # ------------------------
    # User Profile
    # ------------------------
    def set_profile(self, key, value):
        self.conn.execute("""
        INSERT INTO user_profile (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        self.conn.commit()

    def get_profile(self, key):
        cursor = self.conn.execute(
            "SELECT value FROM user_profile WHERE key = ?",
            (key,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    # ------------------------
    # Scheduled Tasks
    # ------------------------
    def add_scheduled_task(self, device, action, execute_at):
        self.conn.execute("""
        INSERT INTO scheduled_tasks (device, action, execute_at, status)
        VALUES (?, ?, ?, ?)
        """, (device, action, execute_at, "PENDING"))
        self.conn.commit()

    def complete_task(self, device, action):
        self.conn.execute("""
        UPDATE scheduled_tasks
        SET status = ?
        WHERE device = ? AND action = ? AND status = ?
        """, ("COMPLETED", device, action, "PENDING"))
        self.conn.commit()

    def get_pending_tasks(self):
        cursor = self.conn.execute("""
        SELECT device, action, execute_at
        FROM scheduled_tasks
        WHERE status = 'PENDING'
        """)
        return cursor.fetchall()
