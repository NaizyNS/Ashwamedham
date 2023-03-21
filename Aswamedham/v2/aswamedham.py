import aswamedham
import data_provider
import helper
import constants as const
import data_provider as dataset

from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
from PIL import ImageTk, Image
from threading import Thread

he_she = "he/she"
his_her = "his/her"
answer = ""
thread = Thread()


def check_voice_replay():
    replay = helper.check_voice_replay_yes()
    if replay:
        yes_btn.invoke()
    else:
        yes_btn.invoke()


def check_replay_yes():
    # thread.join()
    if var_enable_voice.get() == 1:
        aswamedham.thread = Thread(target=check_voice_replay)
        thread.start()
    yes_no_frame.wait_variable(var_yes_or_no)
    if var_yes_or_no.get() == 1:
        status_lbl["text"] = const.you_choose_yes
        return True
    else:
        status_lbl["text"] = const.you_choose_no
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
        aswamedham.he_she = "he"
        aswamedham.his_her = "his"
        return "Male"
    else:
        aswamedham.he_she = "she"
        aswamedham.his_her = "her"
        return "Female"


def ask_dead_or_alive():
    question = "alive"
    if ask_question(question, True):
        return "Alive"
    else:
        return "Dead"


def ask_about_person():
    # First ask about person's gender
    dataset.user_data[const.gender_txt] = ask_gender()

    # Then aks about the person's first name second letter, first letter, last letter and birth year.
    about_list = [const.second_letter_txt, const.first_letter_txt, const.last_letter_txt, const.first_name_len_txt]
    get_and_set_user_data(about_list)

    # Finally ask about person's country and length of first name
    about_list = [const.birth_year_txt]
    get_and_set_user_data(about_list)

    # name = dataset.get_unique_column_values(const.name_txt)


def get_and_set_user_data(about_list):
    person = helper.get_person()
    while person == "":
        got_all_values = True
        # title_list = helper.sort_title_list(title_list)
        for about in about_list:
            if dataset.user_data[about] == "":
                got_all_values = False
                if not set_user_data(about):
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


def set_user_data(about):
    value = get_data_about(about)
    if not value:
        return False
    if len(value) == 1:
        dataset.user_data[about] = value[0]
    else:
        dataset.user_data[about + "_list"] = value

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
    aswamedham.thread = Thread(target=helper.talk, args=(question,))
    thread.start()
    return check_replay_yes()


def person_not_available():
    return ask_play_again(const.user_win)


def some_thing_went_wrong():
    return ask_play_again(const.went_wrong)


def ask_play_again(text_to_show):
    text = text_to_show + "\n" + const.play_again
    title_lbl["text"] = text
    aswamedham.thread = Thread(target=helper.talk, args=(text,))
    thread.start()
    if check_replay_yes():
        helper.reset_all()
        return const.start
    else:
        return const.stop


def ask_person_name_is_correct():
    person = helper.get_first_person()
    if person != "":
        text = "The person you are thinking is " + person + "\n Am I correct?"
        title_lbl["text"] = text
        aswamedham.thread = Thread(target=helper.talk, args=(text,))
        thread.start()
        if check_replay_yes():
            return ask_play_again("")
        else:
            return person_not_available()
    else:
        return person_not_available()


def start_play():
    helper.reset_all()
    show_frame_for_play()
    ask_about_person()
    replay = ask_person_name_is_correct()
    validate_replay(replay)


def validate_replay(user_replay):
    if user_replay == "" or user_replay == const.start:
        start_play()
    else:
        on_closing()


def set_app_position(win):
    window_width = 500
    window_height = 600

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


def on_closing():
    root.destroy()
    root.quit()
    exit()


def add_new_peron():
    birth_year = birth_year_txt.get("1.0", "end-1c")
    category = category_txt.get("1.0", "end-1c")
    person_name = person_name_txt.get("1.0", "end-1c")
    country = country_txt.get("1.0", "end-1c")
    dead_or_alive = selected_dead_alive.get()
    gender = selected_gender.get()
    is_year_numeric = birth_year.isnumeric()
    if is_year_numeric and category != "" and person_name != "" and country != "" and birth_year != "" \
            and dead_or_alive != "" and gender != "":
        new_rowdata = [0, category, person_name, country, birth_year, dead_or_alive, "", gender, ""]
        data_provider.add_data_into_dataset(new_rowdata)
        status_lbl["text"] = const.person_data_added_success
        aswamedham.thread = Thread(target=helper.talk, args=(const.person_data_added_success,))
        thread.start()
    else:
        status_lbl["text"] = const.wrong_data_entered
        aswamedham.thread = Thread(target=helper.talk, args=(const.wrong_data_entered,))
        thread.start()


class SetBanner:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.banner_frame = Frame(root, relief=RIDGE)
        self.banner_frame.pack(side=TOP)

        self.banner_img = ImageTk.PhotoImage(Image.open('app-banner.png'))
        self.banner = Label(self.banner_frame, background=const.clr_app_bg)
        self.banner.image = self.banner_img  # <== this is where we anchor the img object
        self.banner.configure(image=self.banner_img)
        self.banner.pack()


def show_frame_for_play():
    # Hide Start,Stop,Voice mode buttons
    start_exit_frame.pack_forget()
    voice_enable_frame.pack_forget()
    show_create_person_frame.pack_forget()
    # Show Yes,No, Restart buttons
    yes_no_frame.pack(side=TOP, padx=20, pady=20)
    restart_frame.pack(side=TOP, padx=20, pady=20)
    status_lbl["text"] = ""


