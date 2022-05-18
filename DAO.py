import sqlite3


class EsperosConnection:
    def __init__(self):
        """
        Constructor for Data Application object.

        :return: None.
        """
        self.connection: sqlite3.Connection = sqlite3.connect("Esperos.db")
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def close(self):
        """
        A Callback for closing the database

        :return: None.
        """
        self.connection.close()

    def get_categories(self, no_coach: bool = True) -> list:
        """
        A getter for the table categories

        :param no_coach: whether the coach entry is used or not
        :return: list of the reults
        """
        query = "SELECT Cat_name " + \
                "FROM Category"
        if not no_coach:
            query += " WHERE Cat_name != 'Προπονητής';"
        rows = self.cursor.execute(query)
        self.connection.commit()
        return list(rows)

    def get_athlete_info(self, search: str):
        """
        Retrieve the athlete info from the db

        :param search: the search term to look for a certain athlete, is nullable
        :return: the list of matches
        """
        query = "Select State as Κατάσταση, p.Name as Όνομα,p.Surname as Επώνυμο,Cat as Κατηγορία,Home_pn as Σταθερό," \
                "Cellphone_pn as Κινητό, Email, Responsibilities as Εκκρεμότητες, Last_payment as Πληρωμή From Person " \
                "p join Athlete_Data a on p.Surname=a.Surname and p.Name=a.Name "
        if search is not None:
            query += f" and (instr(p.Name,'{search}')>0 or instr(p.Surname,'{search}')>0 or instr(p.Cat,'{search}')>0)"
        data = self.cursor.execute(query)
        self.connection.commit()
        return data.fetchall()

    def get_occupation(self, cat: str) -> str:
        """
        A getter for the occupation a certain category corresponds to.

        :param cat: The name of the category
        :return: The string value of the occupation
        """
        rows = self.cursor.execute(f"SELECT Occupation FROM Category WHERE Cat_name={cat}")
        return rows.fetchall()[0]

    def get_attributes(self, mode: int) -> list:
        """
        Getter for the attributes of the current category

        :param mode: indicator for what type of info we are looking for. 0 for plain Person, 1 for Athlete and 2 for
        Non_athlete POI.
        :return: the list of attributes requested
        """
        query = "Select name from pragma_table_info('Person')"

        # If we are looking for Athletes
        if mode == 1:
            query += "UNION\nSELECT name from pragma_table_info('Athlete_Data')"
        # if we are looking for Non_athlete People of Interest
        elif mode == 2:
            query += "UNION\nSELECT name from pragma_table_info('Non_athlete_POI')"

        data = self.cursor.execute(query).fetchall()
        return data

    def get_person_by_category(self, category: str, parameter: str = None):
        """
        Matcher for every person that belongs in a certain category, with an additional parameter that is requested.

        :param category: The category we are filtering on.
        :param parameter: The optional additional parameter we are looking to add as well.
        :return: the list of person objects (Surname, Name, Category[, Parameter]).
        """
        if parameter is not None:
            occ = self.get_occupation(category)
            table = ""
            if occ == "Αθλητής/τρια":
                table = "Athlete_Data"
            else:
                table = "Non_athlete_POI"
            query = f"SELECT Surname,Name,Cat{',' + parameter} FROM Person p join {table} t on p.Surname=t.Surname and p.Name=t.Name  WHERE Cat={category} "
        else:
            query = f"SELECT Surname,Name,Cat FROM Person WHERE Cat={category} "
        return self.cursor.execute(query).fetchall()
