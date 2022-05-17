import tkinter as tk
from PIL import ImageTk, Image
from collections.abc import Callable


class MainWindowFrame(tk.Frame):
    def __init__(self, root: tk.Tk, init_athlete: Callable[[], []], init_club: Callable[[], []],
                 go_back: Callable[[], []], go_forward: Callable[[], []]) -> None:
        """
        Constructor for the main frame
        :param root: the Tk object that acts like the root of the frame
        :param init_athlete: a callback function for elevating the athlete page
        :param init_club: a callback function for elevating the club page
        :param go_back: a callback function for moving to the previous page
        :param go_forward: a callback function for moving to the next page
        """
        super().__init__(root, bg="#4e73c2")
        self.forphoto = None
        self.backphoto = None
        self.go_back = go_back
        self.go_forward = go_forward
        self.init_club = init_club
        self.init_athlete = init_athlete
        self.root = root
        self.imag: ImageTk = None
        self.imaging: ImageTk = None
        self.initialize()

    def initialize(self) -> None:
        """ Method to initialize UI
        """
        headerFrame = tk.Frame(self, bg="light grey")
        headerFrame.place(relheight=0.35, relwidth=0.8, relx=0.1, rely=0)

        subHeaderFrame = tk.Frame(self, bg="grey")
        subHeaderFrame.place(relheight=0.65, relwidth=0.8, relx=0.1, rely=0.35)

        titleFrame = tk.Frame(headerFrame, bg="white")
        titleFrame.place(relwidth=0.7, relheight=0.4, relx=0.3, rely=0)

        menuFrame = tk.Frame(subHeaderFrame, bg="#494949")
        menuFrame.place(relwidth=0.3, relheight=1, relx=0, rely=0)

        menuLabel = tk.Label(menuFrame, text="Menu", fg="#fff", bg=menuFrame["bg"])
        menuLabel.place(relwidth=1, relheight=0.3, relx=0, rely=0)
        menuLabel.config(font=("Arial Black", 42))

        athleteFrame = tk.Frame(menuFrame, bg="#3a3a3a")
        athleteFrame.place(relwidth=0.8, relx=0.1, relheight=0.2, rely=0.25)

        athleteButton = tk.Button(athleteFrame, text="Δεδομένα\nΜελών", command=self.init_athlete, bg="#494949",
                                  fg="#fff")
        athleteButton.config(font=("Arial", 38))
        athleteButton.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

        teamFrame = tk.Frame(menuFrame, bg="#3a3a3a")
        teamFrame.place(relwidth=0.8, relx=0.1, relheight=0.2, rely=0.55)

        teamButton = tk.Button(teamFrame, text="Δεδομένα\nΣυλλόγου", command=self.init_club, bg="#494949", fg="#fff")
        teamButton.config(font=("Arial", 38))
        teamButton.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

        self.imag = ImageTk.PhotoImage(Image.open("assets\\esperos.png").resize((350, 350)))  # BE CAREFUL
        logo = tk.Label(headerFrame, image=self.imag, bg="light grey")
        logo.place(relheight=1, relwidth=0.3, relx=0, rely=0)

        title = tk.Label(titleFrame, text="Team Manager:\nΈσπερος", bg="white")
        title.config(font=("Arial", 28))
        title.place(relheight=1, relwidth=1, relx=0, rely=0)

        self.imaging = ImageTk.PhotoImage(Image.open("assets\\Welcome.png").resize((1075, 662)))  # BE CAREFUL
        welcomePic = tk.Label(subHeaderFrame, image=self.imaging)
        welcomePic.place(relwidth=0.7, relheight=1, rely=0, relx=0.3)

        self.backphoto = ImageTk.PhotoImage(Image.open("assets\\back.png").resize((75, 75)))
        backButton = tk.Button(headerFrame, image=self.backphoto, command=self.go_back, bg="light grey", borderwidth=0)
        backButton.place(relheight=0.225, relwidth=0.05, relx=0.9, rely=0.7)

        self.forphoto = ImageTk.PhotoImage(Image.open("assets\\next.png").resize((75, 75)))
        forwardButton = tk.Button(headerFrame, image=self.forphoto, command=self.go_forward, bg="light grey",
                                  borderwidth=0)
        forwardButton.place(relheight=0.225, relwidth=0.05, relx=0.95, rely=0.7)
