import tkinter as tk
from collections.abc import Callable
from enum import IntEnum

import pandas as pd
from pandas import Timestamp

from Controller import LogicController
import tkinter.messagebox as mb


class Mode(IntEnum):
    UPDATE = 0
    CREATE = 1


class ButtonFrame(tk.Frame):
    def __init__(self, root: tk.Frame, controller: LogicController, return_callback: Callable[[], []],
                 cancel_activation_function: Callable[[], []], occ: str):
        """
        Constructor for a blank person information page, with the needed entries for the occupation.

        :param root: The base frame to initialize this frame on.
        :param controller: the logic controller of the application
        :param return_callback: Callback to revert after completion
        :param cancel_activation_function: The function to run whenever this frame is brought to the surface in order to be able to return to the default activity.
        :param occ: The name  of the occupation that this page will be formatted for.
        """
        super().__init__(root, bg="#E8E6E8")
        self.return_callback = return_callback
        self._mode = None
        self.revert_function = cancel_activation_function
        self.controller = controller
        self.occ = occ

        self.initialize()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value: Mode):
        self._mode = value

    def initialize(self) -> None:
        """
        Initializes UI.

        :return: None.
        """
        self.frames = {}
        self.entries = {}
        namevar = tk.StringVar()
        namevar.set("")
        self.nameFrame = tk.Frame(self, bg="#b3b3b3")
        self.nameFrame.place(relheight=0.1, relwidth=0.26, relx=0.05, rely=0.025)
        self.nameLabel = tk.Label(self.nameFrame, text="Επώνυμο", bg="#b3b3b3", fg="#fff")
        self.nameLabel.config(font=("Arial", 18))
        self.nameLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        self.nameEntry = tk.Entry(self.nameFrame, textvariable=namevar, bg="#fff")
        self.nameEntry.config(font=("Arial", 18))
        self.nameEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        self.nameEntry["state"] = tk.DISABLED
        self.frames["Επώνυμο"] = self.nameEntry
        self.entries["Επώνυμο"] = namevar

        surNamevar = tk.StringVar()
        surNamevar.set("")
        surNameFrame = tk.Frame(self, bg="#b3b3b3")
        surNameFrame.place(relheight=0.1, relwidth=0.26, relx=0.37, rely=0.025)
        self.surNameLabel = tk.Label(surNameFrame, text="Όνομα", bg="#b3b3b3", fg="#fff")
        self.surNameLabel.config(font=("Arial", 18))
        self.surNameLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        self.surNameEntry = tk.Entry(surNameFrame, textvariable=surNamevar, bg="#fff")
        self.surNameEntry.config(font=("Arial", 18))
        self.surNameEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        self.surNameEntry["state"] = tk.DISABLED
        self.frames["Όνομα"] = self.surNameEntry
        self.entries["Όνομα"] = surNamevar

        self.catvar = tk.StringVar()
        self.catvar.set("")
        self.catFrame = tk.Frame(self, bg="#1b2135")
        self.catFrame.place(relheight=0.1, relwidth=0.26, relx=0.68, rely=0.025)
        self.catLabel = tk.Label(self.catFrame, text="Κατηγορία", bg="#b3b3b3", fg="#fff")
        self.catLabel.config(font=("Arial", 18))
        self.catLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        self.catEntry = tk.Entry(self.catFrame, textvariable=self.catvar, bg="#fff")
        self.catEntry.config(font=("Arial", 18))
        self.catEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        self.catEntry["state"] = tk.DISABLED
        self.frames["Κατηγορία"] = self.catEntry
        self.entries["Κατηγορία"] = self.catvar

        self.rest = tk.Frame(self, bg="#e2e2e2")
        self.rest.place(relheight=0.7, relwidth=0.9, relx=0.05, rely=0.15)
        counter = 0
        self.frames = {}
        categories = self.controller.get_person_attributes_by_occupation(self.occ)

        for cat in categories:
            if cat != "Κατηγορία" and cat != "Τελευταία_πληρωμή" and cat != "Ημερομηνία_Δημιουργίας" and cat != "Κατάσταση" and cat != "Επώνυμο" and cat != "Όνομα":
                tempFrame = tk.LabelFrame(self.rest, bg="#1b2135")
                tempFrame.place(relheight=0.1, relwidth=1, relx=0, rely=0.075 * counter)
                tempVar = tk.StringVar()
                tempVar.set("")
                tempLabel = tk.Label(tempFrame, text="{:20s}".format(cat), bg="#b3b3b3", fg="#fff", justify=tk.LEFT,
                                     anchor='w')
                tempLabel.config(font=("Arial", 14))
                tempLabel.place(relwidth=0.35, relheight=1)
                tempEntry = tk.Entry(tempFrame, textvariable=tempVar, bg="#fff")
                tempEntry.config(font=("Arial", 14))
                tempEntry.place(relwidth=0.65, relheight=1, relx=0.35)
                tempEntry["state"] = tk.DISABLED
                self.frames[cat] = tempEntry
                self.entries[cat] = tempVar
                counter += 1

        temp = None
        tempLabel = None
        tempEntry = None
        tempVar = None

        self.editButton = tk.Button(self, text="Επεξεργασία", command=self.enable, font=("Arial", 16))
        self.editButton.place(relheight=0.05, relwidth=0.35, relx=0.1, rely=0.9)
        self.doneButton = tk.Button(self, text="Ολοκλήρωση", command=self.complete, font=("Arial", 16))
        self.doneButton.place(relheight=0.05, relwidth=0.35, relx=0.55, rely=0.9)
        self.doneButton["state"] = tk.DISABLED

    def set_data(self, data: dict) -> None:
        """
        Callback to adding the person data for inspection.

        :param data: The person data in a tuple.
        :return: None.
        """
        self.disable()
        self.revert_function()
        self.mode = Mode.UPDATE
        info = self.controller.get_person_info(data["Επώνυμο"], data["Όνομα"], data["Κατηγορία"])
        for i in info:
            if i != "Τελευταία_πληρωμή" and i != "Ημερομηνία_Δημιουργίας" and i != "Κατάσταση":
                self.entries[i].set(info[i])

    def enable(self) -> None:
        """
        Enabling callback for when we want to edit the person entry.

        :return: None.
        """
        self.doneButton["state"] = tk.NORMAL
        self.nameEntry["state"] = tk.NORMAL
        self.surNameEntry["state"] = tk.NORMAL
        self.catEntry["state"] = tk.NORMAL
        for i in self.frames:
            self.frames[i]["state"] = tk.NORMAL

    def complete(self) -> None:
        """
        Callback to initiate the update and insert functions.

        :return: None
        """
        # index = self.controller.get_person_attributes_by_occupation(self.occ)
        data = {}
        for i in self.entries:
            if i == "Ενεργά_χρόνια" or i == "Δωρεάν_μπλούζες" or i == "Χρεωμένες_μπλούζες":
                data[i] = int(self.entries[i].get() if self.entries[i].get() != "" else "0")
                continue
            elif i == "Ύψος" or i == "Ποσό_για_μπλούζες" or i == "Υποχρεώσεις":
                data[i] = float(self.entries[i].get() if self.entries[i].get() != "" else "0")
                continue
            data[i] = self.entries[i].get() if self.entries[i].get() != "" else "-"
        if data["Όνομα"] != "" and data["Επώνυμο"] != "" and data["Κατηγορία"] != "":
            if self.mode == Mode.CREATE:
                print("Create")
                data["Ημερομηνία_Δημιουργίας"] = Timestamp.now()
                if self.occ == "Αθλητής/τρια":
                    data["Τελευταία_πληρωμή"] = Timestamp.now()
                    data["Κατάσταση"] = 1
                self.controller.create_person_entry(data["Όνομα"], data["Επώνυμο"], self.occ,data)
            else:
                print("Update")
                if self.controller.get_occupation_by_category(data["Κατηγορία"]) == "Αθλητής/τρια":
                    if self.controller.get_person_responsibility(data["Επώνυμο"], data["Όνομα"],
                                                                 data["Υποχρεώσεις"]) > 0:
                        data["Κατάσταση"] = 2 if data["Υποχρεώσεις"] > 0 else 1
                        data["Τελευταία_πληρωμή"] = Timestamp.now()
                self.controller.update_person_info(data["Όνομα"], data["Επώνυμο"], data)

        else:
            mb.showinfo("Σφάλμα", "Τα πεδία Όνομα, Επώνυμο και Κατηγορία πρέπει να έχουν τιμή")
        self.return_callback()

    def disable(self) -> None:
        """
        Disable all entries when just viewing the target entry.

        :return:
        """
        self.nameEntry["state"] = tk.DISABLED
        self.surNameEntry["state"] = tk.DISABLED
        self.catEntry["state"] = tk.DISABLED
        for i in self.frames:
            self.frames[i]["state"] = tk.DISABLED
        self.doneButton["state"] = tk.DISABLED

    def clear(self):
        self.mode = Mode.CREATE
        self.revert_function()
        info = self.controller.get_person_attributes_by_occupation(self.occ)
        for i in info:
            if i != "Τελευταία_πληρωμή" and i != "Ημερομηνία_Δημιουργίας" and i != "Κατάσταση":
                self.entries[i].set("")
        self.enable()
        self.tkraise()
