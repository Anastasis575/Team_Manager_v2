import tkinter as tk
from collections.abc import Callable

from PIL import ImageTk, Image
import logging as log

from Controller import LogicController
from DAO import EsperosConnection
from PageManager import PageManager
from AthletePage import AthletePage
from Club import ClubPage
from MainWindowFrame import MainWindowFrame
import CopyPaste as Cp

frame_page: dict = {}


def show(title: str) -> None:
    """
    The function to raise a specific frame that is already initialized

    :param title: the title of the frame we want to show
    :return: None
    """
    if title not in frame_page.keys():
        log.fatal("There is no frame with the name %s", title)
        raise Exception("There is no frame with this title")

    frame_page[title].tkraise()


def update_manager(manager: PageManager, curr: str, title: str, page: Callable[[str], []]) -> None:
    """
    A wrapper to decide whether a page is to be initialized in the page manager or be called from there.

    :param manager: the page manager instance
    :param curr: the name of the current page
    :param title: the name of the new page
    :param page: the callback to switch to that page
    :return: None
    """
    if manager.check_existing(title) == 0:
        manager.add_back(curr)
        manager.curr = title
        page(title)
    else:
        manager.open_existing(title, manager.check_existing(title))


def copy(event):
    event.widget.event_generate("<<Copy>>")


def paste(event):
    event.widget.event_generate("<<Paste>>")


def cut(event):
    event.widget.event_generate("<<Cut>>")


def exit_w(root: tk.Tk) -> None:
    """
    On exit callback

    :param root: the main Tk object
    :param dao: the Data Application Object handler/Model
    :return: None
    """
    root.destroy()


def main() -> None:
    """
    The main function the program starts from

    :return: None
    """

    log.info("we start here")

    manager = PageManager("main", show)
    with EsperosConnection() as dao:
        controller = LogicController(dao)

        root = tk.Tk()
        root.title("Team Manager")
        root.geometry("1600x900")
        root.state("zoomed")
        root.iconphoto(True, ImageTk.PhotoImage(Image.open("assets\\Esperos.png")))
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        frame_page["main"] = MainWindowFrame(root, controller, lambda: update_manager(manager, "main", "athletes", show),
                                             lambda: update_manager(manager, "main", "club", show),
                                             manager.move_back,
                                             manager.move_forward)

        frame_page["main"].grid(row=0, column=0, sticky="nsew")
        frame_page["athletes"] = AthletePage(root, controller, lambda: update_manager(manager, "athletes", "club", show),
                                             manager.move_back,
                                             manager.move_forward)

        frame_page["athletes"].grid(row=0, column=0, sticky="nsew")

        frame_page["club"] = ClubPage(root, controller, lambda: update_manager(manager, "club", "athletes", show),
                                      manager.move_back,
                                      manager.move_forward)

        frame_page["club"].grid(row=0, column=0, sticky="nsew")

        show("main")

        Cp.make_textmenu(root)
        root.bind_class("Entry", "<Button-3><ButtonRelease-3>", Cp.show_textmenu)
        root.bind_class("Entry", "<Control-a>", lambda event: Cp.callback_select_all(event, root))
        root.bind_class("Entry", "<Control-c>", copy)
        root.bind_class("Entry", "<Control-x>", cut)
        root.bind_class("Entry", "<Control-p>", paste)
        root.protocol("WM_DELETE_WINDOW", lambda: exit_w(root))
        root.mainloop()



if __name__ == '__main__':
    log.basicConfig(level=log.INFO, filename="esperos.log", filemode="w",
                    format='[%(asctime)s]:%(levelname)s-%(message)s')
    main()
