"""CELLS FUNCTIONS"""
from itertools import product
from numpy import chararray
from rich.console import Console
from rich.table import Table
from rich.box import MINIMAL_DOUBLE_HEAD
from typing import List, Tuple


def create_array(rows: int, cols: int, empty_char: str) -> chararray:
    """Create a 2D numpy chararray with the given dimensions and fill it with a specified character.

    Args:
        rows (int): The number of rows in the array.
        cols (int): The number of columns in the array.
        empty_char (str): The character to fill the array with.

    Returns:
        chararray: A 2D numpy chararray filled with the specified character.
    """
    char_array = chararray((rows, cols), unicode=True)
    char_array[:] = empty_char
    return char_array


def show_array(my_array, console: Console = None):
    """Prints the array in the console as a table.

    Args:
        my_array (List[List[str]]): A 2D array to be printed as a table.
        console (Console, optional): A Console instance for output.
                    Defaults to None, which creates a new Console instance.
    """
    if console is None:
        console = Console()

    table = Table(show_header=False, header_style="none", box=MINIMAL_DOUBLE_HEAD)

    # Add columns
    for i in range(len(my_array[0])):
        table.add_column(f"Column {i + 1}", style="white")

    # Add rows
    for row in my_array:
        table.add_row(*row)

    # Print table
    console.print(table)


def cell_inside(cell: tuple, rows_: int = 5, cols_: int = 5) -> bool:
    """
    Checks if the cell is inside the array based on the X, Y position.

    Args:
        cell (tuple): A tuple containing the X and Y positions of the cell (cellx, celly).
        rows_ (int, optional): The number of rows in the array. Defaults to 5.
        cols_ (int, optional): The number of columns in the array. Defaults to 5.

    Returns:
        bool: True if the cell is inside the array, False otherwise.
    """
    cellx, celly = cell
    x_pos = 0 <= cellx < rows_
    y_pos = 0 <= celly < cols_
    return x_pos and y_pos


def cell_neighbors(
    cell: Tuple[int, int], my_array: List[List[str]], empty_char: str
) -> List[Tuple[int, int]]:
    """Returns a list of neighboring cells for the given cell in the 2D array.

    Args:
        cell (Tuple[int, int]): A tuple containing the X and Y positions of the cell (cellx, celly).
        my_array (List[List[str]]): A 2D array representing the grid.
        empty_char (str): The character representing an empty cell in the array.

    Returns:
        List[Tuple[int, int]]: A list of neighboring cells as (x, y) tuples.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    possible_cells = []

    for dx, dy in directions:
        neighbor = (cell[0] + dx, cell[1] + dy)
        if cell_inside(neighbor):
            if my_array[cell] == empty_char and my_array[neighbor] != empty_char:
                possible_cells.append(neighbor)
            elif my_array[cell] != empty_char:
                possible_cells.append(neighbor)

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
    """for every cell in the array with a letter, returns a list of cells that can be played"""

    cells = list(product(range(5), range(5)))
    return {
        cell: step(cell, my_array, empty_char)
        for cell in cells
        if step(cell, my_array, empty_char)
    }


def check_user_path(user_path: list, my_array: list, empty_char: str) -> bool:
    """_summary_

    Args:
        user_path (list): list of cell positions
        my_array (list): list of lists containing the array

    Returns:
        bool: if the path is valid

    if len(user_path) < 3:
        return False
    else:
        for cell in user_path:
            if cell not in cells_to_play(my_array, empty_char):
                return False
        return True
    """
    return True
