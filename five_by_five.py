"""_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
from time import perf_counter
import os
import logging
from random import choice
from rich.console import Console
from rich import print as rich_print
from rich.columns import Columns
from rich.panel import Panel
from core_func import my_bad_function
from cells_func import (
    cell_inside,
    cell_neighbors,
    cells_to_play,
    create_array,
    possible_words_list,
    show_array,
    step,
)
from words_func import add_letter, find_word, start_word, set_first_word

ARRAY = []
ROWS, COLS = (5, 5)
MIN = 0
EMPTY_CHAR = "#"

# LOGGING SETUP
logging.basicConfig(
    filename="five_by_five.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s; %(message)s",
)

# SYSTEM FUNCIONS


def cls():
    """Clear screen"""
    os.system("cls" if os.name == "nt" else "clear")


def get_possible_words(
    bigger_than: int,
    smaller_than: int,
    my_dict: dict,
    my_words_played: list,
    words_file: str,
) -> list:
    """
    here we'll store all words that can be played in current stage
    but not the ones that are already played
    """
    current_state_words_ = []

    for key_, path_ in my_dict.items():
        if len(key_) > bigger_than and len(key_) < smaller_than:
            answer_ = find_word(key_, words_file)
            if len(answer_) > 0:
                if mod_answer_ := [
                    word for word in answer_ if word not in my_words_played
                ]:
                    current_state_words_.append([len(answer_[0]), mod_answer_, path_])
                    logging.debug("current_state_words, %s", current_state_words_)

    return current_state_words_


if __name__ == "__main__":
    console = Console()
    cls()
    ARRAY = create_array(ROWS, COLS, "#")
    START_WORD = start_word(ROWS, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt")
    set_first_word(ARRAY, 5, 5, START_WORD)
    words_played = [START_WORD.strip()]
    logging.debug("first word: %s", START_WORD.strip())
    # console.print(f"words_played: [blue]{words_played[0]}[/blue]")
    show_array(ARRAY)
    while True:
        start = perf_counter()
        e = my_bad_function(ARRAY, cells_to_play(ARRAY, "#"))
        # print(e, len(e), type(e))  # we have list with possible paths
        # inform if no path found
        if len(e) == 0:
            console.print("\nFinished! Exiting...", style="red")
            logging.debug("Finished! Exiting...")
            break
        f = possible_words_list(e, ARRAY)  # we have dict with possible words and paths

        # here we'll store all words that can be played in current stage
        # but not the ones that are already played
        # TODO: there is no exit condition if no words are found
        current_state_words = get_possible_words(
            3, 7, f, words_played, "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt"
        )
        if not current_state_words:
            logging.debug("No words found in range 3-7, trying 1-4")
            current_state_words = get_possible_words(
                1,
                4,
                f,
                words_played,
                "/home/cielak/Nauka/fivebyfive/rzeczowniki_rm.txt",
            )

        sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
        # print(len(sorted_current_state_words))
        max_lenght = sorted_current_state_words[0][0]

        # word to play next
        next_word_list = choice(
            [x for x in sorted_current_state_words if x[0] == max_lenght]
        )
        next_word = choice(next_word_list[1])
        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(ARRAY, letter, position[0], position[1])
        console.print(f"\nNew word: [blue]{next_word}[/blue] {next_word_list[2]}")
        words_played.append(next_word)
        console.print(f"Words played: {words_played}.")
        end = perf_counter()
        console.print(f"It took me: {end - start:.2f} seconds to find next_word.\n")
        logging.debug("It took me, %s seconds to find: %s.", end - start, next_word)
        # users = [words_played]
        user_renderables = [Panel(user, expand=True) for user in words_played]
        console.print(Columns(user_renderables))
        show_array(ARRAY)
