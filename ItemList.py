import tkinter as tk

from Controller import LogicController


class ItemList(tk.Frame):
    def __init__(self, controller: LogicController, root_window, bco: str):
        """
        Constructor of the item list frame for people

        :param controller: the controller object
        :param root_window: the athlete page root frame
        :param bco: a string corresponding to the background color
        """
        self.controller = controller
        self.bco = bco
        self.items = []
        self.scrollbar = None
        super().__init__(root_window.mainCanvas, bg=bco)
        self.root = root_window

    # def setScrollBar(self, obj):
    #     self.scrollbar = obj
    #
    # def disable_all(self):
    #     self.root.disableAll()
    #     if len(self.items) != 0:
    #         for item in self.items:
    #             item["state"] = tk.DISABLED
    #
    # def enable_all(self):
    #     self.root.enableAll()
    #     if len(self.items) != 0:
    #         for item in self.items:
    #             item["state"] = tk.NORMAL
    #         self.root.update(0)
    #
    def update_list(self, category, parameter=None):
        # self.data = run()
        # self.root.refresh(self.data)
        for i in self.winfo_children():
            i.destroy()
            self.items = []
        if category is not None:
            counter = 0
            tempdata = self.controller.match_person_by_category(category, parameter)

            for match in tempdata:
                self.items.append(ItemButton(self, match, self.bco, parameter, width=100))
                self.items[-1].pack(fill=tk.X)
                counter += 1
    #
    # def check(self, cat, data):
    #     if len(data) == 0:
    #         return pd.DataFrame()
    #     return data[["Έτος Γέννησης", "Σταθερό", "Κατηγορία", "Ιδιότητα", "Κινητό", "Email", "Επάγγελμα", "Χόμπυ",
    #                  "Σχέση με τον Αθλητισμό"]] if data[data["Κατηγορία"].str.match(cat)]["Ιδιότητα"].unique()[
    #                                                    0] != "Αθλητής/τρια" else data.drop(
    #         columns=["Επάγγελμα", "Χόμπυ", "Σχέση με τον Αθλητισμό"])


