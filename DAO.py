import sqlite3


class EsperosConnection:
    def __init__(self):
        """
        Constructor for Data Application object.

        :return: None.
        """
        self.connection: sqlite3.Connection = sqlite3.connect("Esperos.db")
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, typ, value, tb):
        """
        A Callback for closing the database.

        :param typ:
        :param value:
        :param tb:
        :return: None.
        """
        self.connection.close()

    def get_categories(self, no_coach: bool = True) -> list:
        """
        A getter for the table categories

        :param no_coach: whether the coach entry is used or not
        :return: list of the reults
        """
        query = "SELECT Κατηγορία " + \
                "FROM Category"
        if not no_coach:
            query += " WHERE Κατηγορία != 'Προπονητής';"
        rows = self.cursor.execute(query)
        self.connection.commit()
        return list(rows)

    def get_athlete_info(self, search: str):
        """
        Retrieve the athlete info from the db

        :param search: the search term to look for a certain athlete, is nullable
        :return: the list of matches
        """
        query = "Select Κατάσταση,p.Όνομα,p.Επώνυμο, Κατηγορία,Σταθερό, Κινητό, Email, Υποχρεώσεις,Τελευταία_πληρωμή " \
                "From Person p join Athlete_Data a on p.Επώνυμο=a.Επώνυμο and p.Όνομα=a.Όνομα "
        if search is not None:
            query += f" and (instr(p.Επώνυμο,'{search}')>0 or instr(p.Όνομα,'{search}')>0 or instr(p.Κατηγορία,'{search}')>0) "
        data = self.cursor.execute(query)
        self.connection.commit()
        return data.fetchall()

    def get_occupation(self, cat: str) -> str:
        """
        A getter for the occupation a certain category corresponds to.

        :param cat: The name of the category
        :return: The string value of the occupation
        """
        rows = self.cursor.execute(f"SELECT Απασχόληση FROM Category WHERE Κατηγορία='{cat}'")
        self.connection.commit()
        data = rows.fetchall()
        if len(data) == 0:
            return ""
        else:
            return data[0][0]

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
        self.connection.commit()
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
            print(occ)
            table = ""
            if occ == "Αθλητής/τρια":
                table = "Athlete_Data"
            else:
                table = "Non_athlete_POI"
            query = f"SELECT p.Επώνυμο ,p.Όνομα, Κατηγορία{',' + parameter} FROM Person p join {table} t on p.Επώνυμο=t" \
                    f".Επώνυμο and p.Όνομα=t.Όνομα  WHERE Κατηγορία='{category}' "
        else:
            query = f"SELECT p.Επώνυμο,p.Όνομα,Κατηγορία FROM Person p WHERE Κατηγορία='{category}' "
        data = self.cursor.execute(query).fetchall()
        self.connection.commit()
        return data

    def get_person_info(self, surname: str, name: str, occ: str) -> dict:
        """
        A retrieval function for the person info.

        :param surname: The surname of the person.
        :param name: The name of the person.
        :param occ: The occupation of the person.
        :return: the dictionary with their information.
        """
        table = ""
        if occ == "Αθλητής/τρια":
            table = "Athlete_Data"
        else:
            table = "Non_athlete_POI"

        query = f"SELECT * FROM Person p join {table} t on p.Επώνυμο=t.Επώνυμο and p.Όνομα=t.Όνομα WHERE " \
                f"p.Επώνυμο='{surname}' and p.Όνομα='{name}';"
        cu = self.cursor.execute(query)
        des = list(map(lambda c: c[0], cu.description))
        res = cu.fetchall()
        if len(res) != 0:
            res = list(res[0])
        self.connection.commit()
        return dict(zip(des, res))

    def create_person_entry(self, surname: str, name: str, occ: str, data: dict) -> None:
        """
        The method to insert the entry of a new person to the corresponding tables.

        :param occ: the default occupation
        :param surname: Surname of the new person entry.
        :param name: Name of the new person entry
        :param data: The object with the information of the new person entry
        :return: None.
        """
        ret_occ = self.get_occupation(data["Κατηγορία"])
        if ret_occ == "":
            query = f"INSERT INTO Category VALUES('{data['Κατηγορία']}','{occ}')"
            self.cursor.execute(query)
        ret_occ = occ
        query = f"INSERT INTO Person VALUES(\'{data['Επώνυμο']}\',\'{data['Όνομα']}\',\'{data['Σταθερό']}\'," \
                f"\'{data['Κινητό']}\',\'{data['Email']}\',\'{data['Διεύθυνση']}\',\'{data['Κατηγορία']}\'," \
                f"\'{data['Ημερομηνία_Δημιουργίας']}\')"
        self.cursor.execute(query)
        if ret_occ == "Αθλητής/τρια":
            query = f"INSERT INTO Athlete_Data VALUES(\'{data['Επώνυμο']}\',\'{data['Όνομα']}\',\'{data['Έτος']}\'," \
                    f"\'{data['Ύψος']}\',\'{data['Ενεργά_χρόνια']}\',\'{data['Προπονητής']}\'," \
                    f"\'{data['Δωρεάν_μπλούζες']}\',\'{data['Χρεωμένες_μπλούζες']}\',\'{data['Ποσό_για_Μπλούζες']}\'," \
                    f"\'{data['Υποχρεώσεις']}\',\'{data['Τελευταία_πληρωμή']}\',\'{data['Κατάσταση']}\')"
        else:
            query = f"INSERT INTO Non_athlete_POI VALUES(\'{data['Επώνυμο']}\',\'{data['Όνομα']}\',\'{data['Επάγγελμα']}\'," \
                    f"\'{data['Χόμπυ']}\',\'{data['Σχέση_με_Άθλημα']}\')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_person_entry(self, name: str, surname: str, def_occ: str, data: dict) -> None:
        """
        Update method for the person entry.

        :param surname: Surname of the person whose info is to be updated.
        :param name: Surname of the person whose info is to be updated.
        :param data: Name of the person whose info is to be updated.
        :return: None.
        """
        occ = self.get_occupation(data["Κατηγορία"])
        self.clear_categories()
        if occ == "":
            query = f"INSERT INTO Category VALUES ('{data['Κατηγορία']}','{def_occ}')"
            self.cursor.execute(query)
            self.connection.commit()
            occ = def_occ

        extra = ""
        if "Κατάσταση" in data.keys():
            extra = f",Τελευταία_πληρωμή=\'{data['Τελευταία_πληρωμή']}\',Κατάσταση=\'{data['Κατάσταση']}\'"

        query = f"UPDATE Person SET Επώνυμο=\'{data['Επώνυμο']}\',Όνομα=\'{data['Όνομα']}\',Σταθερό=\'{data['Σταθερό']}\'," \
                f"Κινητό=\'{data['Κινητό']}\',Email=\'{data['Email']}\',Διεύθυνση=\'{data['Διεύθυνση']}\'," \
                f"Κατηγορία=\'{data['Κατηγορία']}\' WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        self.cursor.execute(query)
        self.connection.commit()
        if occ == "Αθλητής/τρια":
            query = f"UPDATE Athlete_Data SET Επώνυμο=\'{data['Επώνυμο']}\',Όνομα=\'{data['Όνομα']}\'," \
                    f"Έτος=\'{data['Έτος']}\',Ύψος={data['Ύψος']},Ενεργά_χρόνια={data['Ενεργά_χρόνια']}," \
                    f"Προπονητής=\'{data['Προπονητής']}\',Δωρεάν_μπλούζες={data['Δωρεάν_μπλούζες']}," \
                    f"Χρεωμένες_μπλούζες={data['Χρεωμένες_μπλούζες']}," \
                    f"Ποσό_για_Μπλούζες={data['Ποσό_για_Μπλούζες']},Υποχρεώσεις={data['Υποχρεώσεις']}{extra}" \
                    f" WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        else:
            query = f"UPDATE Non_athlete_POI  SET Επώνυμο=\'{data['Επώνυμο']}\',Όνομα=\'{data['Όνομα']}\'," \
                    f"Επάγγελμα=\'{data['Επάγγελμα']}\',Χόμπυ=\'{data['Χόμπυ']}\'," \
                    f"Σχέση_με_Άθλημα\'{data['Σχέση_με_Άθλημα']}\' WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def get_person_responsibility(self, surname: str, name: str) -> float:
        """
        Getter to return the saved responsibility.

        :param surname: Surname of the user to check.
        :param name: Name of the user to check.
        :return: the responsibility.
        """
        query = f"SELECT Υποχρεώσεις FROM Athlete_data WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        rows = self.cursor.execute(query).fetchall()
        if len(rows) == 0:
            return -1.0
        self.connection.commit()
        return rows[0][0]

    def get_delete_information(self, search: str) -> dict:
        query = "SELECT * FROM PERSON"
        if search is not None:
            query += f" WHERE Επώνυμο like '%{search}%' or Όνομα like '%{search}%' or Κατηγορία like '%{search}%'"
        data = self.cursor.execute(query)
        des = list(map(lambda c: c[0], data.description))
        res = data.fetchall()
        fin = {}
        if len(res) != 0:
            fin = list(map(lambda x: dict(zip(des, x)), res))
        self.connection.commit()
        return fin

    def delete_person_entry(self, surname: str, name: str, category: str):
        """
        Delete a person entry based on their full name and category.

        :param surname: The surname of the entry to be deleted.
        :param name: The name of the entry to be deleted
        :param category: The name of the category of the person to be deleted
        :return: None.
        """
        occ = self.get_occupation(category)
        if occ == "Αθλητής/τρια":
            query = f"DELETE FROM Athlete_Data WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        else:
            query = f"DELETE FROM Non_athlete_POI WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        self.cursor.execute(query)
        query = f"DELETE FROM Person WHERE Επώνυμο='{surname}' and Όνομα='{name}'"
        self.cursor.execute(query)
        query = f"SELECT * FROM Person WHERE Κατηγορία='{category}'"
        last = self.cursor.execute(query)
        if len(last.fetchall()) == 0:
            query = f"DELETE FROM Category WHERE Κατηγορία='{category}'"
            self.cursor.execute(query)
        self.connection.commit()

    def get_athlete_categories(self, no_coach: bool) -> list:
        """
        Getter for all the athlete_categories that can be edited
        :param no_coach: a boolean value whether to include the coach entries
        :return: The list of athlete category names.
        """
        query = f"SELECT Κατηγορία FROM Category WHERE Απασχόληση='Αθλητής/τρια'"
        res = self.cursor.execute(query).fetchall()
        self.connection.commit()
        if len(res) == 0:
            return res
        else:
            return list(map(lambda x: x[0], res))

    def rename_category(self, old_name: str, new_name: str) -> None:
        query = f"SELECT Κατηγορία FROM Category WHERE Κατηγορία='{new_name}'"
        res = self.cursor.execute(query).fetchall()
        if len(res) == 0:
            query = f"UPDATE Category SET Κατηγορία='{new_name}' WHERE Κατηγορία='{old_name}' "
        else:
            query = f"DELETE FROM Category WHERE Κατηγορία='{old_name}' "
        self.cursor.execute(query)
        self.connection.commit()
        query = f"UPDATE Person SET Κατηγορία='{new_name}' WHERE Κατηγορία='{old_name}'"
        self.cursor.execute(query)
        self.connection.commit()

    def clear_categories(self):
        query = "SELECT Κατηγορία FROM Category WHERE Κατηγορία NOT IN (SELECT DISTINCT Κατηγορία FROM Person)"
        res = self.cursor.execute(query).fetchall()
        if len(res) == 0:
            return
        for i in list(map(lambda x: x[0], res)):
            query = f"DELETE FROM Category WHERE Κατηγορία='{i}'"
            self.cursor.execute(query)
            self.connection.commit()
