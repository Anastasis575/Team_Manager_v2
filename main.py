import tkinter as tk
from PIL import ImageTk, Image
import logging as log

from AthletePage import AthletePage
from Club import ClubPage
from MainWindowFrame import MainWindowFrame
import CopyPaste as c

frame_page: dict = {}


def show(title: str) -> None:
    """
    The function to raise a specific frame that is already initialized
    :param title: the title of the frame we want to show
    """
    if not title in frame_page.keys():
        log.fatal("There is no frame with the name %s", title)
        raise Exception("There is no frame with this title")
    frame_page[title].tkraise()


def main():
    log.info("we start here")
    root = tk.Tk()
    root.title("Team Manager")
    root.geometry("1600x900")
    root.state("zoomed")
    root.iconphoto(True, ImageTk.PhotoImage(Image.open("assets\\Esperos.png")))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame_page["main"] = MainWindowFrame(root, lambda: show("athletes"), lambda: show("club"), None, None)
    frame_page["main"].grid(row=0, column=0, sticky="nsew")
    frame_page["athletes"] = AthletePage(root, lambda: show("club"), None, None)
    frame_page["athletes"].grid(row=0, column=0, sticky="nsew")
    frame_page["club"] = ClubPage(root, lambda: show("athletes"), None, None)
    frame_page["club"].grid(row=0, column=0, sticky="nsew")
    show("main")
    c.make_textmenu(root)
    root.bind_class("Entry", "<Button-3><ButtonRelease-3>", c.show_textmenu)
    root.bind_class("Entry", "<Control-a>", lambda event: c.callback_select_all(event, root))
    root.bind_class("Entry", "<Control-c>", copy)
    root.bind_class("Entry", "<Control-x>", cut)
    root.bind_class("Entry", "<Control-p>", paste)
    root.protocol("WM_DELETE_WINDOW", lambda : exit_w(root))
    log.info("we debug here")
    root.mainloop()


def copy(event):
    event.widget.event_generate("<<Copy>>")


def paste(event):
    event.widget.event_generate("<<Paste>>")


def cut(event):
    event.widget.event_generate("<<Cut>>")


def exit_w(root):
    root.destroy()


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG, filename="esperos.log", filemode="w",
                    format='[%(asctime)s]:%(levelname)s-%(message)s')
    main()