class ItemButton(tk.Button):
    def __init__(self, root, data: dict, bgc: str, param: str = None, **kwargs):
        self.root = root
        self.data = data
        self.DueChange = ""
        #TODO: find a way to tell the item button which layer to set
        self.textName = self.data["Επώνυμο"] + " " + self.data["Όνομα"] + \
                        ("| %s %s" % (param, self.data[param]) if param is not None else "")
        super().__init__(root, text=self.textName, fg="#fff", command=self.produce_data, bg=bgc)
        super().config(font=("Arial", 18))

    def produce_data(self):
        #TODO: Set the data on the correct frame correctly
        pass

        # # The more information window
        # self.root.disableAll()
        # self.top = tk.Toplevel(bg="#1b2135")
        # self.top.geometry("800x750")
        # self.top.resizable(True, True)
        # self.top.title(self.textName)
        # self.topFrame = tk.Frame(self.top, bg="#1b2135")
        # self.topFrame.place(relheight=1, relwidth=1, relx=0, rely=0)
        # self.frames = {}
        # self.entries = {}
        # namevar = tk.StringVar()
        # namevar.set(list(self.person.index[0])[0])
        # self.nameFrame = tk.Frame(self.topFrame, bg="#1b2135")
        # self.nameFrame.place(relheight=0.1, relwidth=0.4, relx=0.05, rely=0.025)
        # self.nameLabel = tk.Label(self.nameFrame, text="Επώνυμο", bg="#1b2135", fg="#fff")
        # self.nameLabel.config(font=("Arial", 18))
        # self.nameLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        # self.nameEntry = tk.Entry(self.nameFrame, textvariable=namevar, bg="#fff")
        # self.nameEntry.config(font=("Arial", 18))
        # self.nameEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        # self.nameEntry["state"] = tk.DISABLED
        # self.frames["Επώνυμο"] = self.nameEntry
        # self.entries["Επώνυμο"] = namevar
        #
        # surNamevar = tk.StringVar()
        # surNamevar.set(list(self.person.index[0])[1])
        # surNameFrame = tk.Frame(self.topFrame, bg="#1b2135")
        # surNameFrame.place(relheight=0.1, relwidth=0.4, relx=0.55, rely=0.025)
        # self.surNameLabel = tk.Label(surNameFrame, text="Όνομα", bg="#1b2135", fg="#fff")
        # self.surNameLabel.config(font=("Arial", 18))
        # self.surNameLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        # self.surNameEntry = tk.Entry(surNameFrame, textvariable=surNamevar, bg="#fff")
        # self.surNameEntry.config(font=("Arial", 18))
        # self.surNameEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        # self.surNameEntry["state"] = tk.DISABLED
        # self.frames["Όνομα"] = self.surNameEntry
        # self.entries["Όνομα"] = surNamevar
        #
        # categories = list(self.root.data["Κατηγορία"].unique())
        # catvar = tk.StringVar()
        # catvar.set(self.person["Κατηγορία"].iloc[0])
        # self.catFrame = tk.Frame(self.topFrame, bg="#1b2135")
        # self.catFrame.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.15)
        # self.catLabel = tk.Label(self.catFrame, text="Κατηγορία", bg="#1b2135", fg="#fff")
        # self.catLabel.config(font=("Arial", 18))
        # self.catLabel.place(relheight=0.5, relwidth=1, relx=0, rely=0)
        # self.catEntry = tk.Entry(self.catFrame, textvariable=catvar, bg="#fff")
        # self.catEntry.config(font=("Arial", 18))
        # self.catEntry.place(relheight=0.5, relwidth=1, relx=0, rely=0.5)
        # self.catEntry["state"] = tk.DISABLED
        # self.frames["Κατηγορία"] = self.catEntry
        # self.entries["Κατηγορία"] = catvar
        #
        # self.rest = tk.Frame(self.top, bg="#1b2135")
        # self.rest.place(relheight=0.5, relwidth=0.9, relx=0.05, rely=0.275)
        # counter = 0
        # self.frames = {}
        # for cat in self.person.iloc[0].index:
        #     if cat != "Κατηγορία" and cat != "Τελευταία επεξεργασία" and cat != "Τελευταία Πληρωμή" and cat != "Ημερομηνία Δημιουργίας" and cat != "Κατάσταση":
        #         tempFrame = tk.LabelFrame(self.rest, bg="#1b2135")
        #         tempFrame.place(relheight=0.1, relwidth=1, relx=0, rely=0 + 0.075 * counter)
        #         tempVar = tk.StringVar()
        #         tempVar.set(self.person[cat].iloc[0])
        #         tempLabel = tk.Label(tempFrame, text="{:20s}".format(cat), bg="#1b2135", fg="#fff", justify=tk.LEFT,
        #                              anchor='w')
        #         tempLabel.config(font=("Arial", 14))
        #         tempLabel.place(relwidth=0.5, relheight=1)
        #         tempEntry = tk.Entry(tempFrame, textvariable=tempVar, bg="#fff")
        #         tempEntry.config(font=("Arial", 14))
        #         tempEntry.place(relwidth=0.5, relheight=1, relx=0.5)
        #         tempEntry["state"] = tk.DISABLED
        #         self.frames[cat] = tempEntry
        #         self.entries[cat] = tempVar
        #         if cat == "Εκρεμμότητες":
        #             self.DueChange = self.person[cat].iloc[0]
        #         counter += 1
        #
        # temp = None
        # tempLabel = None
        # tempEntry = None
        # tempVar = None
        #
        # self.editButton = tk.Button(self.topFrame, text="Επεξεργασία", command=self.enable, font=("Arial", 16))
        # self.editButton.place(relheight=0.05, relwidth=0.35, relx=0.1, rely=0.9)
        # self.doneButton = tk.Button(self.topFrame, text="Ολοκλήρωση", command=self.complete, font=("Arial", 16))
        # self.doneButton.place(relheight=0.05, relwidth=0.35, relx=0.55, rely=0.9)
        # self.doneButton["state"] = tk.DISABLED
        #
        # self.top.protocol("WM_DELETE_WINDOW", self.endAction)
        # self.top.mainloop()

    # def updateData(self, event):
    #     try:
    #         self.data["Ημερομηνία Δημιουργίας"].loc[self.person.index] = pd.to_datetime(self.dateVar.get(),
    #                                                                                     dayfirst=True)
    #
    #         write_data(self.data)
    #         self.data = run()
    #     except Exception:
    #         print(pd.to_datetime(self.dateVar.get()))

    def endAction(self):
        self.top.destroy()
        self.root.root.redraw()

    def enable(self):
        self.doneButton["state"] = tk.NORMAL
        self.nameEntry["state"] = tk.NORMAL
        self.surNameEntry["state"] = tk.NORMAL
        self.catEntry["state"] = tk.NORMAL
        for i in self.frames:
            self.frames[i]["state"] = tk.NORMAL

    # def complete(self):
    #     index = self.person.index
    #     data = {}
    #     for i in self.entries:
    #         data[i] = self.entries[i].get()
    #     if data["Όνομα"] != "" and data["Επώνυμο"] != "" and data["Κατηγορία"] != "":
    #         ind = self.data.index.get_loc(index[0])
    #         self.data = self.data.reset_index()
    #         self.data.loc[ind, "Όνομα"] = data["Όνομα"] if data["Όνομα"] != "" else "-"
    #         self.data.loc[ind, "Επώνυμο"] = data["Επώνυμο"] if data["Επώνυμο"] != "" else "-"
    #         index = (self.data.loc[ind, "Επώνυμο"], self.data.loc[ind, "Όνομα"])
    #         self.data = self.data.set_index(["Επώνυμο", "Όνομα"])
    #         for i in data:
    #             if i != "Όνομα" and i != "Επώνυμο":
    #                 if i == "Μπλούζες Δωρεάν" or i == "Μπλούζες Χρεωμένες" or i == "Σύνολο για Μπλούζες" or i == "Εκρεμμότητες":
    #                     self.data.loc[index, i] = int(data[i]) if data[i] != "" else 0
    #                 elif i == "Ημερομηνία Δημιουργίας":
    #                     self.data.loc[index, i] = pd.to_datetime(data[i]) if data[i] != "" else self.data.loc[index, i]
    #                 elif i == "Όνομα" or i == "Επώνυμο":
    #                     ind = self.data.index.get_loc(index[0])
    #                     self.data = self.data.reset_index()
    #                     self.data.loc[ind, i] = data[i] if data[i] != "" else "-"
    #                     self.data = self.data.set_index(["Επώνυμο", "Όνομα"])
    #                 else:
    #                     self.data.loc[index, i] = data[i] if data[i] != "" else "-"
    #             if float(self.DueChange) != float(data["Εκρεμμότητες"]):
    #                 self.data.loc[index, "Τελευταία Πληρωμή"] = pd.Timestamp.today()
    #                 if int(data["Εκρεμμότητες"]) <= 0:
    #                     self.data.loc[index, "Κατάσταση"] = 1
    #                 else:
    #                     self.data.loc[index, "Κατάσταση"] = 2
    #
    #         write_data(self.data)
    #     else:
    #         mb.showinfo("Σφάλμα", "Τα πεδία Όνομα, Επώνυμο και Κατηγορία πρέπει να έχουν τιμή")
    #     self.disable()

    # def disable(self):
    #     if mb.askyesno("Έξοδος", "Θα θέλατε να αποχωρήσετε;"):
    #         self.endAction()
    #     else:
    #         self.nameEntry["state"] = tk.DISABLED
    #         self.surNameEntry["state"] = tk.DISABLED
    #         self.catEntry["state"] = tk.DISABLED
    #         for i in self.frames:
    #             self.frames[i]["state"] = tk.DISABLED
    #         self.doneButton["state"] = tk.DISABLED
    #

class ButtonFrame(tk.Frame):
    def __init__(self, root: tk.Frame, controller: LogicController, occ: str):
        super().__init__(root)
        self.controller = controller
        self.occ = occ
        self.initialize()

    def initialize(self):
        self.frames = {}
        self.entries = {}
        namevar = tk.StringVar()
        namevar.set(list(self.person.index[0])[0])
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
        catvar.set()
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
                tempVar.set(self.person[cat].iloc[0])
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

        self.editButton = tk.Button(self.topFrame, text="Επεξεργασία", command=self.enable, font=("Arial", 16))
        self.editButton.place(relheight=0.05, relwidth=0.35, relx=0.1, rely=0.9)
        self.doneButton = tk.Button(self.topFrame, text="Ολοκλήρωση", command=self.complete, font=("Arial", 16))
        self.doneButton.place(relheight=0.05, relwidth=0.35, relx=0.55, rely=0.9)
        self.doneButton["state"] = tk.DISABLED

    def set_data(self,data:dict):
        #TODO: Finish item list
        # self.controller.
        pass
