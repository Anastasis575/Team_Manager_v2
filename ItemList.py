import tkinter as tk

from AthleteButtonFrame import ButtonFrame
from Controller import LogicController


class ItemList(tk.Frame):
    def __init__(self, athlete_frame: ButtonFrame, poi_frame: ButtonFrame, controller: LogicController, root_window,
                 bco: str):
        """
        Constructor of the item list frame for people.

        :param athlete_frame: The frame to output the data of athletes to.
        :param poi_frame: The frame to output the data of non-athletes to.
        :param controller: the controller object.
        :param root_window: the athlete page root frame.
        :param bco: a string corresponding to the background color.
        :return: None.
        """
        self.poi_frame = poi_frame
        self.athlete_frame = athlete_frame
        self.controller = controller
        self.bco = bco
        self.items = []
        self.scrollbar = None
        super().__init__(root_window.main_athlete_canvas, bg=bco)
        self.root = root_window

    def update_list(self, category, parameter=None) -> None:
        """
        The callback to refresh the ItemList when either the category or the attribute we look for changes.

        :param category: The name of the current category.
        :param parameter: The name of the extra attribute we are searching for, if any.
        :return: None.
        """
        for i in self.winfo_children():
            i.destroy()
            self.items = []
        if category != "Επιλέξτε μια κατηγορία μέλους":
            counter = 0
            tempdata = self.controller.match_person_by_category(category, parameter)

            for match in tempdata:
                self.items.append(
                    ItemButton(self, self.controller, self.athlete_frame, self.poi_frame, match, "#b3b3b3", parameter,
                               width=100))
                self.items[-1].pack(fill=tk.X)
                counter += 1


class ItemButton(tk.Button):
    def __init__(self, root, controller: LogicController, athlete_frame: ButtonFrame, poi_frame: ButtonFrame,
                 data: dict, bgc: str, param: str = None, **kwargs):
        """
        The button that corresponds to an inspect-able person (athlete or other Person of Interest).

        :param root: the base class that created this.
        :param controller: the logic controller for the application.
        :param athlete_frame: Frame in case we are inspecting athletes.
        :param poi_frame: Frame in case we are inspecting athletes.
        :param data: a tuple for the person information(Surname, Name, Category, Param).
        :param bgc: the background color.
        :param param: extra parameter to search for
        """
        self.controller = controller
        self.athlete_frame = athlete_frame
        self.poi_frame = poi_frame
        self.root = root
        self.data = data
        self.DueChange = ""
        self.textName = self.data["Επώνυμο"] + " " + self.data["Όνομα"] + (
            "| %s" % (self.data[param]) if param is not None else "")
        super().__init__(root, text=self.textName, fg="#fff", command=self.produce_data, bg=bgc)
        super().config(font=("Arial", 18))

    def produce_data(self) -> None:
        """
        The callback to inspect the selected character.

        :return: None.
        """
        occ = self.controller.get_occupation_by_category(self.data["Κατηγορία"])
        if occ == "Αθλητής/τρια":
            self.athlete_frame.set_data(self.data)
            self.athlete_frame.tkraise()
        else:
            self.poi_frame.set_data(self.data)
            self.poi_frame.tkraise()
