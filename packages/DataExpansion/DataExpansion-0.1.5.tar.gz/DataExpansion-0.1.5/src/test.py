from os import name
from DataExpansion import sqlite_class
import sqlite3

class TestObj:
    def __init__(self, value):
        self.value = value

    def printNum(self):
        print(self.value)

sql_connection = sqlite3.connect("test.db")
sql = sqlite_class.SQLite_Ex(TestObj, [], [sqlite_class.IntegerField("vcs")], "main", sql_connection)
#sql.sql_init()
#sql.model_set([250])
a = sql.model_getif("vcs > ?", [500])
print(a.printNum())
sql_connection.close()