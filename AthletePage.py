import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from PIL import ImageTk, Image

import Controller
from DeleteAthleteFrame import DeleteAthleteFrame
from CategoryEditFrame import CategoryEditFrame
from ItemList import ItemList, ButtonFrame
from ProjectList import ProjectList


class AthletePage(tk.Frame):
    def __init__(self, root, controller: Controller.LogicController, init_club: Callable[[], []],
                 go_back: Callable[[], []], go_forward: Callable[[], []]):
        """
        Constructor for the athlete page
        :param root: the Tk object that acts like the root of the frame
        :param init_club: a callback function for opening the club page
        :param go_back: a callback function for going to the previous page
        :param go_forward: a callback function for going to the next page
        """
        super().__init__(root, bg="#4e73c2")
        self.listFrame: ItemList | None = None
        self.controller = controller
        self.basicFrame = None
        self.project_frame = None
        self.go_back = go_back
        self.go_forward = go_forward
        self.init_club = init_club
        self.forphoto: ImageTk = None
        self.backphoto: ImageTk = None
        self.photo = None
        self.root = root
        self.initialize()

    def initialize(self):
        """
        Initializer for the UI.

        :return: None.
        """
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
        self.createButton = tk.Button(self.subHeaderFrame, bg="#494949", text="Δημιουργία Καινούργιας \nΕγγραφής",
                                      command=self.create_person, borderwidth=0)
        self.createButton.config(font=("Arial", 16), fg="#fff")
        self.createButton.place(relwidth=0.2, relheight=0.15, relx=0.025, rely=0.27)

        # Delete button, to delete an existing entry
        self.deleteButton = tk.Button(self.subHeaderFrame, bg="#494949", text="Διαγραφή Υπάρχουσας \nΕγγραφής",
                                      command=self.delete_entry, borderwidth=0)
        self.deleteButton.config(font=("Arial", 16), fg="#fff")
        self.deleteButton.place(relwidth=0.2, relheight=0.15, relx=0.025, rely=0.45)

        # Choice box about the category of the data
        options = ["Επιλέξτε μια κατηγορία μέλους"]
        data = self.controller.get_categories_no_coach()
        for i in data:
            options.append(str(i))
        self.formVar = tk.StringVar(self.headerFrame)
        self.formVar.set(options[0])
        self.forms = tk.OptionMenu(self.headerFrame, self.formVar, *options, command=self.update_form)
        self.forms.config(font=("Arial", 18), bg="#c1c1c1")
        self.forms['menu'].config(font=("Arial", 18), bg="#c1c1c1")
        self.forms.place(relwidth=0.25, relheight=0.1, relx=0.58, rely=0.75)

        self.cat_change_button = tk.Button(self.headerFrame, text="...", bg="#494949", command=self.change_categories)
        self.cat_change_button.config(font=("Arial", 18), bg="#c1c1c1")
        self.cat_change_button.place(relwidth=0.03, relheight=0.1, relx=0.84, rely=0.75)

        # List of data options for which attribute to look for
        self.typeOptions = ["Στοιχεία"]
        attributes = self.controller.get_person_attributes(
            self.formVar.get() if self.formVar.get() != "Επιλέξτε μια κατηγορία μέλους" else None)
        for column in attributes:
            if str(column) != "Όνομα" and str(column) != "Κατηγορία" and str(column) != "Επώνυμο" \
                    and str(column) != "Τελευταία_πληρωμή" and str(column) != "Ημερομηνία_Δημιουργίας" and \
                    str(column) != "Κατάσταση":
                self.typeOptions.append(str(column.replace("_", " ")))
        self.typeVar = tk.StringVar(self.subHeaderFrame)
        self.typeVar.set(self.typeOptions[0])
        self.type = tk.OptionMenu(self.headerFrame, self.typeVar, *self.typeOptions, command=self.update_values())
        self.type.config(font=("Arial", 18), bg="#c1c1c1")
        self.type['menu'].config(font=("Arial", 18), bg="#c1c1c1")
        self.type.place(relheight=0.1, relwidth=0.25, relx=0.3, rely=0.75)
        self.type["state"] = tk.DISABLED

        # Club page creation button
        self.teamButton = tk.Button(self.subHeaderFrame, text="Δεδομένα\nΣυλόγου",
                                    command=self.init_club,
                                    bg="#494949", fg="#fff")
        self.teamButton.config(font=("Arial", 36))
        self.teamButton.place(relwidth=0.2, relheight=0.2, relx=0.025, rely=0.05)

        above_frame = tk.Frame(self.subHeaderFrame, bg="#b3b3b3")
        above_frame.place(relheight=1, relwidth=0.75, relx=0.25, rely=0)
        above_frame.rowconfigure(0, weight=1)
        above_frame.columnconfigure(0, weight=1)
        # Main data frame for objects
        self.project_frame = tk.Frame(above_frame, bg="red")
        self.project_frame.grid(row=0, column=0, sticky="nsew")

        self.basicFrame = tk.Frame(above_frame, bg="#1b2135")
        self.basicFrame.grid(row=0, column=0, sticky="nsew")
        self.main_athlete_canvas = tk.Canvas(self.basicFrame)
        self.main_athlete_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll = ttk.Scrollbar(self.basicFrame, command=self.main_athlete_canvas.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_athlete_canvas.configure(yscrollcommand=self.scroll.set)
        self.main_athlete_canvas.bind("<Configure>",
                                      lambda e: self.main_athlete_canvas.configure(
                                          scrollregion=self.main_athlete_canvas.bbox("all")))

        # Athlete info editing frame
        self.athlete_data_frame = ButtonFrame(above_frame, self.controller, self.revert, self.disable_options,
                                              "Αθλητής/τρια")
        self.athlete_data_frame.grid(row=0, column=0, sticky="nsew")

        # Non-athlete info editing frame
        self.POI_data_frame = ButtonFrame(above_frame, self.controller, self.revert, self.disable_options,
                                          "Ενδιαφερόμενος/η", )
        self.POI_data_frame.grid(row=0, column=0, sticky="nsew")

        # People entry delete frame
        self.delete_frame = DeleteAthleteFrame(above_frame, self.controller, self.revert, self.disable_options)
        self.delete_frame.grid(row=0, column=0, sticky="nsew")

        # Main person inspection frame
        self.listFrame = ItemList(self.athlete_data_frame, self.POI_data_frame, self.controller, self, "#e2e2e2")

        # self.listFrame = tk.Frame(self.mainCanvas, bg="#1b2135")
        self.main_athlete_canvas.create_window((0, 0), window=self.listFrame, anchor=tk.NW, width=1200,
                                               height=1330)  # Be Careful
        self.category_frame = CategoryEditFrame(above_frame, self.controller, self.revert, self.disable_options)
        self.category_frame.grid(row=0, column=0, sticky="nsew")

        # Responsibility inspection frame
        self.projection = ProjectList(self.controller, self.project_frame)
        self.projection.pack(expand=True, fill=tk.BOTH)
        self.project_button = tk.Button(self.subHeaderFrame, bg="#494949", fg="#fff",
                                        text="Εμφάνιση Λίστας \nΕκκρεμοτήτων", command=self.project_data, borderwidth=0)

        self.project_button.config(font=("Arial", 16))
        self.project_button.place(relwidth=0.2, relheight=0.15, relx=0.025, rely=0.62)

        self.cancel_button = tk.Button(self.subHeaderFrame, bg="#494949", fg="#fff",
                                       text="Ακύρωση", command=self.revert, borderwidth=0)
        self.cancel_button.config(font=("Arial", 16))
        self.cancel_button.place(relwidth=0.2, relheight=0.15, relx=0.025, rely=0.8)
        self.cancel_button["state"] = tk.DISABLED
        self.revert()

    def disable_options(self) -> None:
        """
        Callback to disable all other options.

        :return: None.
        """
        self.formVar.set("Επιλέξτε μια κατηγορία μέλους")
        self.typeVar.set("Στοιχεία")
        self.type["state"] = tk.DISABLED
        self.forms["state"] = tk.DISABLED
        self.cancel_button["state"] = tk.NORMAL
        self.createButton["state"] = tk.DISABLED
        self.deleteButton["state"] = tk.DISABLED
        self.project_button["state"] = tk.DISABLED

    def project_data(self):
        """
        Callback for raising the Data projection frame.

        :return: None.
        """
        self.disable_options()
        self.project_frame.tkraise()

    def update_form(self, value):
        """
        An updater callback for the attribute selection Option menu.

        :param value: an empty event parameter for the outcome of tk.OptionMenu.
        :return: None.
        """
        if self.formVar.get() != "Επιλέξτε μια κατηγορία μέλους":
            self.type["state"] = tk.NORMAL
            tempdata = self.controller.get_person_attributes(self.formVar.get())
            self.typeVar.set("")
            self.type["menu"].delete(0, 'end')
            self.type["menu"].add_command(label="Στοιχεία", command=lambda value="Στοιχεία": self.update_entry(value))
            for column in tempdata:
                if str(column) != "Όνομα" and str(column) != "Κατηγορία" and str(column) != "Επώνυμο" \
                        and str(column) != "Τελευταία_πληρωμή" and str(column) != "Ημερομηνία_Δημιουργίας" and \
                        str(column) != "Κατάσταση":
                    self.type["menu"].add_command(label=column.replace("_", " "),
                                                  command=lambda value=column: self.update_entry(
                                                      value))
            self.typeVar.set("Στοιχεία")
            if self.formVar.get() != "Επιλέξτε μια κατηγορία μέλους":
                self.listFrame.update_list(self.formVar.get(),
                                           self.typeVar.get() if self.typeVar.get() != "Στοιχεία" else None)
        else:
            for i in self.listFrame.winfo_children():
                i.destroy()
                self.listFrame.items = []
            self.type["state"] = tk.DISABLED

    def revert(self):
        """
        A callback to revert to the default screen.

        :return: None
        """
        self.update_categories()
        self.formVar.set("Επιλέξτε μια κατηγορία μέλους")
        self.typeVar.set("Στοιχεία")
        self.type["state"] = tk.DISABLED
        self.forms["state"] = tk.NORMAL
        self.cancel_button["state"] = tk.DISABLED
        self.createButton["state"] = tk.NORMAL
        self.deleteButton["state"] = tk.NORMAL
        self.project_button["state"] = tk.NORMAL
        self.delete_frame.clear_delete_input()
        self.delete_frame.refresh_deleted(0)
        self.controller.clear_categories()
        self.update_categories()
        self.update_form(0)
        self.basicFrame.tkraise()

    def update_values(self) -> None:
        """
        A callback for when we change which attribute we want to be displayed alongside the person's fulll name.

        :return: None.
        """
        if self.listFrame is not None:
            self.listFrame.update_list(self.formVar.get(),
                                       self.typeVar.get() if self.typeVar.get() != "Στοιχεία" else None)

    def update_entry(self, value):
        """
        Callback to create new options for the attribute selector type.

        :param value: value to be used.
        :return: None.
        """
        self.typeVar.set(value)
        self.update_values()

    def create_person(self):
        """
        A callback to decide the type of person you want to create.

        :return: None.
        """
        self.revert()
        self.disable_options()
        self.top = tk.Toplevel(self.root, bg="#b3b3b3")
        self.top.geometry("500x200")
        self.top.resizable(True, True)
        self.top.title("Είδος Νέου Μέλους")
        frame = tk.Frame(self.top, bg="#b3b3b3")
        frame.pack(fill=tk.BOTH, expand=True)
        label = tk.Label(frame, text="Επιλεξτε το είδος του νέου μέλους")
        label.config(font=("Arial", 18))
        label.pack(anchor=tk.CENTER)
        options = ["Αθλητής/τρια", "Προπονητικό Team", "Χορηγός", "Θεατής", "Παλαιός Αθλητής", "Παθητικό Μέλος",
                   "Γονέας"]
        self.tempvar = tk.StringVar(frame)
        self.tempvar.set("Ιδιότητα")
        self.choicebox = tk.OptionMenu(frame, self.tempvar, "Ιδιότητα", *options, command=self.create)
        self.choicebox.config(font=("Arial", 18))
        self.choicebox["menu"].config(font=("Arial", 18))
        self.choicebox.pack(anchor=tk.CENTER)
        self.top.protocol("WM_DELETE_WINDOW", lambda: self.panel_destroy)
        # self.listFrame.disableAll()
        self.top.mainloop()

    def create(self, value) -> None:
        """
        Callback to begin the creation of a new Person entry.

        :param value: The type of person we chose to create.
        :return: None.
        """
        if value != "Ιδιότητα":
            self.disable_options()
            self.panel_destroy()
            if value == "Αθλητής/τρια":
                self.athlete_data_frame.clear()
            else:
                self.POI_data_frame.clear()
                self.POI_data_frame.catvar.set(value)

    def panel_destroy(self) -> None:
        """
        A callback to destroy the new person category widget.

        :return: None.
        """
        self.revert()
        self.top.destroy()

    def delete_entry(self) -> None:
        """
        Callback to move to the person delete frame.

        :return: None.
        """
        self.disable_options()
        self.delete_frame.tkraise()

    def update_categories(self) -> None:
        """
        Callback to update viewing athletes, so that the ui is updated at all times.

        :return: None.
        """
        self.forms["menu"].delete(0, 'end')
        self.forms["menu"].add_command(label="Επιλέξτε μια κατηγορία μέλους",
                                       command=lambda value="Επιλέξτε μια κατηγορία μέλους": self.set_form(value))
        data = self.controller.get_categories_no_coach()
        for column in data:
            self.forms["menu"].add_command(label=column, command=lambda value=column: self.set_form(value))
        self.formVar.set("Επιλέξτε μια κατηγορία μέλους")

    def set_form(self, value) -> None:
        """
        Callback to return the category option menu to default and reloading callback.

        :param value: a non-used event variable from the tk command section.
        :return: None.
        """
        self.formVar.set(value)
        self.update_form(value)

    def change_categories(self) -> None:
        """
        A callback to initialize the category edit page.

        :return: None
        """
        self.category_frame.enabled()
