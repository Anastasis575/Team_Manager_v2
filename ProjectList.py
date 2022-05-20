import tkinter as tk
from tkinter import ttk

import pandas as pd
from PIL import ImageTk, Image

import Controller


class ProjectList(tk.Frame):
    def __init__(self, controller: Controller.LogicController, master):
        """
        Responsibility frame information constructor

        :param controller: the logic controller for the app
        :param master: the root node
        """
        self.controller = controller
        self.master = master
        # self.data = data
        self.imag = {}
        self.top = super().__init__(master, bg="#b3b3b3")
        miniframe = tk.Frame(self, bg="#b3b3b3")
        miniframe.pack(padx=25, pady=15, anchor=tk.E, fill=tk.X)
        label = tk.Label(miniframe, text="Λίστα Οφειλών Μελών", font=("Arial", 24), fg="#fff", bg="grey")
        label.pack(padx=25, pady=15, side=tk.LEFT, anchor=tk.W)
        self.projectVariable = tk.StringVar()
        self.projectVariable.set("Αναζήτηση")
        self.projectSearch = tk.Entry(miniframe, textvariable=self.projectVariable, bg="grey")
        self.projectSearch.bind("<FocusIn>", func=lambda x: self.projectVariable.set(""));
        self.projectSearch.bind("<Return>", func=self.refresh_treeview)
        self.projectSearch.bind("<FocusOut>", func=self.refresh_treeview)
        self.projectSearch.pack(padx=20, side="right", ipady=8)
        self.projectSearch.config(font=("Arial", 16))

        self.emailButton = tk.Button(miniframe, text="Αποστολή Email", font=('Arial', 16), command=lambda: print(
            self.treeview.item(self.treeview.selection()[0], option="values")[5]))
        self.emailButton.pack(side="right")
        self.emailAllButton = tk.Button(miniframe, text="Αποστολή σε όλους", font=('Arial', 16),
                                        command=lambda: print(
                                            self.treeview.item(self.treeview.selection()[0], option="values")[5]))
        self.emailAllButton.pack(side="right", padx=10)
        self.treeframe = tk.Frame(self)
        self.treeframe.pack(padx=10, pady=25)

        tree_scroll = ttk.Scrollbar(self.treeframe)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        style = ttk.Style()
        style.configure('Treeview', rowheight=60)
        style.configure("ownstyle.Treeview", font=('Arial', 12))  # Modify the font of the body
        style.configure("ownstyle.Treeview.Heading", font=('Arial', 14, 'bold'),
                        rowheight=120)  # Modify the font of the headings
        self.treeview = ttk.Treeview(self.treeframe, style="ownstyle.Treeview", select=tk.EXTENDED,
                                     columns=["Όνομα", "Επώνυμο", "Κατηγορία", 'Σταθερό', "Κινητό", "Email",
                                              "Εκκρεμμότητες", "Ημέρες από Εξόφληση"],
                                     yscrollcommand=tree_scroll.set)
        self.treeview.column("#0", width=120, stretch=tk.NO)
        self.treeview.column("Επώνυμο", anchor=tk.CENTER, width=120, minwidth=50)
        self.treeview.column("Όνομα", anchor=tk.W, width=120, minwidth=50)
        self.treeview.column("Κατηγορία", anchor=tk.W, width=120, minwidth=70)
        self.treeview.column("Σταθερό", anchor=tk.W, width=120, minwidth=70)
        self.treeview.column("Κινητό", anchor=tk.W, width=120, minwidth=70)
        self.treeview.column("Email", anchor=tk.W, width=180, minwidth=70)
        self.treeview.column("Εκκρεμμότητες", anchor=tk.W, width=160, minwidth=70)
        self.treeview.column("Ημέρες από Εξόφληση", anchor=tk.W, width=240, minwidth=70)
        self.treeview.heading("#0", text='Κατάσταση', anchor=tk.CENTER)
        self.treeview.heading("Επώνυμο", text="Επώνυμο", anchor=tk.W)
        self.treeview.heading("Όνομα", text="Όνομα", anchor=tk.W)
        self.treeview.heading("Κατηγορία", text="Κατηγορία", anchor=tk.W)
        self.treeview.heading("Σταθερό", text="Σταθερό", anchor=tk.W)
        self.treeview.heading("Κινητό", text="Κινητό", anchor=tk.W)
        self.treeview.heading("Email", text="Email", anchor=tk.W)
        self.treeview.heading("Εκκρεμμότητες", text="Εκκρεμμότητες", anchor=tk.W)
        self.treeview.heading("Ημέρες από Εξόφληση", text="Ημέρες από Εξόφληση", anchor=tk.W)
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.refresh_treeview(0)
        tree_scroll.config(command=self.treeview.yview)

    # def email(self):
    #    print(self.treeview.selection())

    def refresh_treeview(self, value) -> None:
        """
        Refreshes the Responsibilities UI for new search results.

        :param value: not used.
        :return: None.
        """
        if len(self.treeview.get_children()) != 0:
            for item in self.treeview.get_children():
                self.treeview.delete(item)
        searchResults = self.projectVariable.get()
        if searchResults.strip() == "":
            self.projectVariable.set("Αναζήτηση")
        count = 0
        if searchResults != "Αναζήτηση":
            data = self.controller.get_responsibility_information(searchResults)
            for entry in data:
                self.imag[entry["Όνομα"] + " " + entry["Επώνυμο"]] = ImageTk.PhotoImage(
                    file="assets//state" + str(entry["Κατάσταση"]) + ".png")
                self.treeview.insert(parent='', text="", image=self.imag[entry["Όνομα"] + " " + entry["Επώνυμο"]],
                                     index=tk.END, iid=str(count), values=(
                        entry["Επώνυμο"], entry["Όνομα"], entry["Κατηγορία"], entry["Σταθερό"], entry["Κινητό"],
                        entry["Email"], entry["Εκκρεμότητες"],
                        len(pd.date_range(start=entry["Πληρωμή"], end=pd.Timestamp.today(), freq="D")) - 1))
                count += 1
        else:
            data = self.controller.get_responsibility_information()
            for entry in data:
                self.imag[entry["Όνομα"] + " " + entry["Επώνυμο"]] = ImageTk.PhotoImage(
                    file="assets//state" + str(entry["Κατάσταση"]) + ".png")
                self.treeview.insert(parent='', text="", image=self.imag[entry["Όνομα"] + " " + entry["Επώνυμο"]],
                                     index=tk.END, iid=str(count), values=(
                        entry["Επώνυμο"], entry["Όνομα"], entry["Κατηγορία"], entry["Σταθερό"], entry["Κινητό"],
                        entry["Email"], entry["Εκκρεμότητες"],
                        len(pd.date_range(start=entry["Πληρωμή"], end=pd.Timestamp.today(), freq="D")) - 1))
                count += 1
