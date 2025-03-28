import os
import sqlite3 as sql


# conn = sql.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database\db.sqlite'))


class Database:
    __DB_OBJECT = None

    def __init__(self):
        self.conn = sql.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite'))
        self.cursor = self.conn.cursor()

    def getSingleObject(self, sqlQuery, params=()):
        row = self.getRow(sqlQuery, params)
        if (row is not None):
            return row[0]

    def execute(self, sqlQuery, params=()):
        self.cursor.execute(sqlQuery, params)
        self.conn.commit()

    def getRow(self, sqlQuery, params=()):
        print("Params:",params,type(params))
        self.cursor.execute(sqlQuery, params)
        return self.cursor.fetchone()

    @staticmethod
    def getInstance():
        if (Database.__DB_OBJECT is None):
            Database.__DB_OBJECT = Database()
        return Database.__DB_OBJECT
