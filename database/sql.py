import os
import sqlite3 as sql


# conn = sql.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database\db.sqlite'))


class Database:
    __DB_OBJECT = None

    def __init__(self):
        if self.__DB_OBJECT is not None:
            self.__DB_OBJECT.close()
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

    def closeConnection(self):
        self.conn.close()

    @staticmethod
    def getInstance():
        if (Database.__DB_OBJECT is None):
            Database.__DB_OBJECT = Database()
        return Database.__DB_OBJECT
