import sqlite3, json
from datetime import datetime, timezone
from typing import Union, Dict, Any


class SharedMemory:
    def __init__(self, use_file_db=False):
        if use_file_db:
            self.conn = sqlite3.connect('shared_memory.db')
        else:
            self.conn = sqlite3.connect(':memory:')  # In-memory for clean runs
        self._init_db()
        
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        
    def log(self, conversation_id: str, data: Dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data
        }
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversation_logs (conversation_id, timestamp, data)
            VALUES (?, ?, ?)
        ''', (conversation_id, entry["timestamp"], json.dumps(entry)))
        self.conn.commit()

    def get_context(self, conversation_id: str) -> list:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT data FROM conversation_logs 
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        ''', (conversation_id,))
        return [json.loads(row[0]) for row in cursor.fetchall()]

    def get_last_extraction(self, conversation_id: str) -> dict:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT data FROM conversation_logs 
            WHERE conversation_id = ? 
            AND data LIKE '%extracted_values%'
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (conversation_id,))
        row = cursor.fetchone()
        return json.loads(row[0])["extracted_values"] if row else {}

    def clear_conversation(self, conversation_id: str) -> None:
        """Clear specific conversation history"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM conversation_logs WHERE conversation_id = ?', (conversation_id,))
        self.conn.commit()

# Initialize shared memory
shared_memory = SharedMemory()