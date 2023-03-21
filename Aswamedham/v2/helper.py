import pandas as pd
import data_provider as dataset
import helper
import pyttsx3
import speech_recognition as sr
import constants as const

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 145)

question_number = 0


def reset_all():
    # helper.question_number, dataset.birth_day, dataset.birth_month, dataset.birth_year, \
    # dataset.max_person_count = (0,) * 5
    # dataset.gender, dataset.category, dataset.dead_or_alive, dataset.country, dataset.state, \
    # dataset.district, dataset.have_last_name, dataset.first_letter, dataset.last_letter = ("",) * 9
    helper.question_number = 0
    dataset.data = []
    dataset.max_person_count = 0
    dataset.found_person = False
    dataset.user_data = {
        const.gender_txt: "",
        const.dead_or_alive_txt: "",
        const.category_txt: "",
        const.category_txt + "_list": [],
        const.country_txt: "",
        const.country_txt + "_list": [],
        const.first_letter_txt: "",
        const.first_letter_txt + "_list": [],
        const.second_letter_txt: "",
        const.second_letter_txt + "_list": [],
        const.last_letter_txt: "",
        const.last_letter_txt + "_list": [],
        const.birth_year_txt: "",
        const.birth_year_txt + "_list": [],
        const.first_name_len_txt: "",
        const.first_name_len_txt + "_list": []
    }


def get_next_question_number():
    helper.question_number += 1
    return f"Q {helper.question_number}. "


def get_states():
    data = dataset.get_filtered_data()
    states = data['state']
    states = list(set(states))
    return states


def get_name_list():
    names = dataset.get_unique_column_values('test_name')
    non_initial_name = []

    for item in names:
        name = str(item).strip()
        split_name = name.split()
        new_name = ''

        for each_name in split_name:
            if len(each_name) != 1:
                new_name += each_name + ' '
        item = new_name.strip()
        non_initial_name.append(new_name.strip())


def sort_title_list(title_list):
    # title_list = [const.category_txt, const.country_txt, const.second_letter_txt, const.first_letter_txt,
    #               const.last_letter_txt, const.first_name_len_txt, const.birth_year_txt]
    title_order = {
        "order": [],
        "title": []
    }
    for title in title_list:
        item_count = 0
        # item = dataset.user_data[title + "_list"]
        # if not item:
        dataset.user_data[title + "_list"] = dataset.get_values_about(title)
        item_count = len(dataset.user_data[title + "_list"])
        if item_count == 1 and dataset.user_data[title] == "":
            dataset.user_data[title] == dataset.user_data[title + "_list"][0]
        if item_count != 0 and dataset.user_data[title] == "":
            title_order["order"].append(item_count)
            title_order["title"].append(title)

    df = pd.DataFrame(title_order)
    df = df.sort_values(by=['order'])
    return df["title"]
    # if len(df["title"]) >= 3:
    #     return df["title"].head(3)
    # else:
    #      return df["title"]


def get_max_questions(actual_number):
    column_values = helper.get_unique_column_values('test_number')

    while len(column_values) != 1:
        half_count = int(len(column_values) / 2)
        middle_value = column_values[half_count - 1]
        first_half = column_values[:half_count]
        second_half = column_values[-(len(column_values) - half_count):]
        column_values = first_half

        if len(column_values) == 1:
            value = column_values[0]
            question = get_next_question_number()
            if actual_number == value:
                return question_number
            else:
                column_values = second_half
        else:
            value = middle_value
            question = get_next_question_number()
            if not actual_number <= value:
                column_values = second_half

    if len(column_values) == 1:
        value = column_values[0]
        question = get_next_question_number()
        if actual_number == value:
            return question_number
        else:
            return ("Sorry, \n The person you are thinking is not in my database "
                    "\n Please think of an Indian actor and try again ")
    else:
        return (
            "Sorry, \n Some thing went wrong"
            "\n Please think of an Indian actor and try again ")


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_first_person():
    person_list = dataset.get_unique_column_values("name")
    return person_list[0]


def get_person():
    if dataset.found_person:
        person_list = dataset.get_unique_column_values("name")
        if len(person_list) == 1:
            return person_list[0]
        else:
            return ""
    else:
        return ""


def handle_listener_error():
    talk('sorry \n I did not get you \n can you say it again \n')
    # text = 'sorry \n I did not get you \n can you say it again \n'
    # thread = Thread(target=helper.talk, args=(text,))
    # thread.start()
    convert_voice_to_text()


def check_replay_ready():
    user_replay = convert_voice_to_text()

    while "ready" not in user_replay:
        talk('sorry \n I did not get you \n please say ready when you are ready \n')
        user_replay = convert_voice_to_text()

    return True


def check_voice_replay_yes():
    user_replay = convert_voice_to_text()
    condition = 's' in user_replay or 'n' in user_replay or 'o' in user_replay
    while not condition:
        user_replay = handle_wrong_replay()
        condition = 's' in user_replay or 'n' in user_replay or 'o' in user_replay

    if 's' in user_replay:
        return True
    else:
        return False


def handle_wrong_replay():
    talk('sorry \n please answer with yes or no \n')
    return convert_voice_to_text()


def convert_voice_to_text():
    command = ""
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command

    except:
        handle_listener_error()

    return command


def check_is_over():
    if question_number > 21 or get_person() != "":
        return True
    else:
        return False
