""" Here we have all the functions for words and letters

    """
from pathlib import Path
from math import floor
from random import choice
from re import compile as re_compile
from re import match
from time import time
from functools import lru_cache
from typing import Tuple
from typing import List
from multiprocessing import Pool, cpu_count


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


@lru_cache(maxsize=269)  # Cache results indefinitely
def find_word(word_: str, words_list: List[str]) -> List[str]:
    """Finds the words matching the given criteria in the "word" variable
    by looking into the words list using binary search."""

    # Replace "#" with an empty string since we're checking prefixes
    word_ = word_.replace("#", "").lower()

    # Check if any word in the list starts with the given prefix
    return (
        [word_] if binary_search_prefix(words_list, word_) else []
    )  # Return an empty list if no match is found


def binary_search_prefix(words_list: List[str], prefix: str) -> bool:
    """Check if any word in words_list starts with the given prefix using binary search."""
    low, high = 0, len(words_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if words_list[mid].startswith(prefix):
            return True
        if words_list[mid] < prefix:
            low = mid + 1
        else:
            high = mid - 1

    return False


def process_keys_chunk(args):
    chunk, words_list, words_played_set, word_dict = args
    results = []

    for key in chunk:
        path = word_dict[key]
        answer = find_word(key, words_list)
        if answer and answer[0] not in words_played_set:
            results.append([len(answer[0]), answer, path])

    return results


def get_current_state_words(
    word_dict: dict, words_played: list, words_list: tuple
) -> list:
    """
    Executes the get_current_state_words function to retrieve the current state words based
    on a word dictionary, a list of words played, and a list of words. The function splits
    the word dictionary into multiple chunks and processes them in parallel using
    multiprocessing. It returns a flattened list of current state words.

    Args:
        word_dict (dict): A dictionary containing words as keys and their corresponding values.
        words_played (list): A list of words that have been played.
        words_list (tuple): A tuple of words to search within.

    Returns:
        list: A list of current state words.

    Example:
        ```python
        word_dict = {
            "apple": 1,
            "banana": 2,
            "cherry": 3,
            "orange": 4
        }
        words_played = ["apple", "banana"]
        words_list = ("apple", "banana", "cherry", "orange")
        result = get_current_state_words(word_dict, words_played, words_list)
        print(result)  # Output: ["cherry", "orange"]
        ```
    """
    words_played_set = set(words_played)

    # Determine number of chunks based on available CPU cores
    num_chunks = cpu_count()

    # Split word_dict.keys() into chunks
    keys = list(word_dict.keys())
    chunk_size = len(keys) // num_chunks
    chunks = [keys[i : i + chunk_size] for i in range(0, len(keys), chunk_size)]

    # Prepare arguments for multiprocessing
    args = [(chunk, words_list, words_played_set, word_dict) for chunk in chunks]

    # Use a pool of processes to execute the tasks
    with Pool() as pool:
        results_list = pool.map(process_keys_chunk, args)

    # Flatten the results and return
    return [result for sublist in results_list for result in sublist]
