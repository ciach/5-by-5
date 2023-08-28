""" Here we have all the functions for words and letters

    """
from pathlib import Path
from math import floor
from random import choice
from re import compile as re_compile
from re import match
from time import time


def calculate_score(word):
    """Calculate score for a given word."""
    return len(word) ** 2 if word.isalpha() else 0


def load_words(
    words_dict_path: str, short_words_length: int, too_long_words_length: int
) -> tuple[list, list]:
    """Reads file with words and returns two lists of words
    one with words shorter than short_words_length
    and one with words longer than too_long_words_length

    Args:
        words_dict_path (str): path to the file with words
        short_words_length (int): words shorter than this will be returned
        too_long_words_length (int): words longer than this will be returned

    Returns:
        tuple[list, list]: tuple of two lists, first with short words, second with long words
    """

    words_list_short = []
    words_list_long = []
    with open(Path(words_dict_path), "r", encoding="UTF-8") as file:
        for line in file:
            line = line.rstrip()
            if len(line) < short_words_length:
                words_list_short.append(line)
            elif short_words_length <= len(line) < too_long_words_length:
                words_list_long.append(line)
    return words_list_short, words_list_long


def set_first_word(my_array, word_, orientation="horizontal"):
    """Sets the first word in the array"""
    word_ = word_.upper()
    middle_index = floor(len(word_) / 2)
    if orientation == "horizontal":
        for cell, letter in enumerate(word_):
            my_array[middle_index][cell] = str(letter)
    elif orientation == "vertical":
        for cell, letter in enumerate(word_):
            my_array[cell][middle_index] = str(letter)
    else:
        raise ValueError(
            "Invalid word orientation, should be 'vertical' or 'horizontal'"
        )


def add_letter(my_array: list, letter_: str, pos_x: int, pos_y: int):
    """Adds a letter to the games array

    Args:
        letter_ (str): Letter to be added to the game array
        pos_x (int): X position in array
        pos_y (int): Y position in array
    """
    my_array[pos_x][pos_y] = letter_.capitalize()
    return my_array


def start_word(length: int, words_list: list) -> str:
    """Get random word from words list of given length

    Args:
        length (int): Desired word length
        words_list (list): List of words

    Returns:
        str: Random word of given length from dictionary
    """
    return choice([word for word in words_list if len(word) == length])


def find_word(word_: str, words_list: list) -> list:
    """Finds the words matching the given criteria in the "word" variable
    by looking into the words list

    Args:
        word_ (str): Word to search for
        words_list (list): List of words

    Returns:
        list: Words matching the criteria from "word" variable
    """
    word_ = word_.replace("#", ".").lower()
    reg = re_compile(word_)
    return [
        word
        for word in words_list
        if bool(match(reg, word)) and len(word) == len(word_)
    ]


def check_user_letter(user_letter_: str) -> bool:
    """Check if user input is a letter and has only one character

    Args:
        user_letter_ (str): User input

    Returns:
        bool: True if user input is a letter and has only one character
    """
    return bool(user_letter_ and user_letter_.isalpha() and len(user_letter_) == 1)


def check_user_word(user_word_: str, words_played_: list, words_list: list) -> bool:
    """Check if the user word is valid

    Args:
        user_word_ (str): User word
        words_played_ (list): List of words already played
        words_list (list): List of words

    Returns:
        bool: True if the user word is valid
    """

    # depending on a lenght of the user word, need to check if rest of the letters exist in array

    return bool(
        user_word_ and user_word_ not in words_played_ and user_word_ in words_list
    )


def get_current_state_words(
    word_dict: dict,
    words_played: list,
    words_list: list,
) -> list:
    """
    Retrieve all words that can be played in the current stage
    and exclude the ones that are already played.
    """
    current_state_words = []
    time_limit = 60  # seconds
    start_time = time()
    for key, path in word_dict.items():
        answer = find_word(key, words_list)
        if len(answer) > 0:
            if modified_answer := [word for word in answer if word not in words_played]:
                current_state_words.append([len(answer[0]), modified_answer, path])
        if time() - start_time > time_limit:
            break
    # Filter out words that have already been played
    return [word for word in current_state_words if word not in words_played]
