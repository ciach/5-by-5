"""_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_

    TODO: we should load all the words from dictionary into memory / list
    TODO: words longer than X letters should be ignored, X value TBD (11?)
    TODO: figure out the user input method for path (only one letter?) or a GUI/TUI?
    TODO: add two buttons press to show last word played
    """
from time import perf_counter
import os
import logging
from random import choice
from math import pow
from rich.console import Console
from rich import print as rich_print
from rich.columns import Columns
from rich.panel import Panel
from rich.progress import track
from core_func import my_bad_function
from cells_func import (
    cell_inside,
    cell_neighbors,
    cells_to_play,
    check_user_path,
    create_array,
    possible_words_list,
    show_array,
    step,
)
from words_func import (
    add_letter,
    check_user_word,
    find_word,
    load_words,
    start_word,
    set_first_word,
)

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
    my_dict: dict,
    my_words_played: list,
    words_list: list,
) -> list:
    """
    here we'll store all words that can be played in current stage
    but not the ones that are already played
    """
    current_state_words_ = []

    for key_, path_ in my_dict.items():
        answer_ = find_word(key_, words_list)
        if len(answer_) > 0:
            if mod_answer_ := [word for word in answer_ if word not in my_words_played]:
                current_state_words_.append([len(answer_[0]), mod_answer_, path_])
                logging.debug("current_state_words, %s", current_state_words_)

    return current_state_words_


def words_display(words_played_: list, score: bool = False) -> None:
    """Display score"""
    if score:
        return [
            Panel(f"{word} - {str(pow(len(word), 2))}", expand=True)
            for word in words_played_
        ]
    return [Panel(f"{word}", expand=True) for word in words_played_]


def score_display(words_played_: list) -> None:
    """Display score"""
    return int(sum(pow(len(word), 2) for word in words_played_))


if __name__ == "__main__":
    console = Console()
    cls()
    short_words, long_words = load_words("rzeczowniki_rm.txt", 4, 8)
    ARRAY = create_array(ROWS, COLS, "#")
    START_WORD = start_word(ROWS, long_words)
    set_first_word(ARRAY, 5, 5, START_WORD)
    words_played = [START_WORD.strip()]
    words_played_player_one = []
    words_played_player_two = []
    logging.debug("first word: %s", START_WORD.strip())
    # console.print(f"words_played: [blue]{words_played[0]}[/blue]")
    show_array(ARRAY)
    console.print()
    while True:
        # user starts to play
        user_word = input("Enter word (to pass press ENTER): ")
        if check_user_word(user_word, words_played, long_words) or check_user_word(
            user_word, words_played, short_words
        ):
            console.print("Word is correct!")
            user_letter = input("Enter new letter: ")
            user_path_str = input("New letter position in format y,x: ")
            user_path = user_path_str.split(",")
            if check_user_path(user_path, ARRAY, "#"):
                console.print("Letter position is correct!")
                console.print(f"Your word is: [blue]{user_word}[/blue],")
                console.print(f"your new letter is: {user_letter}")
                console.print(f"position is: [blue]{user_path}[/blue]")
                logging.debug("user word: %s", user_word)
                logging.debug("user letter: %s", user_letter)
                logging.debug("user path: %s", user_path)
                console.print(f"{user_word}: {user_letter}: {user_path}")
                add_letter(ARRAY, user_letter, int(user_path[0]), int(user_path[1]))
                words_played.append(user_word)
                words_played_player_one.append(user_word)
                console.print()
                show_array(ARRAY)
        else:
            logging.debug("no user word")
        # computer starts to play
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
        # use rich progress bar to show progress of function
        console.print()
        with console.status("[bold green]Finding possible words...") as status:
            current_state_words = get_possible_words(f, words_played, long_words)
        if not current_state_words:
            logging.debug("No words found in range 3-7, trying 1-4")
            with console.status("[bold green]Finding more possible words...") as status:
                current_state_words = get_possible_words(f, words_played, short_words)

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
        console.print(
            f"\nNew word: [dark_olive_green2]{next_word}[/dark_olive_green2] {next_word_list[2]}"
        )
        words_played.append(next_word)
        words_played_player_two.append(next_word)
        console.print(f"Words played: {words_played}.")
        end = perf_counter()
        console.print(f"It took me: {end - start:.2f} seconds to find {next_word}.\n")
        logging.debug("It took me, %s seconds to find: %s.", end - start, next_word)
        console.print(Columns(words_display(words_played)))
        console.print(f"Player One: {score_display(words_played_player_one)}")
        console.print(f"Player Two: {score_display(words_played_player_two)}")
        show_array(ARRAY)
        console.print()
