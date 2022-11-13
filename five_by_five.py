"""_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
from math import floor
from re import compile as re_compile
from re import match
from time import perf_counter
import os
from pathlib import Path
from itertools import product
from random import choice
import numpy as np
from rich.console import Console
from rich import print as rich_print
from rich.columns import Columns
from rich.panel import Panel
from core_func import my_bad_function


global ARRAY

ROWS, COLS = (5, 5)
MIN = 0
EMPTY_CHAR = "#"

# SYSTEM FUNCIONS


def cls():
    """Clear screen"""
    os.system("cls" if os.name == "nt" else "clear")


# WORDS FUNCTIONS


def set_first_word(word_, orientation="horizontal"):
    """Sets the first word in the array"""
    word_ = word_.upper()
    if orientation == "horizontal":
        for cell in range(ROWS):
            ARRAY[floor(COLS / 2)][cell] = str(word_[cell])
    elif orientation == "vertical":
        for cell in range(ROWS):
            ARRAY[cell][floor(COLS / 2)] = str(word_[cell])
    else:
        raise ValueError(
            "Invalid word orientation, should be 'vertical' or 'horizontal'"
        )


def add_letter(letter_, pos_x, pos_y):
    """Adds a letter to the game ARRAYay

    Args:
        letter (str): Letter to be added to the game ARRAYay
        x (int): X position in ARRAYay
        y (int): Y position in ARRAYay
    """
    ARRAY[pos_x, pos_y] = letter_.capitalize()


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


# CELLS FUNCTIONS


def create_array(rows, cols):
    """_summary_

    Args:
        rows (_type_): _description_
        cols (_type_): _description_

    Returns:
        _type_: _description_
    """
    char_array = np.chararray((rows, cols), unicode=True)
    char_array[:] = EMPTY_CHAR
    return char_array


def show_array():
    """Prints the array in the console"""
    for row in ARRAY:
        rich_print(row)


def cell_inside(cell) -> bool:
    """
    Checks if the cell is inside the ARRAYay based on the X, Y position

    Args:
        cellx (int): cell X position
        celly (int): cell Y position

    Returns:
        Bool: if the cell is inside the ARRAYay
    """
    cellx, celly = cell[0], cell[1]
    x_pos = (cellx >= MIN) and (cellx < ROWS)
    y_pos = (celly >= MIN) and (celly < COLS)
    return (x_pos, y_pos) == (True, True)


def cell_neighbors(cell) -> list:
    """Returns list with cells that are neighbours of the given cell"""
    # cell under investigation
    up_ = (cell[0] - 1, cell[1])
    down = (cell[0] + 1, cell[1])
    left = (cell[0], cell[1] - 1)
    right = (cell[0], cell[1] + 1)
    possible_cells = []

    if ARRAY[cell] == EMPTY_CHAR:
        if cell_inside(up_) and ARRAY[up_] != EMPTY_CHAR:
            possible_cells.append(up_)

        if cell_inside(down) and ARRAY[down] != EMPTY_CHAR:
            possible_cells.append(down)

        if cell_inside(left) and ARRAY[left] != EMPTY_CHAR:
            possible_cells.append(left)

        if cell_inside(right) and ARRAY[right] != EMPTY_CHAR:
            possible_cells.append(right)

    else:
        if cell_inside(up_):
            possible_cells.append(up_)

        if cell_inside(down):
            possible_cells.append(down)

        if cell_inside(left):
            possible_cells.append(left)

        if cell_inside(right):
            possible_cells.append(right)

    return possible_cells


def step(cell) -> list:
    """Receives a cell and returns a list with the cells that can be played"""
    steps_all = cell_neighbors(cell)

    return list(steps_all)


def possible_words_list(paths_list) -> dict:
    """_summary_

    Args:
        paths_list (list): list of lists containing posible paths indicated
        by cell position. Eg: [[(1,0), (2,0)], [(1,0), (2,0), (3, 0)]

    Returns:
        dict: possible word as key and path as item. Eg.: {'#A': [(1, 0), (2, 0)]}
    """
    possible_words = {}
    for path_ in paths_list:
        word_ = [ARRAY[item] for item in path_]
        if word_.count("#") == 1:  # should have only one free space
            possible_words["".join(word_)] = path_
    return possible_words


def cells_to_play() -> dict:
    """_summary_"""

    cells = list(product(range(5), range(5)))
    return {cell: step(cell) for cell in cells if step(cell)}


if __name__ == "__main__":
    console = Console()
    cls()
    ARRAY = create_array(ROWS, COLS)
    START_WORD = start_word(5, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt")
    # set_first_word(start_word(5, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt"))
    set_first_word(START_WORD)
    # add_letter("a", 3, 0)
    # add_letter("b", 1, 0)
    # list of words already played
    words_played = [START_WORD.strip()]
    # console.print(f"words_played: [blue]{words_played[0]}[/blue]")
    show_array()
    while True:
        start = perf_counter()
        e = my_bad_function(ARRAY, cells_to_play())
        # print(e, len(e), type(e))  # we have list with possible paths
        # inform if no path found
        if len(e) == 0:
            console.print("\nFinished! Exiting...", style="red")
            break

        f = possible_words_list(e)  # we have dict with possible words and paths

        # here we'll store all words that can be played in current stage
        # but not the ones that are already played
        current_state_words = []

        for key, path in f.items():
            answer = find_word(key, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt")
            if len(answer) > 0:
                # if any word from answer list is in words_played list
                # then this word should be removed from answer list
                # if aswer list has only one word then answer should not be add to current_state_words
                for word in answer:
                    if word in words_played:
                        answer.remove(word)
                # in this moment we do not have repeated words in answer list
                if answer:
                    current_state_words.append([len(answer[0]), answer, path])

        sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
        max_lenght = sorted_current_state_words[0][0]

        # word to play next
        next_word_list = choice(
            [x for x in sorted_current_state_words if x[0] == max_lenght]
        )
        next_word = choice(next_word_list[1])
        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(letter, position[0], position[1])
        console.print(f"\nNew word: [blue]{next_word}[/blue] {next_word_list[2]}")
        words_played.append(next_word)
        console.print(f"Words played: {words_played}.")
        end = perf_counter()
        console.print(f"It took me: {end - start:.2f} seconds to find last word.\n")
        # users = [words_played]
        user_renderables = [Panel(user, expand=True) for user in words_played]
        console.print(Columns(user_renderables))
        show_array()
