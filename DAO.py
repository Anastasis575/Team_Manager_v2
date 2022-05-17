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
        rows = self.cursor.execute(sql)
        self.connection.commit()
        return list(rows)

    def get_athlete_info(self, search: str):
        """
        Retrieve the athlete info from the db

        :param search: the search term to look for a certain athlete, is nullable
        :return: the list of matches
        """
        sql = "Select State as Κατάσταση, p.Name as Όνομα,p.Surname as Επώνυμο,Cat as Κατηγορία,Home_pn as Σταθερό," + \
              "Cellphone_pn as Κινητό, Email, Responsibilities as Εκκρεμότητες, Last_payment as Πληρωμή From Person p " + \
              "join Athlete_Data a on p.Surname=a.Surname and p.Name=a.Name"
        if search is not None:
            sql += f" and (instr(p.Name,'{search}')>0 or instr(p.Surname,'{search}')>0 or instr(p.Cat,'{search}')>0)"
        data = self.cursor.execute(sql)
        self.connection.commit()
        return data.fetchall()
