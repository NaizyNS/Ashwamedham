from _csv import writer
from collections import Counter
import pandas as pd
import constants as const
import data_provider

user_data = {
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
data = []
max_person_count = 0
found_person = False
# gender, category, dead_or_alive, country, state, district, have_last_name, first_letter, last_letter, birth_day, \
# birth_month, birth_year = ("",) * 12


def add_data_into_dataset(new_row):

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(const.dataset_file_name, 'a', newline='', encoding='utf-8') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(new_row)

        # Close the file object
        f_object.close()


def set_data():
    data_set = pd.read_csv(const.dataset_file_name)

    names = data_set[const.name_txt]
    names = list(set(names))
    names = [item for item in names if str(item) != 'nan']
    data_provider.max_person_count = len(names)

    data_provider.data = data_set.loc[(data_set[const.name_txt] != 'nan')]
    # data_provider.data = data_set.head(data_provider.max_person_count)
    df_obj = data_provider.data.select_dtypes(['object'])
    data_provider.data[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    data_provider.data[const.name_txt] = data_provider.data['name'].map(lambda x: x.replace(".", " "))
    data_provider.data[const.name_txt] = data_provider.data['name'].map(lambda x: remove_initials(x))
    data_provider.data[const.first_name_txt] = data_provider.data.apply(lambda row: get_first_name(row[const.name_txt]),
                                                                        axis=1)
    data_provider.data[const.first_name_len_txt] = data_provider.data.apply(
        lambda row: len(row[const.first_name_txt]), axis=1)
    data_provider.data[const.second_letter_txt] = data_provider.data.apply(
        lambda row: row[const.first_name_txt][1], axis=1)
    data_provider.data.birth_year = data_provider.data.birth_year.astype(int)


def get_filtered_data():
    if data_provider.max_person_count == 0:
        set_data()

    filtered_data = data_provider.data
    title_list = [const.category_txt, const.country_txt, const.birth_year_txt,
                  const.first_name_len_txt, const.second_letter_txt]
    for title in title_list:
        if user_data[title + "_list"]:
            list_items = user_data[title + "_list"]
            filtered_data = filtered_data[filtered_data[title].isin(list_items)]

    if user_data[const.first_letter_txt + "_list"]:
        list_items = user_data[const.first_letter_txt + "_list"]
        filtered_data = filtered_data[filtered_data[const.first_name_txt].str.startswith(tuple(list_items))]
    if user_data[const.last_letter_txt + "_list"]:
        list_items = user_data[const.last_letter_txt + "_list"]
        filtered_data = filtered_data[filtered_data[const.first_name_txt].str.endswith(tuple(list_items))]

    title_list = [const.gender_txt, const.category_txt, const.dead_or_alive_txt,
                  const.country_txt, const.second_letter_txt]
    for title in title_list:
        if user_data[title] != "":
            filtered_data = filtered_data.loc[(filtered_data[title] == user_data[title])]

    if user_data[const.birth_year_txt] != "":
        filtered_data = filtered_data.loc[(filtered_data[const.birth_year_txt] == int(user_data[const.birth_year_txt]))]
    if user_data[const.first_name_len_txt] != "":
        filtered_data = filtered_data.loc[(filtered_data[const.first_name_len_txt] ==
                                           int(user_data[const.first_name_len_txt]))]
    if user_data[const.first_letter_txt] != "":
        filtered_data = filtered_data[filtered_data[const.first_name_txt].str.match(user_data[const.first_letter_txt])]
    if user_data[const.last_letter_txt] != "":
        check_letter = [user_data[const.last_letter_txt]]
        filtered_data = filtered_data[filtered_data[const.first_name_txt].str.endswith(tuple(check_letter))]

    data_provider.data = filtered_data
    if len(filtered_data) == 1:
        data_provider.found_person = True
    # print("Number of Persons :" + str(len(filtered_data)))
    return filtered_data


def modify_user_data():
    while True:
        any_change = False
        for title in const.title_list:
            old_data = set(data_provider.user_data[title + "_list"])
            data_provider.user_data[title + "_list"] = old_data.intersection(set(get_values_about(title)))
            if old_data != data_provider.user_data[title + "_list"]:
                any_change = True
        if not any_change:
            break


def get_values_about(about):
    values = []
    if about == const.first_letter_txt or about == const.last_letter_txt or about == const.second_letter_txt:
        values = get_letters(about)
    else:
        values = get_unique_column_values(about)
    return values


def get_unique_column_values(column_name):
    filtered_data = get_filtered_data()
    column_values = filtered_data[column_name]
    column_values = [item for item in column_values if str(item) != 'nan']
    return get_sorted_unique(column_values)


def get_sorted_unique(values):
    if isinstance(values[0], int):
        values = list(set(values))
        values = sorted(values, reverse=False)
    else:
        values = [key for key, value in Counter(values).most_common()]
    return values


def get_letters(letter_txt):
    column_values = get_unique_column_values(const.first_name_txt)
    # index for last letter
    index = -1
    if letter_txt == const.first_letter_txt:
        index = 0
    elif letter_txt == const.second_letter_txt:
        index = 1
    values = [item[index] for item in column_values]
    return get_sorted_unique(values)


def get_first_name(name):
    split_name = name.split()
    for each_name in split_name:
        if len(each_name) != 1:
            each_name = str(each_name).strip()
            return each_name.upper()


def remove_initials(name):
    split_name = name.split()
    new_name = ''

    for item in split_name:
        if len(item) != 1:
            new_name += item + ' '

    new_name = new_name.strip()
    return new_name
