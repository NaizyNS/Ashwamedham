import ask
import constants as const
import data_provider
import data_provider as dataset
import helper
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
from PIL import ImageTk, Image
from threading import Thread

he_she = "he/she"
his_her = "his/her"
answer = ""


def check_replay_yes():
    if enable_voice.get() == 1:
        helper.check_voice_replay_yes()
    answer_frame.wait_variable(var)
    if var.get() == 1:
        return True
    else:
        return False


def ask_about(about):
    if about == const.gender_txt:
        return ask_gender()
    elif about == const.dead_or_alive_txt:
        return ask_dead_or_alive()
    elif about == const.have_last_name_txt:
        return ask_have_last_name()
    else:
        return ask_recursive(about)


def ask_ready():
    helper.reset_all()
    title_lbl["text"] = const.welcome
    helper.talk(const.welcome)
    return helper.check_replay_ready()


def ask_have_last_name():
    question = "Do " + he_she + " have a first name and  last name other than initial"
    title_lbl["text"] = question
    helper.talk(question)
    if check_replay_yes():
        return const.yes
    else:
        return const.no


def ask_gender():
    question = "Are you thinking of a male"
    if ask_question(question, False):
        ask.he_she = "he"
        ask.his_her = "his"
        return "Male"
    else:
        ask.he_she = "she"
        ask.his_her = "her"
        return "Female"


def ask_dead_or_alive():
    question = "alive"
    if ask_question(question, True):
        return "Alive"
    else:
        return "Dead"


def ask_about_person():
    dataset.user_data[const.gender_txt] = ask_gender()
    title_list = [const.second_letter_txt, const.first_letter_txt, const.last_letter_txt,
                  const.birth_year_txt]
    get_and_set_user_data(title_list)

    title_list = [const.country_txt, const.first_name_len_txt]
    get_and_set_user_data(title_list)

    name = data_provider.get_unique_column_values(const.name_txt)

    return ask_person()


def get_and_set_user_data(title_list):
    person = helper.get_person()
    while person == "":
        got_all_values = True
        # title_list = helper.sort_title_list(title_list)
        for title in title_list:
            if dataset.user_data[title] == "":
                got_all_values = False
                if not set_user_data(title):
                    return person_not_available()
            person = helper.get_person()
            if person != "":
                break

        if got_all_values:
            break
    if person == "":
        return False
    else:
        return True


def set_user_data(title):
    value = get_data_about(title)
    if not value:
        return False
    if len(value) == 1:
        dataset.user_data[title] = value[0]
    else:
        dataset.user_data[title + "_list"] = value

    dataset.modify_user_data()
    return True


def get_data_about(about):
    column_values = dataset.get_values_about(about)

    if len(column_values) == 0:
        return person_not_available()

    is_numeric = isinstance(column_values[0], int)
    if len(column_values) != 1:
        half_count = int(len(column_values) / 2)
        middle_value = column_values[half_count - 1]
        first_half = column_values[:half_count]
        second_half = column_values[-(len(column_values) - half_count):]
        column_values = first_half
        if len(column_values) == 1:
            value = str(column_values[0])
            question = get_question(about, value)
            if ask_question(question, True):
                return column_values
            else:
                return second_half
        else:
            if is_numeric:
                value = str(middle_value)
            else:
                # value = "\n".join(column_values)
                value = ','.join(map(str, column_values))
            question = get_question(about + 's', value)
            if not ask_question(question, True):
                column_values = second_half
            return column_values
    else:
        value = str(column_values[0])
        question = get_question(about, value)
        if ask_question(question, True):
            return column_values
        else:
            return []


def is_answered():
    if answer != "":
        return True
    return False


def ask_recursive(about):
    column_values = dataset.get_values_about(about)

    if len(column_values) == 0:
        return person_not_available()

    is_numeric = isinstance(column_values[0], int)
    while len(column_values) != 1:
        half_count = int(len(column_values) / 2)
        middle_value = column_values[half_count - 1]
        first_half = column_values[:half_count]
        second_half = column_values[-(len(column_values) - half_count):]
        column_values = first_half
        if len(column_values) == 1:
            value = str(column_values[0])
            question = get_question(about, value)
            if ask_question(question, True):
                return value
            else:
                column_values = second_half
        else:
            if is_numeric:
                value = str(middle_value)
            else:
                value = "\n".join(column_values)
            question = get_question(about + 's', value)
            if not ask_question(question, True):
                column_values = second_half

    if len(column_values) == 1:
        value = str(column_values[0])
        question = get_question(about, value)
        if ask_question(question, True):
            return value
        else:
            return person_not_available()

    else:
        return some_thing_went_wrong()


