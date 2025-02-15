import json
import time
from typing import Optional, Dict, Any, List, Union
import threading
import traceback
import sqlite3
import inspect
import requests
from ..exceptions.base import (BaleException)
from ..objects.keyboards import (InlineKeyboardButton,InlineKeyboardMarkup,MenuKeyboardButton,MenuKeyboardMarkup)
from ..objects.callbackquery import (CallbackQuery)
from ..objects.chat import (Chat)
from ..objects.voice import (Voice)
from ..objects.document import (Document)
from ..objects.photo import (Photo)
from ..objects.message import (Message)
from ..objects.user import (User)
from ..objects.location import (Location)
from ..objects.contact import (Contact)
from ..objects.inputfile import(InputFile)
from ..objects.labeledprice import (LabeledPrice)
from ..objects.invoice import (Invoice)
from ..objects.client import (Client)
from ..objects.chatmember import (ChatMember)

class DataBase:
    """
    Database class for managing key-value pairs in a SQLite database.
    """
    def __init__(self, name):
        self.name = name
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS key_value_store
                        (key TEXT PRIMARY KEY, value TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def read_database(self, include_timestamps=False):
        if not self.conn:
            self._initialize_db()
        if include_timestamps:
            self.cursor.execute(
                "SELECT key, value, created_at, updated_at FROM key_value_store")
            rows = self.cursor.fetchall()
            return {
                key: {
                    'value': json.loads(value),
                    'created_at': created,
                    'updated_at': updated} for key,
                value,
                created,
                updated in rows}
        else:
            self.cursor.execute("SELECT key, value FROM key_value_store")
            rows = self.cursor.fetchall()
            return {key: json.loads(value) for key, value in rows}

    def write_database(self, data_dict):
        if not self.conn:
            self._initialize_db()
        for key, value in data_dict.items():
            self.cursor.execute("""
                INSERT INTO key_value_store (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                value=excluded.value, updated_at=CURRENT_TIMESTAMP""",
                                (key, json.dumps(value, default=str)))
        self.conn.commit()

    def read_key(self, key: str, default=None):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "SELECT value FROM key_value_store WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return json.loads(result[0]) if result else default

    def write_key(self, key: str, value):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("""
            INSERT INTO key_value_store (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
            value=excluded.value, updated_at=CURRENT_TIMESTAMP""",
                            (key, json.dumps(value, default=str)))
        self.conn.commit()

    def delete_key(self, key: str):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "DELETE FROM key_value_store WHERE key = ?", (key,))
        self.conn.commit()

    def keys(self):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("SELECT key FROM key_value_store")
        return [row[0] for row in self.cursor.fetchall()]

    def clear(self):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("DELETE FROM key_value_store")
        self.conn.commit()

    def get_metadata(self, key: str):
        if not self.conn:
            self._initialize_db()
        self.cursor.execute("""
            SELECT created_at, updated_at
            FROM key_value_store
            WHERE key = ?""", (key,))
        result = self.cursor.fetchone()
        return {
            'created_at': result[0],
            'updated_at': result[1]} if result else None

    def exists(self, key: str) -> bool:
        if not self.conn:
            self._initialize_db()
        self.cursor.execute(
            "SELECT 1 FROM key_value_store WHERE key = ?", (key,))
        return bool(self.cursor.fetchone())