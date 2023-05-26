from pathlib import Path
from time import perf_counter, time
import os
import logging
from random import choice
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from core_func import my_bad_function
from cells_func import (
    cells_to_play,
    check_user_path,
    create_array,
    possible_words_list,
    show_array,
)
from words_func import (
    add_letter,
    check_user_letter,
    check_user_word,
    find_word,
    load_words,
    start_word,
    set_first_word,
)

ARRAY = []
ROWS, COLS = (5, 5)

# LOGGING SETUP
logging.basicConfig(
    filename="five_by_five.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s; %(message)s",
)

# SYSTEM FUNCTIONS


def cls():
    """Clear screen"""
    os.system("cls" if os.name == "nt" else "clear")


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
                logging.debug("current_state_words: %s", current_state_words)
        if time() - start_time > time_limit:
            break
    return current_state_words


def words_display(words_played: list, score: bool = False) -> list:
    """Generate the panels for displaying words and scores"""
    if score:
        return [
            Panel(f"{word} - {str(pow(len(word), 2))}", expand=True)
            for word in words_played
        ]
    return [Panel(f"{word}", expand=True) for word in words_played]


def score_display(words_played: list) -> int:
    """Calculate the total score"""
    return int(sum(pow(len(word), 2) for word in words_played))


if __name__ == "__main__":
    console = Console()
    cls()
    short_words, long_words = load_words("rzeczowniki_rm.txt", 4, 10)
    ARRAY = create_array(ROWS, COLS, "#")
    START_WORD = start_word(ROWS, long_words)
    set_first_word(ARRAY, ROWS, COLS, START_WORD)
    words_played = [START_WORD.strip()]
    words_played_player_one = []
    words_played_player_two = []
    logging.debug("First word: %s", START_WORD.strip())
    show_array(ARRAY)
    console.print()

    while True:
        # User plays
        user_word = input("Enter a word (to pass, press ENTER): ")
        if check_user_word(user_word, words_played, long_words) or check_user_word(
            user_word, words_played, short_words
        ):
            console.print("Word is correct!")
            user_letter = input("Enter a new letter: ")
            if check_user_letter(user_letter):
                user_path_str = input("Enter the letter position in format y,x: ")
                user_path = user_path_str.split(",")
                if check_user_path(user_path, ARRAY, "#"):
                    console.print("Letter position is correct!")
                    console.print(f"Your word is: [orchid1]{user_word}[/orchid1],")
                    console.print(f"Your new letter is: {user_letter}")
                    console.print(f"Position is: [orchid1]{user_path}[/orchid1]")
                    logging.debug("User word: %s", user_word)
                    logging.debug("User letter: %s", user_letter)
                    logging.debug("User path: %s", user_path)
                    add_letter(ARRAY, user_letter, int(user_path[0]), int(user_path[1]))
                    words_played.append(user_word)
                    words_played_player_one.append(user_word)
                    console.print()
                    show_array(ARRAY)
                else:
                    console.print(
                        "Letter is incorrect! Should be one letter! Not a number!"
                    )
                    console.print("Computer will play!")
            else:
                console.print("Letter is incorrect! Should be one letter!")
                console.print("Computer will play!")
        else:
            logging.debug("No user word")

        # Computer plays
        start = perf_counter()
        possible_paths = my_bad_function(ARRAY, cells_to_play(ARRAY, "#"))
        if len(possible_paths) == 0:
            console.print("\nFinished! Exiting...", style="red")
            logging.debug("Finished! Exiting...")
            break
        words_dict = possible_words_list(possible_paths, ARRAY)

        # Find words that can be played in the current stage
        current_state_words = get_current_state_words(
            words_dict, words_played, long_words
        )
        if not current_state_words:
            logging.debug("No words found in range 3-7, trying 1-4")
            current_state_words = get_current_state_words(
                words_dict, words_played, short_words
            )

        sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
        max_length = sorted_current_state_words[0][0]

        # Select the word to play next
        matching_words = [x for x in sorted_current_state_words if x[0] == max_length]
        next_word_list = choice(matching_words)
        next_word = choice(next_word_list[1])

        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(ARRAY, letter, position[0], position[1])
        console.print(
            f"\nNew word: [dark_olive_green2]{next_word}[/dark_olive_green2] {next_word_list[2]}"
        )
        words_played.append(next_word)
        words_played_player_two.append(next_word)
        end = perf_counter()
        console.print(f"It took me: {end - start:.2f} seconds to find {next_word}.\n")
        logging.debug("It took me %s seconds to find: %s.", end - start, next_word)
        console.print(Columns(words_display(words_played)))
        console.print(f"Player One: {score_display(words_played_player_one)}")
        console.print(
            f"Player Two (computer): {score_display(words_played_player_two)}"
        )
        show_array(ARRAY)
        console.print()

    console.print(f"Player One: {score_display(words_played_player_one)}")
    console.print(f"Player Two (computer): {score_display(words_played_player_two)}")
    if score_display(words_played_player_one) > score_display(words_played_player_two):
        console.print("Player One wins!", style="blink")
    elif score_display(words_played_player_one) < score_display(
        words_played_player_two
    ):
        console.print("Player Two (computer) wins!")
    else:
        console.print("Draw!")