def get_question(about, value):
    switcher = {
        const.first_letter_txt: " first name start with the letter ",
        const.first_letter_txt + 's': " first name start with any of the following letters \n",
        const.second_letter_txt: " first name second letter is ",
        const.second_letter_txt + 's': " first name second letter is any of the following \n",
        const.first_name_len_txt: " first name letters count is ",
        const.first_name_len_txt + 's': " first name letters count is below or equal to ",
        const.last_letter_txt: " first name ends with the letter ",
        const.last_letter_txt + 's': " first name ends with any of the following letters \n",
        const.category_txt: " belong to the category ",
        const.category_txt + 's': " belong to any of the following category \n",
        const.country_txt: " born in the country ",
        const.country_txt + 's': " born in any of the following countries \n",
        const.state_txt: " born in the state ",
        const.state_txt + 's': " born in any of the following states \n",
        const.district_txt: " born in the district ",
        const.district_txt + 's': " born in any of the following districts \n",
        const.birth_year_txt: " born in the year ",
        const.birth_year_txt + 's': " born in the year or before the year ",
    }
    question = switcher.get(about, "") + str(value)
    return question


def ask_question(question, is_person):
    extra_str = " "
    if is_person:
        if question.startswith(' first name'):
            extra_str = " Does " + his_her + extra_str
        else:
            extra_str = " Is " + he_she + extra_str

    question = extra_str + question
    full_question = helper.get_next_question_number() + question
    title_lbl["text"] = full_question
    # thread = Thread(target=helper.talk, args=(question,))
    # thread.start()
    return check_replay_yes()


def person_not_available():
    title_lbl["text"] = const.not_available
    helper.talk(const.not_available)
    return ask_play_again()


def some_thing_went_wrong():
    title_lbl["text"] = const.went_wrong
    helper.talk(const.went_wrong)
    return ask_play_again()


def ask_play_again():
    title_lbl["text"] = const.play_again
    helper.talk(const.play_again)
    if check_replay_yes():
        helper.reset_all()
        return const.start
    else:
        return const.stop


def ask_person():
    person = helper.get_person()
    if person != "":
        text = "The person you are thinking is " + person + "\n Am I correct?"
        title_lbl["text"] = text
        helper.talk(text)
        if check_replay_yes():
            return ask_play_again()
        else:
            return person_not_available()
    else:
        return person_not_available()


def show_answer_frame():
    btn_frame.pack_forget()
    voice_enable_frame.pack_forget()
    answer_frame.pack(side=TOP, padx=20, pady=20)


def start_asking():
    show_answer_frame()
    replay = ask_about_person()
    validate_replay(replay)


def validate_replay(user_replay):
    if helper.check_is_over():
        user_replay = ask.ask_person()

    if user_replay == "" or user_replay == const.start:
        start_asking()
    elif user_replay == const.stop:
        on_closing()


def set_answer_yes():
    ask.answer = "yes"


def center_screen(win):
    window_width = 500
    window_height = 500

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


def on_closing():
    root.destroy()
    root.quit
    exit()


class GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        # status bar
        self.bar = Frame(root, relief=RIDGE)
        self.bar.pack(side=TOP)

        self.iconPath = 'app-banner.png'
        self.icon = ImageTk.PhotoImage(Image.open(self.iconPath))
        self.icon_size = Label(self.bar, background=const.clr_app_bg)
        self.icon_size.image = self.icon  # <== this is where we anchor the img object
        self.icon_size.configure(image=self.icon)
        self.icon_size.pack()


root = Tk()
root.title(const.app_title)
root.iconbitmap("app-icon.ico")
root.geometry("700x300")
root.protocol("WM_DELETE_WINDOW", on_closing)
center_screen(root)
app = GUI(root)
myFont = font.Font(family='Helvetica', size=10, weight='bold')
style = Style()
# style.configure('TButton', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970', width=10)
style.configure('TFrame', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970', width=10)
style.configure('TCheckbutton', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970')
root.configure(background=const.clr_app_bg)
var = IntVar()
title_lbl = Label(root, text=const.welcome_text, justify=CENTER, background=const.clr_app_bg, foreground='white',
                  font=myFont)
title_lbl.configure(anchor="center")
title_lbl.pack(padx=50, pady=50)

btn_frame = Frame(root)
btn_frame.pack(side=TOP, padx=20, pady=20)

start_btn = Button(btn_frame, text="Start", command=start_asking)
start_btn.grid(row=2, column=2, padx=25, pady=25)
exit_btn = Button(btn_frame, text="Exit", command=on_closing)
exit_btn.grid(row=2, column=4, padx=25, pady=25)

voice_enable_frame = Frame(root)
voice_enable_frame.pack(side=TOP, padx=20, pady=20)
enable_voice = IntVar()
Checkbutton(voice_enable_frame, text="Voice mode", variable=enable_voice).pack(padx=76, pady=5)

answer_frame = Frame(root)

yes_btn = Button(answer_frame, text="Yes", command=lambda: var.set(1))
yes_btn.grid(row=2, column=2, padx=25, pady=25)
no_btn = Button(answer_frame, text="No", command=lambda: var.set(2))
no_btn.grid(row=2, column=4, padx=25, pady=25)

root.mainloop()
