import tkinter as tk
from collections.abc import Callable
from enum import IntEnum

from Controller import LogicController
import tkinter.messagebox as mb


class Mode(IntEnum):
    UPDATE = 0
    CREATE = 1


class ButtonFrame(tk.Frame):
    def __init__(self, root: tk.Frame, controller: LogicController, cancel_activation_function: Callable[[], []],
                 occ: str):
        """
        Constructor for a blank person information page, with the needed entries for the occupation.

        :param root: The base frame to initialize this frame on.
        :param controller: the logic controller of the application
        :param cancel_activation_function: The function to run whenever this frame is brought to the surface in order to be able to return to the default activity.
        :param occ: The name  of the occupation that this page will be formatted for.
        """
        super().__init__(root)
        self.revert_function = cancel_activation_function
        self.controller = controller
        self.occ = occ
        self.initialize()

    @property
    def mode(self):
        return self.mode

    @mode.setter
    def mode(self, value: Mode):
        self.mode = value

    def initialize(self):
        self.frames = {}
        self.entries = {}
        namevar = tk.StringVar()
        namevar.set("55")
        self.nameFrame = tk.Frame(self, bg="#1b2135")
        self.nameFrame.place(relheight=0.1, relwidth=0.4, relx=0.05, rely=0.025)
        self.nameLabel = tk.Label(self.nameFrame, text="Επώνυμο", bg="#1b2135", fg="#fff")
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
        surNameFrame = tk.Frame(self, bg="#1b2135")
        surNameFrame.place(relheight=0.1, relwidth=0.4, relx=0.55, rely=0.025)
        self.surNameLabel = tk.Label(surNameFrame, text="Όνομα", bg="#1b2135", fg="#fff")
        self.surNameLabel.config(font=("Arial", 18))
        self.surNameLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        self.surNameEntry = tk.Entry(surNameFrame, textvariable=surNamevar, bg="#fff")
        self.surNameEntry.config(font=("Arial", 18))
        self.surNameEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        self.surNameEntry["state"] = tk.DISABLED
        self.frames["Όνομα"] = self.surNameEntry
        self.entries["Όνομα"] = surNamevar

        catvar = tk.StringVar()
        catvar.set("")
        self.catFrame = tk.Frame(self, bg="#1b2135")
        self.catFrame.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.15)
        self.catLabel = tk.Label(self.catFrame, text="Κατηγορία", bg="#1b2135", fg="#fff")
        self.catLabel.config(font=("Arial", 18))
        self.catLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        self.catEntry = tk.Entry(self.catFrame, textvariable=catvar, bg="#fff")
        self.catEntry.config(font=("Arial", 18))
        self.catEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        self.catEntry["state"] = tk.DISABLED
        self.frames["Κατηγορία"] = self.catEntry
        self.entries["Κατηγορία"] = catvar

        self.rest = tk.Frame(self, bg="#1b2135")
        self.rest.place(relheight=0.5, relwidth=0.9, relx=0.05, rely=0.275)
        counter = 0
        self.frames = {}
        categories = self.controller.get_person_attributes_by_occupation(self.occ)

        for cat in categories:
            if cat != "Cat" and cat != "Latest_payment" and cat != "Date_created" and cat != "State":
                tempFrame = tk.LabelFrame(self.rest, bg="#1b2135")
                tempFrame.place(relheight=0.1, relwidth=1, relx=0, rely=0 + 0.075 * counter)
                tempVar = tk.StringVar()
                tempVar.set("")
                tempLabel = tk.Label(tempFrame, text="{:20s}".format(cat), bg="#1b2135", fg="#fff", justify=tk.LEFT,
                                     anchor='w')
                tempLabel.config(font=("Arial", 14))
                tempLabel.place(relwidth=0.5, relheight=1)
                tempEntry = tk.Entry(tempFrame, textvariable=tempVar, bg="#fff")
                tempEntry.config(font=("Arial", 14))
                tempEntry.place(relwidth=0.5, relheight=1, relx=0.5)
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

    def set_data(self, data: dict):
        self.revert_function()
        self.mode = self.mode.UPDATE
        for i in data:
            self.entries[i].set(data[i])

    def enable(self):
        self.doneButton["state"] = tk.NORMAL
        self.nameEntry["state"] = tk.NORMAL
        self.surNameEntry["state"] = tk.NORMAL
        self.catEntry["state"] = tk.NORMAL
        for i in self.frames:
            self.frames[i]["state"] = tk.NORMAL

    def complete(self):
        # index = self.controller.get_person_attributes_by_occupation(self.occ)
        data = {}
        for i in self.entries:
            data[i] = self.entries[i].get()
        print(data)
        if data["Όνομα"] != "" and data["Επώνυμο"] != "" and data["Κατηγορία"] != "":
            if self.mode == Mode.CREATE:
                print("Create")
            else:
                print("Update")
            # self.data = self.data.reset_index()
            # self.data.loc[ind, "Όνομα"] = data["Όνομα"] if data["Όνομα"] != "" else "-"
            # self.data.loc[ind, "Επώνυμο"] = data["Επώνυμο"] if data["Επώνυμο"] != "" else "-"
            # index = (self.data.loc[ind, "Επώνυμο"], self.data.loc[ind, "Όνομα"])
            # self.data = self.data.set_index(["Επώνυμο", "Όνομα"])
            # for i in data:
            #     if i != "Όνομα" and i != "Επώνυμο":
            #         if i == "Μπλούζες Δωρεάν" or i == "Μπλούζες Χρεωμένες" or i == "Σύνολο για Μπλούζες" or i == "Εκρεμμότητες":
            #             self.data.loc[index, i] = int(data[i]) if data[i] != "" else 0
            #         elif i == "Ημερομηνία Δημιουργίας":
            #             self.data.loc[index, i] = pd.to_datetime(data[i]) if data[i] != "" else self.data.loc[index, i]
            #         elif i == "Όνομα" or i == "Επώνυμο":
            #             ind = self.data.index.get_loc(index[0])
            #             self.data = self.data.reset_index()
            #             self.data.loc[ind, i] = data[i] if data[i] != "" else "-"
            #             self.data = self.data.set_index(["Επώνυμο", "Όνομα"])
            #         else:
            #             self.data.loc[index, i] = data[i] if data[i] != "" else "-"
            #     if float(self.DueChange) != float(data["Εκρεμμότητες"]):
            #         self.data.loc[index, "Τελευταία Πληρωμή"] = pd.Timestamp.today()
            #         if int(data["Εκρεμμότητες"]) <= 0:
            #             self.data.loc[index, "Κατάσταση"] = 1
            #         else:
            #             self.data.loc[index, "Κατάσταση"] = 2

            # TODO: call the controller callback to save the data
        else:
            mb.showinfo("Σφάλμα", "Τα πεδία Όνομα, Επώνυμο και Κατηγορία πρέπει να έχουν τιμή")
        self.disable()

    def disable(self):
        if mb.askyesno("Έξοδος", "Θα θέλατε να αποχωρήσετε;"):
            self.endAction()
        else:
            self.nameEntry["state"] = tk.DISABLED
            self.surNameEntry["state"] = tk.DISABLED
            self.catEntry["state"] = tk.DISABLED
            for i in self.frames:
                self.frames[i]["state"] = tk.DISABLED
            self.doneButton["state"] = tk.DISABLED
