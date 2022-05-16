import sqlite3

class EsperosConnection:
    def __init__(self):
        self.connection=sqlite3.connect("Esperos.db")
        self.cursor=self.connection.cursor()
    def close(self):
        self.connection.close()