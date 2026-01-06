import os
import sqlite3 as sql
from pathlib import Path
import sys

from scripts.helper import abs_path


class Database:
    __DB_OBJECT = None

    def __init__(self):
        if self.__DB_OBJECT is not None:
            self.__DB_OBJECT.close()
        # self.conn = sql.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite'))
        self.conn = initialize_database()
        self.cursor = self.conn.cursor()

    def get_single_object(self, sql_query, params=()):
        row = self.get_row(sql_query, params)
        if row is not None:
            return row[0]
        return None

    def execute(self, sql_query, params=()):
        self.cursor.execute(sql_query, params)
        self.conn.commit()

    def get_row(self, sql_query, params=()):
        self.cursor.execute(sql_query, params)
        return self.cursor.fetchone()

    def close_connection(self):
        self.conn.close()

    @staticmethod
    def get_instance():
        if Database.__DB_OBJECT is None:
            Database.__DB_OBJECT = Database()
        return Database.__DB_OBJECT


def get_db_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = abs_path('')
    return os.path.join(application_path, 'db.sqlite')


def initialize_database():
    db_file = get_db_path()
    if Path(db_file).exists():
        conn = sql.connect(db_file)
        print("Database already initialized")
        return conn
    conn = sql.connect(db_file)
    cursor = conn.cursor()
    create_table_query = "CREATE TABLE IF NOT EXISTS player_data (id TEXT PRIMARY KEY UNIQUE NOT NULL, value TEXT NOT NULL)"
    cursor.execute(create_table_query)
    add_value_query = "INSERT INTO player_data (id, value) VALUES (?, ?)"
    cursor.executemany(add_value_query, [('xp',0),('coin',0),('last_seen',0),('music',1),('sound',1)])
    conn.commit()
    print(f"Database initialized at: {db_file}")
    return conn