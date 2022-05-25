import tkinter as tk
import tkinter.messagebox as mb
from collections.abc import Callable

from Controller import LogicController


class CategoryEditFrame(tk.Frame):
    def __init__(self, root: tk.Frame, controller: LogicController, return_callback: Callable[[], []],
                 cancel_activation_function: Callable[[], []]):
        super().__init__(root, bg="#e2e2e2")
        self.listtbox: tk.Listbox = None
        self.return_callback = return_callback
        self.cancel_activation_function = cancel_activation_function
        self.controller = controller
        self.initialize()

    def initialize(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        self.listtbox = tk.Listbox(self)
        self.listtbox.bind('<<ListboxSelect>>', self.edit)
        self.listtbox.config(font=("Arial", 16))
        self.listtbox.grid(row=1, column=2, sticky="nsew")

        self.nameVar = tk.StringVar()
        self.nameVar.set("")

        entry = tk.Entry(self, textvariable=self.nameVar, bg="#b3b3b3")
        entry.config(font=("Arial", 16))
        entry.grid(row=0, column=3)

        my_label = tk.Label(self,
                            text="Πληκτρολογήστε το νέο όνομα της κατηγορίας, \nΚαι επιλέξτε την κατηγορία που θέλετε να "
                                 "αντικαταστήσετε", bg="#e2e2e2")
        my_label.config(font=("Arial", 16))
        my_label.grid(row=0, column=0, columnspan=3)

    def enabled(self):
        self.cancel_activation_function()
        self.tkraise()
        self.listtbox["state"] = tk.NORMAL
        self.listtbox.delete(0, "end")
        self.nameVar.set("")
        data = self.controller.get_athlete_categories_no_coach()
        for i in data:
            self.listtbox.insert("end", i)

    def edit(self, value):
        if self.nameVar.get() == "":
            mb.showwarning("Εισαγωγή Ονόματος", "Παρακαλώ πρώτα προσθέστε το όνομα και μετά επιλέξτε την κατηγορία "
                                                "που θέλετε να αντικαταστήσει")
            return
        self.listtbox["state"] = tk.DISABLED
        self.controller.rename_category(self.listtbox.get(self.listtbox.curselection()), self.nameVar.get())
        self.enabled()
