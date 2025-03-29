import os
import sqlite3 as sql


class Database:
    __DB_OBJECT = None

    def __init__(self):
        if self.__DB_OBJECT is not None:
            self.__DB_OBJECT.close()
        self.conn = sql.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite'))
        self.cursor = self.conn.cursor()

    def get_single_object(self, sql_query, params=()):
        row = self.get_row(sql_query, params)
        if row is not None:
            return row[0]

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
