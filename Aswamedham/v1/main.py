from tkinter import *
import constants as const
import tkinter.font as font
import main
from tkinter.ttk import *
from PIL import ImageTk, Image


# Global declaration
global root


def center_screen(win):
    window_width = win.winfo_width()
    window_height = win.winfo_height()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


def on_closing():
    exit()


def start_asking():
    a = "ss"


splash_win = Tk()
splash_win.title("Splash Screen Example")
splash_win.geometry("500x500")
splash_win.eval('tk::PlaceWindow . center')
splash_win.overrideredirect(True)
center_screen(splash_win)
bg = PhotoImage(file="splash-bg.png")
splash_label = Label(splash_win, image=bg).pack()


def mainWin():
    splash_win.destroy()
    main.root = Tk()
    main.root.title("Main Window")
    main.root.geometry("500x500")
    main.root.configure(background=const.clr_app_bg)
    main.root.eval('tk::PlaceWindow . center')
    center_screen(main.root)
    main.root.title(const.app_title)
    main.root.iconbitmap("app-icon.ico")
    main.root.protocol("WM_DELETE_WINDOW", on_closing)
    style = Style()
    # style.configure('TButton', font=('Helvetica', 10, 'bold'), foreground='white', background='grey', width=10)
    style.configure('TFrame', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970', width=10)
    main_window_elements()


def main_window_elements():
    label_font = font.Font(family='Helvetica', size=10, weight='bold')

    # banner = PhotoImage(file="banner.png")
    # splash_label1 = Label(root, text='kjhikh jhg', width=10).pack()
    frame = Frame(root)
    frame.pack(side=TOP, padx=20, pady=20)
    img = PhotoImage(file="banner.png")
    label = Label(frame, image=img).pack()

    title_lbl = Label(root, text=const.welcome_text, background='black', foreground='white', font=label_font)
    title_lbl.pack(padx=50, pady=50)

    btn_frame = Frame(root)
    btn_frame.pack(side=TOP, padx=20, pady=20)

    start_btn = Button(btn_frame, text="Start", command=start_asking)
    start_btn.grid(row=2, column=2, padx=25, pady=25)
    exit_btn = Button(btn_frame, text="Exit", command=root.quit)
    exit_btn.grid(row=2, column=4, padx=25, pady=25)

    answer_frame = Frame(root)

    var = IntVar()
    yes_btn = Button(answer_frame, text="Yes", command=lambda: var.set(1))
    yes_btn.grid(row=2, column=2, padx=25, pady=25)
    no_btn = Button(answer_frame, text="No", command=lambda: var.set(2))
    no_btn.grid(row=2, column=4, padx=25, pady=25)


splash_win.after(3000, mainWin)

mainloop()