def restart():
    start_exit_frame.pack(side=TOP, padx=20, pady=20)
    voice_enable_frame.pack(side=TOP, padx=20, pady=5)
    show_create_person_frame.pack(side=TOP, padx=20, pady=15)
    yes_no_frame.pack_forget()
    restart_frame.pack_forget()
    add_person_form.pack_forget()
    add_person_btn_frame.pack_forget()
    title_lbl["text"] = const.welcome_text
    status_lbl["text"] = ""


def show_add_person_form():
    title_lbl["text"] = const.add_person_text
    add_person_form.pack(side=TOP, padx=10, pady=10)
    add_person_btn_frame.pack(side=TOP, padx=10, pady=10)
    start_exit_frame.pack_forget()
    voice_enable_frame.pack_forget()
    show_create_person_frame.pack_forget()


# UI Implementation
root = Tk()
root.title(const.app_title)
root.iconbitmap("app-icon.ico")
root.protocol("WM_DELETE_WINDOW", on_closing)
root.configure(background=const.clr_app_bg)
set_app_position(root)
SetBanner(root)

myFont = font.Font(family='Helvetica', size=10, weight='bold')
style = Style()
style.configure('TFrame', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970', width=10)
style.configure('TCheckbutton', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970')
style.configure('P.TLabel', font=('Helvetica', 10, 'bold'), foreground='white', background='#063970', justify=LEFT,
                width=15)

title_lbl = Label(root, text=const.welcome_text, justify=CENTER, background=const.clr_app_bg, foreground='white',
                  font=myFont)
title_lbl.configure(anchor="center")
title_lbl.pack(padx=40, pady=40)

# Add person form
add_person_form = Frame(root)

Label(add_person_form, text="Person Name", style='P.TLabel').grid(row=2, column=2, padx=5, pady=5)
person_name_txt = Text(add_person_form, height=1, width=30)
person_name_txt.grid(row=2, column=4, padx=5, pady=5)

Label(add_person_form, text="Birth Year", style='P.TLabel').grid(row=3, column=2, padx=5, pady=5)
birth_year_txt = Text(add_person_form, height=1, width=30)
birth_year_txt.grid(row=3, column=4, padx=5, pady=5)

Label(add_person_form, text="Category", style='P.TLabel').grid(row=4, column=2, padx=5, pady=5)
category_txt = Text(add_person_form, height=1, width=30)
category_txt.grid(row=4, column=4, padx=5, pady=5)

Label(add_person_form, text="Country", style='P.TLabel').grid(row=5, column=2, padx=5, pady=5)
country_txt = Text(add_person_form, height=1, width=30)
country_txt.grid(row=5, column=4, padx=5, pady=5)

selected_dead_alive = StringVar()
selected_dead_alive.set("Alive")
Label(add_person_form, text="Dead Or Alive", style='P.TLabel').grid(row=6, column=2, padx=5, pady=5)
dead_or_alive_txt = OptionMenu(add_person_form, selected_dead_alive, "Alive", "Alive", "Dead")
dead_or_alive_txt.config(width=35)
dead_or_alive_txt.grid(row=6, column=4, padx=5, pady=5)

selected_gender = StringVar()
selected_gender.set("Male")
Label(add_person_form, text="Gender", style='P.TLabel').grid(row=7, column=2, padx=5, pady=5)
gender_txt = OptionMenu(add_person_form, selected_gender, "Male", "Male", "Female")
gender_txt.config(width=35)
gender_txt.grid(row=7, column=4, padx=5, pady=5)

add_person_btn_frame = Frame(root)
add_person_btn = Button(add_person_btn_frame, text="Add Person", command=add_new_peron)
add_person_btn.grid(row=2, column=2, padx=55, pady=25)
cancel_btn = Button(add_person_btn_frame, text="Back", command=restart)
cancel_btn.grid(row=2, column=4, padx=55, pady=25)

# End of form

start_exit_frame = Frame(root)
start_exit_frame.pack(side=TOP, padx=20, pady=20)
start_btn = Button(start_exit_frame, text="Start", command=start_play)
start_btn.grid(row=2, column=2, padx=25, pady=25)
exit_btn = Button(start_exit_frame, text="Exit", command=on_closing)
exit_btn.grid(row=2, column=4, padx=25, pady=25)

var_yes_or_no = IntVar()
yes_no_frame = Frame(root)
yes_btn = Button(yes_no_frame, text="Yes", command=lambda: var_yes_or_no.set(1))
yes_btn.grid(row=2, column=2, padx=25, pady=25)
no_btn = Button(yes_no_frame, text="No", command=lambda: var_yes_or_no.set(2))
no_btn.grid(row=2, column=4, padx=25, pady=25)

restart_frame = Frame(root)
Button(restart_frame, text="Restart", command=restart).pack(padx=88, pady=5)

var_enable_voice = IntVar()
voice_enable_frame = Frame(root)
voice_enable_frame.pack(side=TOP, padx=20, pady=5)
Checkbutton(voice_enable_frame, text="Voice mode", variable=var_enable_voice).pack(padx=76, pady=5)

show_create_person_frame = Frame(root)
show_create_person_frame.pack(side=TOP, padx=20, pady=15)
Button(show_create_person_frame, text="Add new person", command=show_add_person_form).pack(padx=77, pady=5)

status_lbl = Label(root, text="", justify=CENTER, background='grey', foreground='orange', font=myFont, width=500)
status_lbl.configure(anchor="center")
status_lbl.pack(padx=10, pady=10, side=BOTTOM)

root.mainloop()
