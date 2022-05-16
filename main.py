import tkinter as tk

frame_page: dict(str, tk.Frame) = {}


def show(title: str) -> None:
    """
    The function to raise a specific frame that is already initialized
    :param title: the title of the frame we want to show
    """
    if not title in frame_page.keys():
        raise Exception("There is no frame with this title")
    frame_page[title].tkraise()


def main():
    root = tk.Tk()
    root.geometry("1600x900")
    root.state("zoomed")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == '__main__':
    main()
