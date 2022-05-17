import sqlite3


class EsperosConnection:
    def __init__(self):
        """
        Constructor for Data Application object
        """
        self.connection: sqlite3.Connection = sqlite3.connect("Esperos.db")
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def get_categories(self, no_coach: bool = True) -> list:
        """
        A getter for the table categories

        :param no_coach: whether the coach entry is used or not
        :return: list of the reults
        """
        sql = "SELECT *" + \
              "FROM Category"
        if not no_coach:
            sql += " WHERE Cat_name != 'Προπονητής';"
        print(sql)
        rows = self.cursor.execute(sql)
        print(rows)
        self.connection.commit()
        return list(rows)
