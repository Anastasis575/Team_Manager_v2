import DOA


class LogicController:
    def __init__(self, doa: DOA, ):
        self.doa = None

    def setDoa(self, doa: DOA) -> None:
        self.doa = doa
