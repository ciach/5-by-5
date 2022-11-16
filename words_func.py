""" Here we have all the functions for words and letters

    """
from pathlib import Path
from math import floor
from random import choice
from re import compile as re_compile
from re import match


def set_first_word(my_array, rows, cols, word_, orientation="horizontal"):
    """Sets the first word in the array"""
    word_ = word_.upper()
    if orientation == "horizontal":
        for cell in range(rows):
            my_array[floor(cols / 2)][cell] = str(word_[cell])
    elif orientation == "vertical":
        for cell in range(rows):
            my_array[cell][floor(cols / 2)] = str(word_[cell])
    else:
        raise ValueError(
            "Invalid word orientation, should be 'vertical' or 'horizontal'"
        )


def add_letter(my_array: list, letter_: str, pos_x: int, pos_y: int):
    """Adds a letter to the games array

    Args:
        letter (str): Letter to be added to the game ARRAYay
        x (int): X position in ARRAYay
        y (int): Y position in ARRAYay
    """
    my_array[pos_x, pos_y] = letter_.capitalize()
    return my_array


def start_word(lenght, words_dict_path) -> str:
    """get random word from words dictionary of given lenght
        example: print(start_word(5, "/home/cielak/Nauka/fivebyfive/sjp-20220605/slowa.txt"))
    Args:
        lenght (int): desired word lenght
        wordsDictPath (str): path to the file

    Returns:
        str: random word of given lenght from dictionary
    """
    words_list = []
    with open(Path(words_dict_path), "r", encoding="UTF-8") as file:
        words_list.extend(line for line in file if len(line) == lenght + 1)
    file.close()
    return choice(words_list)


def find_word(word_, words_dict_path) -> list:
    """Finds the words matching the given criteria in the "word" variable
    by looking into the wordsDictPath

    Args:
        word (str): _description_
        wordsDictPath (str): _description_

    Returns:
        list: with word matching critiria from "word" variable
    """
    word_ = word_.replace("#", ".").lower()

    # rich_print(f"{word}")
    reg = re_compile(word_)
    words_list = []
    with open(Path(words_dict_path), "r", encoding="UTF-8") as file:
        for line in file:
            line = line.rstrip()
            if bool(match(reg, line)) and (len(line) == len(word_)):
                words_list.append(line)
    file.close()
    return words_list


def check_user_word(user_word_: str, words_dict_path) -> bool:
    """_summary_

    Args:
        user_word (str): _description_

    Returns:
        bool: _description_
    """
    if user_word_:
        # check if the word is in the file
        with open(Path(words_dict_path), "r", encoding="UTF-8") as file:
            for line in file:
                line = line.rstrip()
                if line == user_word_:
                    file.close()
                    return True
    return False
