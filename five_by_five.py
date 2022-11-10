"""_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
from math import floor
from re import compile as re_compile
from re import match
import os
from pathlib import Path
from itertools import product
from random import choice
import numpy as np
from rich.console import Console
from rich import print as rich_print
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


def set_first_word(word, orientation="horizontal"):
    """Sets the first word in the array"""
    word = word.upper()
    if orientation == "horizontal":
        for cell in range(ROWS):
            ARRAY[floor(COLS / 2)][cell] = str(word[cell])
    elif orientation == "vertical":
        for cell in range(ROWS):
            ARRAY[cell][floor(COLS / 2)] = str(word[cell])
    else:
        raise ValueError(
            "Invalid word orientation, should be 'vertical' or 'horizontal'"
        )


def add_letter(letter, pos_x, pos_y):
    """Adds a letter to the game ARRAYay

    Args:
        letter (str): Letter to be added to the game ARRAYay
        x (int): X position in ARRAYay
        y (int): Y position in ARRAYay
    """
    ARRAY[pos_x, pos_y] = letter.capitalize()


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


def find_word(word, words_dict_path) -> list:
    """Finds the words matching the given criteria in the "word" variable
    by looking into the wordsDictPath

    Args:
        word (str): _description_
        wordsDictPath (str): _description_

    Returns:
        list: with word matching critiria from "word" variable
    """
    word = word.replace("#", ".").lower()

    # rich_print(f"{word}")
    reg = re_compile(word)
    words_list = []
    with open(Path(words_dict_path), "r", encoding="UTF-8") as file:
        for line in file:
            line = line.rstrip()
            if bool(match(reg, line)) and (len(line) == len(word)):
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
    if (x_pos, y_pos) == (True, True):
        return True


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
        paths_list (_type_): _description_

    Returns:
        dict: _description_
    """
    possible_words = {}
    for path in paths_list:
        word = [ARRAY[item] for item in path]
        if word.count("#") == 1:  # should have only one free space
            possible_words["".join(word)] = path
    return possible_words


def cells_to_play() -> dict:
    """_summary_"""

    cells = list(product(range(5), range(5)))
    return {cell: step(cell) for cell in cells if step(cell)}


if __name__ == "__main__":
    console = Console()
    cls()
    ARRAY = create_array(ROWS, COLS)
    # set_first_word(start_word(5, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt"))
    set_first_word("mural")
    show_array()

    d = cells_to_play()
    # print(d)
    e = my_bad_function(d)
    # print(len(e), type(e))  # we have list with possible paths

    f = possible_words_list(e)  # we have dict with possible words and paths
    # print(possible_words_list(e))

    # here we have all words that can be played in current stage
    for key, path in f.items():
        answer = find_word(key, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt")
        if len(answer) > 0:
            print(f"{answer} - {path}")
