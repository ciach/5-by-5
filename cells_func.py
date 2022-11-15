"""CELLS FUNCTIONS"""
from itertools import product
from numpy import chararray
from rich import print as rich_print


def create_array(rows: int, cols: int, empty_char: str):
    """_summary_

    Args:
        rows (_type_): _description_
        cols (_type_): _description_

    Returns:
        _type_: _description_
    """
    char_array = chararray((rows, cols), unicode=True)
    char_array[:] = empty_char
    return char_array


def show_array(my_array):
    """Prints the array in the console"""
    for row in my_array:
        rich_print(row)


def cell_inside(cell: tuple) -> bool:
    """
    Checks if the cell is inside the ARRAYay based on the X, Y position

    Args:
        cellx (int): cell X position
        celly (int): cell Y position

    Returns:
        Bool: if the cell is inside the ARRAYay
    """
    rows_ = 5
    cols_ = 5
    cellx, celly = cell[0], cell[1]
    x_pos = 0 <= cellx < rows_
    y_pos = 0 <= celly < cols_
    return (x_pos, y_pos) == (True, True)


def cell_neighbors(cell: tuple, my_array: list, empty_char: str) -> list:
    """Returns list with cells that are neighbours of the given cell"""
    # cell under investigation
    up_ = (cell[0] - 1, cell[1])
    down = (cell[0] + 1, cell[1])
    left = (cell[0], cell[1] - 1)
    right = (cell[0], cell[1] + 1)
    possible_cells = []

    if my_array[cell] == empty_char:
        if cell_inside(up_) and my_array[up_] != empty_char:
            possible_cells.append(up_)

        if cell_inside(down) and my_array[down] != empty_char:
            possible_cells.append(down)

        if cell_inside(left) and my_array[left] != empty_char:
            possible_cells.append(left)

        if cell_inside(right) and my_array[right] != empty_char:
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


def step(cell: tuple, my_array: list, empty_char: str) -> list:
    """Receives a cell and returns a list with the cells that can be played"""
    steps_all = cell_neighbors(cell, my_array, empty_char)

    return list(steps_all)


def possible_words_list(paths_list: list, my_array: list) -> dict:
    """_summary_

    Args:
        paths_list (list): list of lists containing posible paths indicated
        by cell position. Eg: [[(1,0), (2,0)], [(1,0), (2,0), (3, 0)]

    Returns:
        dict: possible word as key and path as item. Eg.: {'#A': [(1, 0), (2, 0)]}
    """
    possible_words = {}
    for path_ in paths_list:
        word_ = [my_array[item] for item in path_]
        if word_.count("#") == 1:  # should have only one free space
            possible_words["".join(word_)] = path_
    return possible_words


def cells_to_play(my_array: list, empty_char: str) -> dict:
    """_summary_"""

    cells = list(product(range(5), range(5)))
    return {
        cell: step(cell, my_array, empty_char)
        for cell in cells
        if step(cell, my_array, empty_char)
    }
