import tkinter as tk
from collections.abc import Callable

from PIL import ImageTk,Image

class ClubPage(tk.Frame):
    def __init__(self,root:tk.Tk,init_athletes:Callable[[],[]],go_back:Callable[[],[]],go_forward:Callable[[],[]]):
        super().__init__(root, bg="#4e73c2")
        self.forphoto = None
        self.backphoto = None
        self.photo = None
        self.viewSalary = None
        self.editEntry = None
        self.deleteEntry = None
        self.create_entry = None
        self.go_forward = go_forward
        self.go_back = go_back
        self.init_athletes = init_athletes
        self.choose_view = None
        self.root=root
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
        self.title = tk.Label(self.headerFrame, text="Στοιχεία Συλλόγου", bg="#c1c1c1")
        self.title.config(font=("Arial", 36))
        self.title.place(relwidth=0.6, relheight=0.45, relx=0.3, rely=0)

        # Back Button
        self.backphoto = ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75, 75)))
        backButton = tk.Button(self.headerFrame, image=self.backphoto, command=self.go_back, bg="light grey", borderwidth=0)
        backButton.place(relheight=0.225, relwidth=0.05, relx=0.9, rely=0.7)

        # Forward Button
        self.forphoto = ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75, 75)))
        forwardButton = tk.Button(self.headerFrame, image=self.forphoto, command=self.go_forward, bg="light grey",
                                  borderwidth=0)
        forwardButton.place(relheight=0.225, relwidth=0.05, relx=0.95, rely=0.7)

        values = ["Επιλέξτε κάποια όψη",
                  "Οικονομικές Κινήσεις",
                  "Ταμείο Συλλόγου",
                  "Μισθοδοσίες"]
        self.Variable = tk.StringVar()
        self.Variable.set(values[0])
        self.view = tk.OptionMenu(self.headerFrame, self.Variable, *values, command=self.choose_view)
        self.view.config(font=("Arial", 18))
        self.view["menu"].config(font=("Arial", 18))
        self.view.place(relwidth=0.3, relx=0.35, relheight=0.1, rely=0.75)

        label = tk.Label(self.headerFrame, text="Από:", bg="light grey", fg="black", font=("Arial", 16))
        label.place(relwidth=0.125, relx=0.5, relheight=0.1, rely=0.5)

        options1 = ["-"]
        self.rangeA = tk.StringVar()
        self.rangeA.set(options1[0])
        self.begin_time = tk.OptionMenu(self.headerFrame, self.rangeA, *options1,
                                        command=lambda value: self.rangeA.set(value))
        self.begin_time.config(font=("Arial", 18))
        self.begin_time["menu"].config(font=("Arial", 18))
        self.begin_time.place(relwidth=0.125, relx=0.5, relheight=0.1, rely=0.6)

        label = tk.Label(self.headerFrame, text="Μέχρι:", bg="light grey", fg="black", font=("Arial", 16))
        label.place(relwidth=0.125, relx=0.35, relheight=0.1, rely=0.5)

        options2 = ["-"]
        self.rangeB = tk.StringVar()
        self.rangeB.set(options2[0])
        self.end_time = tk.OptionMenu(self.headerFrame, self.rangeB, *options2,
                                      command=lambda value: self.rangeB.set(value))
        self.end_time.config(font=("Arial", 18))
        self.end_time["menu"].config(font=("Arial", 18))
        self.end_time.place(relwidth=0.125, relx=0.35, relheight=0.1, rely=0.6)
        # Main Content frame
        self.contentFrame = tk.Frame(self.subHeaderFrame, bg="#474a48")
        self.contentFrame.place(relheight=1, relwidth=0.7, relx=0.3)
        # movements=ttk.Treeview(contentFrame)

        # Athlete creation Button
        AthleteCreation = tk.Button(self.subHeaderFrame, text="Δεδομένα\nΜελών",
                                    command=self.init_athletes,
                                    bg="#494949", fg="#fff")
        AthleteCreation.config(font=("Arial", 36))
        AthleteCreation.place(relwidth=0.25, relheight=0.2, relx=0.025, rely=0.05)
        # DEPRACATED!!!
        # languages={
        #    "January":"Ιανουάριος",
        #    "February":"Φεβρουάριος",
        #    "March":"Μάρτιος",
        #    "April":"Απρίλιος",
        #    "May":"Μάιος",
        #    "June":"Ιούνιος",
        #    "July":"Ιούλιος",
        #    "August":"Αύγουστος",
        #    "September":"Σεπτέμβριος",
        #    "October":"Οκτώβριος",
        #    "November":"Νοέμβριος",
        #    "December":"Δεκέμβριος",
        #    }
        # DropBar
        # self.dates=list(pd.date_range(pd.Timestamp.today()-pd.Timedelta(days=365),end=pd.Timestamp.today(),freq="MS"))
        # self.acronyms=[languages[i.month_name()] + " " + str(i.year) for i in self.dates]

        # self.search=ttk.Combobox(self.subHeaderFrame,value=self.acronyms,font=("Arial",18))
        # self.search.current(len(self.acronyms)-1)
        # self.search.bind("<<ComboboxSelected>>",self.chooseMonth)
        # self.search.place(relheight=0.1,relwidth=0.25,relx=0.025,rely=0.3)

        # Create Button
        self.Create = tk.Button(self.subHeaderFrame, text="Δημιουργία", command=self.create_entry, bg="#b4b8b5",
                                font=("Arial", 18))
        self.Create.place(relheight=0.1, relwidth=0.25, relx=0.025, rely=0.3)
        self.Create["state"] = tk.DISABLED
        # Delete Button
        self.Delete = tk.Button(self.subHeaderFrame, text="Διαγραφή", command=self.deleteEntry, bg="#b4b8b5",
                                font=("Arial", 18))
        self.Delete.place(relheight=0.1, relwidth=0.25, relx=0.025, rely=0.425)
        self.Delete["state"] = tk.DISABLED
        # Edit Button
        self.Edit = tk.Button(self.subHeaderFrame, text="Προβολή/Ενημέρωση", command=self.editEntry, bg="#b4b8b5",
                              font=("Arial", 18))
        self.Edit.place(relheight=0.1, relwidth=0.25, relx=0.025, rely=0.55)
        self.Edit["state"] = tk.DISABLED

        # Coach Salary Button
        self.Salary = tk.Button(self.subHeaderFrame, text="Λεπτομέρειες Μισθοδοσίας", command=self.viewSalary,
                                bg="#b4b8b5", font=("Arial", 18))
        self.Salary.place(relheight=0.1, relwidth=0.25, relx=0.025, rely=0.675)
        self.Salary["state"] = tk.DISABLED