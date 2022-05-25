import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from Controller import LogicController


class DeleteAthleteFrame(tk.Frame):
    def __init__(self, root: tk.Frame, controller: LogicController, return_callback: Callable[[], []],
                 cancel_activation_function: Callable[[], []]):
        self.cancel_activation_function = cancel_activation_function
        self.return_callback = return_callback
        self.root = root
        self.controller = controller
        super().__init__(root)
        self.initialize()

    def initialize(self):
        self.topFrame = tk.Frame(self, bg="#b3b3b3")
        self.topFrame.pack(fill=tk.BOTH, expand=True)
        self.titleFrame = tk.Frame(self.topFrame, bg="#b3b3b3")
        self.titleFrame.pack(fill=tk.X)
        tk.Label(self.titleFrame, text="Διαγραφή Μέλους", bg="#b3b3b3", fg="#fff", font=("Arial", 24)).pack(anchor=tk.W,
                                                                                                            side=tk.LEFT)
        self.deleteVariable = tk.StringVar()
        self.deleteVariable.set("Αναζήτηση")
        self.deleteSearch = tk.Entry(self.titleFrame, textvariable=self.deleteVariable, bg="grey")
        self.deleteSearch.bind("<FocusIn>", func=self.empty_input)
        self.deleteSearch.bind("<Return>", func=self.refresh_deleted)
        self.deleteSearch.pack(padx=25, pady=25, side=tk.RIGHT)
        self.deleteSearch.config(font=("Arial", 16))
        deleteButton = tk.Button(self.titleFrame, text="Διαγραφή Επιλεγμένων", command=self.delete_selected)
        deleteButton.pack(pady=25, padx=10, side=tk.RIGHT)
        deleteButton.config(font=("Arial", 16))

        self.treeframe = tk.Frame(self.topFrame)
        self.treeframe.pack(padx=10, pady=25, fill=tk.BOTH, expand=True)
        style = ttk.Style()
        style.configure("2.Treeview", rowheight=25, font=("Arial", 16))
        style.configure("2.Treeview.Heading", rowheight=30, font=("Arial", 18))
        tree_scroll = ttk.Scrollbar(self.treeframe)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(self.treeframe, style="2.Treeview", select=tk.EXTENDED,
                                     columns=["Όνομα", "Επώνυμο", "Κατηγορία"], yscrollcommand=tree_scroll.set)
        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Επώνυμο", anchor=tk.CENTER, width=120, minwidth=50)
        self.treeview.column("Όνομα", anchor=tk.W, width=120, minwidth=50)
        self.treeview.column("Κατηγορία", anchor=tk.W, width=120, minwidth=70)
        self.treeview.heading("#0", text='', anchor=tk.W)
        self.treeview.heading("Επώνυμο", text="Επώνυμο", anchor=tk.W)
        self.treeview.heading("Όνομα", text="Όνομα", anchor=tk.W)
        self.treeview.heading("Κατηγορία", text="Κατηγορία", anchor=tk.W)
        self.treeview.pack(anchor=tk.CENTER, expand=True, fill=tk.BOTH)
        self.refresh_deleted(0)

        tree_scroll.config(command=self.treeview.yview)

    def clear_delete_input(self):
        self.deleteVariable.set("Αναζήτηση")

    def refresh_deleted(self, value):
        if len(self.treeview.get_children()) != 0:
            for item in self.treeview.get_children():
                self.treeview.delete(item)
        count = 0
        searchResults = self.deleteVariable.get()
        data = self.controller.get_deletion_information(searchResults if searchResults != "Αναζήτηση" else None)
        for entry in data:
            self.treeview.insert(parent="", index=tk.END, iid=count, values=(
                entry["Επώνυμο"], entry["Όνομα"], entry["Κατηγορία"]))
            count += 1

    def delete_selected(self):
        temp = self.treeview.selection()
        for item in temp:
            self.controller.delete_person_entry(*self.treeview.item(item, option="values"))
        self.return_callback()

    def empty_input(self, value):
        self.deleteVariable.set("")
