from DAO import EsperosConnection


class LogicController:
    def __init__(self, doa: EsperosConnection = None):
        self.dao: EsperosConnection = doa

    def set_doa(self, doa: EsperosConnection) -> None:
        self.dao = doa

    def create_entry(self):
        pass

    def get_responsibility_information(self, search: str = None) -> list:
        """
        A wrapper method to retrieve and curate the responsibility information for all athletes.

        :param search: The input from the search bar if any.
        :return: the list of dictionaries that contain the information of the users.
        """
        data = self.dao.get_athlete_info(search)
        data = list(map(lambda x: dict(
            zip(["Κατάσταση", "Όνομα", "Επώνυμο", "Κατηγορία", "Σταθερό", "Κινητό", "Email", "Εκκρεμότητες", "Πληρωμή"],
                x)),
                        data))
        return data

    def get_categories_no_coach(self) -> list:
        """
        A wrapper function for getting all the existing categories, but ignoring the coach.

        :return: list of the names of the requested categories.
        """
        data = self.dao.get_categories(False)
        data = list(map(lambda x: x[0], data))
        return data

    def get_person_attributes(self, category: str):
        """
        A wrapper function to retrieve and curate the Person attributes.

        :param category: the category we are selecting the attributes from.
        :return: a list of the attributes the user can choose to mass read.
        """
        if category is not None:
            occ = self.dao.get_occupation(category)
            if occ == "Αθλητής/τρια":
                return list(map(lambda x: x[0], self.dao.get_attributes(1)))
            else:
                return list(map(lambda x: x[0], self.dao.get_attributes(2)))
        return list(map(lambda x: x[0], self.dao.get_attributes(0)))

    def match_person_by_category(self, category: str, parameter: str = None) -> list:
        """
        Method to get all Person entries that are in the same categories, (Surname, Name,Category) and a requested
        other attribute.

        :param category: The category all entries must be in.
        :param parameter: The optional additional attribute value that is requested.
        :return: list of person data that matches the query category.
        """
        data = self.dao.get_person_by_category(category, parameter)
        names = ["Επώνυμο", "Όνομα", "Κατηγορία"]
        if parameter is not None:
            names.append(parameter)
        return list(map(lambda x: data(zip(names, x)), data))

    def get_person_attributes_by_occupation(self, occ: str) -> list:
        """
        Getter function for all attributes that correspond to a certain occupation.

        :param occ: The name of the occupation.
        :return: the list of attributes that define a person with the requested occupation.
        """
        if occ == "Αθλητής/τρια":
            return list(map(lambda x: x[0], self.dao.get_attributes(1)))
        return list(map(lambda x: x[0], self.dao.get_attributes(2)))
