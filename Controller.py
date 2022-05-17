from DAO import EsperosConnection


class LogicController:
    def __init__(self, doa: EsperosConnection = None):
        self.dao: EsperosConnection = doa

    def set_doa(self, doa: EsperosConnection) -> None:
        self.dao = doa

    def create_entry(self):
        pass

    def get_resoponsibility_information(self, search: str = None) -> list:
        data = self.dao.get_athlete_info(search)
        data = list(map(lambda x: dict(
            zip(["Κατάσταση", "Όνομα", "Επώνυμο", "Κατηγορία", "Σταθερό", "Κινητό", "Email", "Εκκρεμότητες", "Πληρωμή"],
                x)),
                        data))
        return data

    def get_categories_no_coach(self):
        data = self.dao.get_categories(False)
        data = list(map(lambda x: x[0], data))
        return data
