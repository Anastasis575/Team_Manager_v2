from collections.abc import Callable


class pageManager:
    def __init__(self, page_change: Callable[[str], []]):
        self.page_change = page_change
        self.pages = []

    def go_back(self):
        pass

    def go_forward(self):
        pass
