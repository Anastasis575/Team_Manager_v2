import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from PIL import ImageTk, Image


class AthletePage(tk.Frame):
    def __init__(self, root, init_club: Callable[[], []], go_back: Callable[[], []], go_forward: Callable[[], []]):
        """
        Constructor for the athlete page
        :param root: the Tk object that acts like the root of the frame
        :param init_club: a callback function for opening the club page
        :param go_back: a callback function for going to the previous page
        :param go_forward: a callback function for going to the next page
        """
        super().__init__(root, bg="#4e73c2")
        self.projectData = None
        self.deleteEntry = None
        self.go_back = go_back
        self.go_forward = go_forward
        self.init_club = init_club
        self.forphoto: ImageTk = None
        self.backphoto: ImageTk = None
        self.createEntry = None
        self.photo = None
        self.root = root
        self.initialize()

    def initialize(self):
        # Two basic operational frames
        self.headerFrame = tk.Frame(self, bg="light grey")
        self.headerFrame.place(relwidth=0.8, relheight=0.35, relx=0.1, rely=0)

        self.subHeaderFrame = tk.Frame(self, bg="grey")
        self.subHeaderFrame.place(relwidth=0.8, relheight=0.65, relx=0.1, rely=0.35)

        # Esperos Emblem
        self.photo = ImageTk.PhotoImage(Image.open("assets\\Esperos.png").resize((350, 350)))  # Be Careful
        self.logo = tk.Label(self.headerFrame, image=self.photo, bg="light grey")
        self.logo.place(relheight=1, relwidth=0.3, relx=0, rely=0)

        # Window Title
        self.title = tk.Label(self.headerFrame, text="Στοιχεία Μελών", bg="#c1c1c1")
        self.title.config(font=("Arial", 36))
        self.title.place(relwidth=0.6, relheight=0.45, relx=0.3, rely=0)

        # Back Button
        self.backphoto = ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75, 75)))
        self.backButton = tk.Button(self.headerFrame, image=self.backphoto, command=self.go_back, bg="light grey",
                                    borderwidth=0)
        self.backButton.place(relheight=0.225, relwidth=0.05, relx=0.9, rely=0.7)

        # Forward Button
        self.forphoto = ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75, 75)))
        self.forwardButton = tk.Button(self.headerFrame, image=self.forphoto, command=self.go_forward, bg="light grey",
                                       borderwidth=0)
        self.forwardButton.place(relheight=0.225, relwidth=0.05, relx=0.95, rely=0.7)

        # Create button, to create a new entry
        self.createButton = tk.Button(self.headerFrame, bg="#c1c1c1", text="Δημιουργία Καινούργιας Εγγραφής",
                                      command=self.createEntry, borderwidth=0)
        self.createButton.config(font=("Arial", 16))
        self.createButton.place(relheight=0.15, relwidth=0.25, relx=0.3, rely=0.5)

        # Delete button, to delete an existing entry
        self.deleteButton = tk.Button(self.headerFrame, bg="#c1c1c1", text="Διαγραφή Υπάρχουσας Εγγραφής",
                                      command=self.deleteEntry, borderwidth=0)
        self.deleteButton.config(font=("Arial", 16))
        self.deleteButton.place(relheight=0.15, relwidth=0.25, relx=0.3, rely=0.7)

        # # Choice box about the category of the data
        # options = ["Επιλέξτε μια κατηγορία μέλους"]
        # for i in self.data["Κατηγορία"].unique():
        #     options.append(str(i))
        # self.formVar = tk.StringVar(self.headerFrame)
        # self.formVar.set(options[0])
        # self.forms = tk.OptionMenu(self.headerFrame, self.formVar, *options, command=self.updateForm)
        # self.forms.config(font=("Arial", 18), bg="#c1c1c1")
        # self.forms['menu'].config(font=("Arial", 18), bg="#c1c1c1")
        # self.forms.place(relwidth=0.25, relheight=0.1, relx=0.58, rely=0.75)

        # List of data options
        # self.typeOptions = ["Στοιχεία"]
        # for i in self.data.dropna(axis=1).columns:
        #     if str(i) != "Τελευταία επεξεργασία" and str(i) != "Τελευταία Πληρωμή" and str(
        #             i) != "Ημερομηνία Δημιουργίας" and str(i) != "Κατάσταση":
        #         self.typeOptions.append(str(i))
        # self.typeVar = tk.StringVar(self.subHeaderFrame)
        # self.typeVar.set(self.typeOptions[0])
        # self.type = tk.OptionMenu(self.subHeaderFrame, self.typeVar, *self.typeOptions, command=self.update)
        # self.type.config(font=("Arial", 24), bg="#494949", fg="#fff")
        # self.type['menu'].config(font=("Arial", 18), bg="#494949")
        # self.type.place(relwidth=0.25, relheight=0.15, relx=0.025, rely=0.27)
        # self.type["state"] = tk.DISABLED

        # Club page creation button
        self.teamButton = tk.Button(self.subHeaderFrame, text="Δεδομένα\nΣυλόγου",
                                    command=self.init_club,
                                    bg="#494949", fg="#fff")
        self.teamButton.config(font=("Arial", 36))
        self.teamButton.place(relwidth=0.25, relheight=0.2, relx=0.025, rely=0.05)

        # Main data frame for objects
        basicFrame = tk.Frame(self.subHeaderFrame, bg="#1b2135")
        basicFrame.place(relheight=1, relwidth=0.7, relx=0.3, rely=0)
        self.mainCanvas = tk.Canvas(basicFrame)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll = ttk.Scrollbar(basicFrame, command=self.mainCanvas.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.mainCanvas.configure(yscrollcommand=self.scroll.set)
        self.mainCanvas.bind("<Configure>",
                             lambda e: self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox("all")))
        # self.listFrame = ItemList(self, self.data, "#1b2135")
        # self.mainCanvas.create_window((0, 0), window=self.listFrame, anchor=tk.NW, width=1060,
        #                               height=1330)  # Be Careful

        self.ProjectButton = tk.Button(self.subHeaderFrame, bg="#494949", fg="#fff",
                                       text="Εμφάνιση Λίστας Εκκρεμοτήττων", command=self.projectData, borderwidth=0)
        self.ProjectButton.config(font=("Arial", 16))
        self.ProjectButton.place(relwidth=0.25, relheight=0.15, relx=0.025, rely=0.45)
