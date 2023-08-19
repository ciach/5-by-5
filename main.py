import itertools
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from time import time
from random import choice

from core_func import my_bad_function
from cells_func import (
    cells_to_play,
    create_array,
    possible_words_list,
)
from words_func import (
    add_letter,
    load_words,
    find_word,
    start_word,
    set_first_word,
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


# Mocking a function to calculate score based on word length
def calculate_score(word):
    """Calculate score for a given word."""
    return len(word) ** 2


# Updating the WordGameGUI class to integrate these functions
class WordGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Five by Five")
        self.master.geometry("700x300")

        self.short_words, self.long_words = load_words("rzeczowniki_rm.txt", 4, 10)
        self.my_array = create_array(5, 5, "#")

        self.current_path = []

        # Scoreboard GUI (Moved before initialize_game)
        self.score_frame = ttk.Frame(master)
        self.score_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # scoreboard_contents Text widget
        self.scoreboard_contents = tk.Text(
            self.master, wrap=tk.WORD, width=30, height=20
        )
        self.scoreboard_contents.grid(row=0, column=5, rowspan=6, sticky="nsew")

        # Step 1: Create a Scrollbar Widget
        self.scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL)

        # Step 2: Associate the Scrollbar with the Text Widget
        self.scrollbar.config(command=self.scoreboard_contents.yview)
        self.scoreboard_contents.config(yscrollcommand=self.scrollbar.set)

        # Step 3: Place the Scrollbar Next to the Text Widget in the Grid
        self.scrollbar.grid(row=0, column=6, rowspan=6, sticky="nsew")

        # Make the scoreboard_contents Text widget expand and fill the available space
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(5, weight=1)

        # Game Board GUI
        self.board_frame = ttk.Frame(master)
        self.board_frame.grid(row=0, column=0, sticky="nsew")
        self.buttons = {}
        for i, j in itertools.product(range(5), range(5)):
            btn = ttk.Button(
                self.board_frame,
                text=self.my_array[i][j],
                command=lambda i=i, j=j: self.cell_clicked(i, j),
            )
            btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
            self.buttons[(i, j)] = btn
            self.buttons[(i, j)].config(text=self.my_array[i][j].upper())

        # Control Area GUI
        self.control_frame = ttk.Frame(master)
        self.control_frame.grid(row=1, column=0, sticky="ew")
        self.pass_button = ttk.Button(
            self.control_frame, text="Pass", command=self.cpu_move
        )
        self.pass_button.grid(row=1, column=0, padx=5, pady=5)

        # Restart Button (New Game Button removed as requested)
        self.restart_button = ttk.Button(
            self.control_frame, text="Restart", command=self.restart_game
        )
        self.restart_button.grid(row=1, column=2, padx=5, pady=5)
        self.initialize_game()
        self.update_valid_cells()

    def initialize_game(self):
        """Initialize the game board and related variables."""
        self.my_array = create_array(5, 5, "#")
        self.played_words = []  # List to store words that have been played
        self.player_score = 0  # Player's score
        self.cpu_score = 0  # CPU's score
        first_word = start_word(
            5, self.long_words
        )  # Getting a 5-letter word for initialization
        self.played_words.append(first_word)
        set_first_word(self.my_array, first_word)
        # Update the button text to reflect changes in my_array
        for i, j in itertools.product(range(5), range(5)):
            self.buttons[(i, j)].config(text=self.my_array[i][j].upper())
        self.update_valid_cells()  # Update the valid cells
        # Update the scoreboard with initial values
        self.update_scoreboard()

    def update_valid_cells(self):
        """
        Disable all cells, then enable only the cells that are valid starting points
        for a new word based on the current state of the game board.
        """
        # Disable all buttons first
        for i, j in itertools.product(range(5), range(5)):
            self.buttons[(i, j)].config(state=tk.DISABLED)

        # Then enable only the valid cells
        valid_cells = cells_to_play(self.my_array, "#")
        for i, j in valid_cells:
            self.buttons[(i, j)].config(state=tk.NORMAL)

        # Check if the game is over (e.g., only one cell left on the board)
        empty_cells = sum(
            self.my_array[i][j] == "#" for i, j in itertools.product(range(5), range(5))
        )
        if empty_cells == 0:
            self.announce_winner()

    def update_scoreboard(self):
        """Update the scoreboard GUI with the current words and scores."""
        self.scoreboard_contents.config(state=tk.NORMAL)  # Enable editing
        self.scoreboard_contents.delete(1.0, tk.END)  # Clear existing content

        # Display the total scores for the player and CPU
        self.scoreboard_contents.insert(
            tk.END, f"Player Score: {self.player_score}\n", "player"
        )
        self.scoreboard_contents.insert(
            tk.END, f"CPU Score: {self.cpu_score}\n\n", "cpu"
        )

        # Display the initial word without points and with a different color (e.g., blue)
        initial_word = self.played_words[0].upper()
        self.scoreboard_contents.insert(tk.END, initial_word + "\n", "initial")
        self.scoreboard_contents.tag_config("initial", foreground="blue")

        # Display the remaining words and scores
        for word in self.played_words[1:]:
            score = calculate_score(word)
            self.scoreboard_contents.insert(tk.END, f"{word.upper()}: {score}\n")

        self.scoreboard_contents.config(state=tk.DISABLED)  # Disable editing

    def cpu_move(self):
        """Handle pass turn event (CPU's play)."""
        # Logic for the CPU's turn adapted from simple_play.py
        possible_paths = my_bad_function(
            self.my_array, cells_to_play(self.my_array, "#")
        )
        if len(possible_paths) == 0:
            self.announce_winner()

        words_dict = possible_words_list(possible_paths, self.my_array)
        current_state_words = get_current_state_words(
            words_dict, self.played_words, self.long_words
        )

        if not current_state_words:
            print("(INFO): No words found in range 4-10, trying 1-4")
            current_state_words = get_current_state_words(
                words_dict, self.played_words, self.short_words
            )

        sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
        max_length = sorted_current_state_words[0][0]
        matching_words = [x for x in sorted_current_state_words if x[0] == max_length]
        next_word_list = choice(matching_words)
        next_word = choice(next_word_list[1])

        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(self.my_array, letter, position[0], position[1])
            self.buttons[(position[0], position[1])].config(text=letter.upper())

        self.played_words.append(next_word)
        self.cpu_score += calculate_score(next_word)
        self.update_valid_cells()
        self.update_scoreboard()

    def restart_game(self):
        """Handle restart game event."""
        self.initialize_game()
        self.update_valid_cells()

    def show_letter_entry_dialog(self, i, j):
        """
        Show a dialog box to ask the user for a single letter.
        This method is called when a valid cell (i, j) on the board is clicked.
        """
        # Ask the user for a letter
        letter = simpledialog.askstring(
            "Input", "Enter a single letter:", parent=self.master
        )

        # Validate the input
        if letter and len(letter) == 1 and letter.isalpha():
            # If valid, update the board and the button text
            self.my_array[i][j] = letter.upper()
            self.buttons[(i, j)].config(text=letter.upper())

            # Ask the user for a word
            word = simpledialog.askstring("Input", "Enter a word:", parent=self.master)

            # Validate the input word
            if (
                word
                and word
                not in self.played_words  # Check if word has not been used before
                and (
                    word.lower() in self.long_words or word.lower() in self.short_words
                )
            ):
                # If valid, update the game state (e.g., update score,
                # add word to played_words, etc.)
                self.played_words.append(word.upper())
                self.player_score += calculate_score(word)
                self.update_scoreboard()
                self.update_valid_cells()
            elif word is not None:
                # If invalid, show an error message
                tk.messagebox.showerror(
                    "Invalid Input", "The entered word is not valid."
                )
                self.my_array[i][j] = "#"
                self.buttons[(i, j)].config(text="#")
            else:
                # If Cancel is pressed, remove the letter and let the computer play
                self.my_array[i][j] = "#"
                self.buttons[(i, j)].config(text="#")
        elif letter is not None:
            # If invalid, show an error message
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a single letter only."
            )

    def cell_clicked(self, i, j):
        """
        Called when a cell (i, j) on the board is clicked.
        """
        if self.my_array[i][j] != "#":
            return
        # Show the letter entry dialog box
        self.show_letter_entry_dialog(i, j)
        self.cpu_move()

    def announce_winner(self):
        """_summary_"""
        if self.player_score > self.cpu_score:
            winner_message = "Congratulations! You won!"
        elif self.player_score < self.cpu_score:
            winner_message = "Sorry! The computer won. Better luck next time."
        else:
            winner_message = "It's a tie!"

        # Show the message box with the winner announcement
        messagebox.showinfo("Game Over", winner_message)
        self.restart_game()

    def setup_endgame_scenario(self):
        """_summary_"""
        for i, j in itertools.product(range(5), range(5)):
            self.my_array[i][j] = "A"  # Set all cells to 'A'

        # Leave the last cell empty to simulate one cell left
        self.my_array[4][4] = "#"

        # Step 3: Update the GUI
        for i, j in itertools.product(range(5), range(5)):
            self.buttons[(i, j)].config(text=self.my_array[i][j].upper())

        # Update the valid cells based on the new board state
        self.update_valid_cells()


root = tk.Tk()
app = WordGameGUI(root)
root.mainloop()