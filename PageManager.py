import logging as log
from collections.abc import Callable


class PageManager:
    def __init__(self, curr: str, page_change: Callable[[str], []]):
        """
        Constructor for the page manager

        :param curr: the current page name
        :param page_change: the callback to change the page
        :return: None
        """
        self.curr = curr
        self.page_change = page_change
        self.pages = []
        self.back = []
        self.forward = []

    def get_back(self) -> list:
        """
        Getter for the back list

        :return: list of previous page names
        """
        return self.back

    def get_forward(self) -> list:
        """
        Getter for the forward list

        :return: list of next page names
        """
        return self.forward

    def check_forward(self) -> bool:
        """
        isEmpty method for the forward list

        :return: Returns True, if there is an element to forward to
        """
        return len(self.forward) != 0

    def check_back(self) -> bool:
        """
        isEmpty method for the back list

        :return: Return True, if there is an element to back to
        """
        return len(self.back) != 0

    def add_back(self, descr: str) -> None:
        """
        Adds a window in the back list as the current back destination

        :param descr: the name of the page you want to add to the back list
        :return: None
        """
        self.back.append(descr)

    def add_forward(self, descr: str) -> None:
        """
        Adds a window in the forward list as the current forward destination

        :param descr: the name of the page you want to add to the forward list
        :return: None
        """
        self.forward.append(descr)

    def check_existing(self, name: str) -> int:
        """
        Check method for a page

        :param name: the name of the page we want to see if exists
        :return: 1 if the page is in the back list, -1 if it exists in the forward list and 0 otherwise
        """
        for i in self.back:
            if i[1] == name:
                return 1
        for i in self.forward:
            if i[1] == name:
                return -1
        return 0

    def open_existing(self, target: str, where: int) -> None:
        """
        PLEASE DON'T USE
        Moves to an already existing window

        :param target: the page of destination
        :param where: 1 if we want to move back and -1 if we want to move forward
        :return: None
        """
        if where > 0:
            if target in self.back:
                ind = self.back.index(target)
                self.back.remove(target)
                self.add_forward(self.curr)
                self.curr = target
                for page in self.back[ind + 1:]:
                    self.add_forward(page)
                    self.back.remove(page)
                self.page_change(self.curr)
        elif where < 0:
            if target in self.forward:
                ind = self.forward.index(target)
                self.forward.remove(target)
                self.add_back(self.curr)
                self.curr = target
                for page in self.back[ind + 1:]:
                    self.add_back(page)
                    self.forward.remove(page)
                self.add_back(target)

    def move_back(self) -> None:
        """
        Initiates a move to previous window action, while setting the current window as a forward destination with
        its string description

        :return: None
        """
        if self.check_back():
            self.add_forward(self.curr)
            self.curr = self.back.pop()
            self.page_change(self.curr)
        else:
            return

    def move_forward(self) -> None:
        """
        Initiates a move to next window action, while setting the current window as a back destination with its string
        description.

        :return: None
        """
        # Warning: checks if there is a window to forward to
        if self.check_forward():
            self.add_back(self.curr)
            self.curr = self.forward.pop()
            self.page_change(self.curr)
        else:
            return

    def peek_type(self, direction: bool = True) -> str:
        """
         Returns the string description of the desired destination in order to update old windows
        :param direction: true if you want to look back and false for forward 
        :return: the type of the window on the given direction
        """
        if direction:
            return self.back[0][1] if self.check_back() else ""
        else:
            return self.forward[0][1] if self.check_forward() else ""

    def clear(self) -> None:
        """
        Clears front and back lists
        :return: None
        """
        self.back = []
        self.forward = []
