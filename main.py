import argparse
import itertools
import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk, messagebox
from random import choice
from time import time
from custom_input_dialog import CustomInputDialog
from tabulate_label import TabulateLabel
from core_func import my_bad_function
from cells_func import (
    cells_to_play,
    create_array,
    possible_words_list,
)
from words_func import (
    add_letter,
    calculate_score,
    get_current_state_words,
    load_words,
    start_word,
    set_first_word,
)


class WordGameGUI:
    def __init__(self, master, mode="single"):
        self.played_words = []  # List to store words that have been played
        self.player_words = []  # List to store words played by the player
        self.cpu_words = []  # List to store words played by the CPU
        self.player_score = 0  # Player's score
        self.word = ""  # Word entered by the player
        self.cpu_score = 0  # CPU's score
        self.is_cpu_move = False  # Flag to indicate if it's the CPU's move
        self.is_player_move_completed = False
        self.is_player_first_click = True
        self.is_path_validated = False
        self.is_timer_running = False

        self.time_limit = 60  # Default to 60 seconds (1 minute)
        self.time_remaining = self.time_limit
        self.is_input_in_progress = False

        self.current_word_path = []  # List to store the current word path
        self.player_words_paths = []  # List of lists to store the player's word paths
        self.word_from_path = []

        # Choose the appropriate dictionary based on the language argument
        if args.language == "pl":
            dictionary_file = "dict.txt"
        else:  # Default to English
            dictionary_file = "singular_nouns.txt"
        self.short_words, self.long_words = load_words(dictionary_file, 4, 10)

        self.my_array = create_array(5, 5, "#")
        self.master = master
        self.master.title("Gridly / Quintix / Five by Five")
        self.master.geometry("830x330")
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Consolas", size=10)

        style = ttk.Style()
        style.configure("Green.TButton", background="lightgreen")
        style.configure("Grey.TButton", background="lightblue")

        # Scoreboard GUI (TabulateLabel)
        self.scoreboard_label = TabulateLabel(
            self.master,
            self.player_words,
            self.cpu_words,
            width=40,
            height=20,
            bg="white",
        )
        self.scoreboard_label.grid(row=0, column=5, rowspan=6, sticky="nsew")

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
            btn.grid(row=i, column=j, sticky="nsew", padx=0, pady=0)
            self.buttons[(i, j)] = btn
            self.buttons[(i, j)].config(text=self.my_array[i][j].upper())
            self.buttons[(i, j)].config(style="Grey.TButton")

        # Control Area GUI
        self.control_frame = ttk.Frame(master)
        self.control_frame.grid(row=1, column=0, sticky="ew")
        # Timer label to display the time remaining
        self.timer_label = ttk.Label(
            self.control_frame, text=f"Time Remaining: {self.time_remaining}"
        )
        self.timer_label.grid(row=0, column=1, padx=5, pady=5)

        self.player_score_label = ttk.Label(self.control_frame)
        self.player_score_label.grid(row=2, column=1, padx=20, pady=5)
        self.cpu_score_label = ttk.Label(self.control_frame)
        self.cpu_score_label.grid(row=3, column=1, padx=20, pady=6)
        self.turn_label = ttk.Label(self.control_frame)
        self.turn_label.grid(row=1, column=1, padx=20, pady=5)
        self.re_do_path = ttk.Button(
            self.control_frame,
            text="Re-Do Path",
            command=self.reset_for_incorrect_path,
            state=tk.DISABLED,
        )

        self.re_do_path.grid(row=0, column=0, padx=5, pady=5)
        self.pass_button = ttk.Button(
            self.control_frame, text="Pass", command=self.handle_pass
        )
        self.pass_button.grid(row=1, column=0, padx=5, pady=5)

        # Restart Button (New Game Button removed as requested)
        self.restart_button = ttk.Button(
            self.control_frame, text="Restart", command=self.restart_game
        )
        self.restart_button.grid(row=2, column=0, padx=5, pady=5)

        # Creating the Menu Bar
        self.menubar = tk.Menu(master)

        # File Dropdown
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Restart", command=self.restart_game)
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # User Time Dropdown
        self.time_menu = tk.Menu(self.menubar, tearoff=0)
        self.time_menu.add_command(
            label="No Limit", command=lambda: self.time_limit == 0
        )
        self.time_menu.add_command(label="1 min", command=lambda: self.time_limit == 60)
        self.time_menu.add_command(
            label="3 min", command=lambda: self.time_limit == 180
        )
        self.time_menu.add_command(
            label="5 min", command=lambda: self.time_limit == 300
        )
        self.menubar.add_cascade(label="User Time", menu=self.time_menu)

        # Display the Menu Bar
        master.config(menu=self.menubar)

        self.initialize_game()
        self.update_valid_cells()

        self.mode = mode
        if self.mode == "multi":
            self.setup_client()

    def initialize_game(self):
        """Initialize the game board and related variables."""
        self.player_score = 0
        self.cpu_score = 0
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.cpu_score_label.config(text=f"CPU Score: {self.cpu_score}")
        self.turn_label.config(text="Turn: Player")
        self.played_words = []
        self.player_words = []
        self.cpu_words = []
        self.is_player_move_completed = False
        self.is_player_first_click = True
        self.is_path_validated = False
        self.is_input_in_progress = False
        self.word = ""
        self.my_array = create_array(5, 5, "#")
        first_word = start_word(
            5, self.long_words
        )  # Getting a 5-letter word for initialization
        self.played_words.append(first_word.lower())
        set_first_word(self.my_array, first_word)
        # Update the button text to reflect changes in my_array
        self.update_game_board()
        self.update_valid_cells()  # Update the valid cells
        # Update the scoreboard with initial values
        self.update_scoreboard()
        self.start_timer()

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

        # Check if the game is over (e.g., no empty cell left on the board)
        empty_cells = sum(
            self.my_array[i][j] == "#" for i, j in itertools.product(range(5), range(5))
        )
        if empty_cells == 0:
            self.announce_winner()

    def update_scoreboard(self):
        """Update the scoreboard GUI with the current words and scores."""
        self.scoreboard_label.config(state=tk.NORMAL)  # Enable editing

        # Update the TabulateLabel with the current words and scores
        self.scoreboard_label = TabulateLabel(
            self.master, self.player_words, self.cpu_words, bg="white"
        )
        self.scoreboard_label.grid(row=0, column=5, rowspan=6, sticky="nsew")

        # Update player and CPU scores
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.cpu_score_label.config(text=f"CPU Score: {self.cpu_score}")

    def update_game_board(self):
        """Update the game board GUI with the current state of the game board."""
        for i, j in itertools.product(range(5), range(5)):
            self.buttons[(i, j)].config(
                text=self.my_array[i][j].upper(), style="Grey.TButton"
            )

    def cpu_move(self):
        """Handle pass turn event (CPU's play)."""
        self.is_cpu_move = True
        start_time = time()  # Start time
        self.turn_label.config(text="Turn: CPU")
        self.master.update_idletasks()
        # Start time
        start_time = time()
        possible_paths = my_bad_function(
            self.my_array, cells_to_play(self.my_array, "#")
        )
        # Check if the game is over (e.g., no cell left on the board)
        if len(possible_paths) == 0:
            self.announce_winner()

        words_dict = possible_words_list(possible_paths, self.my_array)
        current_state_words = get_current_state_words(
            words_dict, self.played_words, tuple(self.long_words)
        )

        if not current_state_words:
            print("(INFO): No words found in range 4-10, trying 1-4")
            current_state_words = get_current_state_words(
                words_dict, sorted(self.played_words), self.short_words
            )

        sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
        max_length = sorted_current_state_words[0][0]
        matching_words = [x for x in sorted_current_state_words if x[0] == max_length]
        next_word_list = choice(matching_words)
        next_word = choice(next_word_list[1])

        # Making sure the chosen word is not in played_words
        while next_word in self.played_words:
            next_word_list = choice(matching_words)
            next_word = choice(next_word_list[1])

        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(self.my_array, letter, position[0], position[1])
            self.buttons[(position[0], position[1])].config(text=letter.upper())
            self.buttons[(position[0], position[1])].config(style="Green.TButton")

        # End time
        end_time = time()
        self.played_words.append(next_word)
        self.cpu_words.append(next_word)
        self.cpu_score += calculate_score(next_word)
        self.update_scoreboard()
        self.master.update_idletasks()
        self.master.after(
            1750,
            lambda: [
                self.update_game_board(),
                self.update_valid_cells(),
                self.turn_label.config(text="Turn: Player"),
            ],
        )
        self.is_path_validated = False
        self.is_player_move_completed = False
        self.master.update_idletasks()
        self.is_input_in_progress = True
        self.is_player_first_click = True

        # Calculate and print the duration
        duration = end_time - start_time
        print(f"(INFO): cpu_move took {duration:.2f} seconds to execute.")
        self.is_cpu_move = False

    def restart_game(self):
        """Handle restart game event."""
        self.stop_timer()
        self.initialize_game()
        self.update_valid_cells()
        self.update_scoreboard()

    def show_letter_entry_dialog(self, i, j):
        """
        Show a dialog box to ask the user for a single letter.
        This method is called when a valid cell (i, j) on the board is clicked.
        """
        # Ask the user for a letter
        letter_dialog = CustomInputDialog(
            self.master, "Input", "Enter a single letter:", OneLetter=True
        )
        self.master.wait_window(letter_dialog)

        letter = letter_dialog.result

        # Validate the input letter
        if letter and len(letter) == 1 and letter.isalpha():
            # If valid, update the board and the button text
            self.my_array[i][j] = letter.upper()
            self.buttons[(i, j)].config(text=letter.upper())

            # Ask the user for a word
            word_dialog = CustomInputDialog(self.master, "Input", "Enter a word:")
            self.master.wait_window(word_dialog)

            if word_dialog.result is None:
                # Reset the cell if word input is cancelled
                self.my_array[i][j] = "#"
                self.buttons[(i, j)].config(text="#")
                self.is_player_move_completed = False
            else:
                self.word = word_dialog.result.strip().lower()

                # Validate the input word
                if (
                    self.word
                    and self.word
                    not in self.played_words  # Check if word has not been used before
                    and (self.word in self.long_words or self.word in self.short_words)
                ):
                    self.is_player_move_completed = True
                    self.is_path_validated = False

                else:
                    # If invalid word, show an error message
                    tk.messagebox.showerror(
                        "Invalid Input", "The entered word is not valid."
                    )
                    self.played_words.append(f"( {self.word} )")
                    self.player_words.append(f"( {self.word} )")
                    self.my_array[i][j] = "#"
                    self.buttons[(i, j)].config(text="#")
                    # Get out of the loop if the word is invalid
                    self.is_path_validated = True
                    self.is_player_move_completed = True
                self.is_player_move_completed = True
        elif letter is None:
            self.is_player_move_completed = False
        else:
            # If invalid letter, show an error message
            tk.messagebox.showerror(
                "Invalid Input", "Please enter a single letter only."
            )
            self.is_player_move_completed = False

    def cell_clicked(self, i, j):
        """Called when a cell (i, j) on the board is clicked."""
        # If it's the player's first click and the clicked cell is not '#', just return
        if (
            self.is_player_first_click
            and self.my_array[i][j] != "#"
            or self.is_cpu_move
        ):
            return

        # If the first move is being made by the player, set the is_player_first_click to False
        if self.is_player_first_click:
            self.is_player_first_click = False

        # If the player move is not completed, show the letter entry dialog box
        if not self.is_player_move_completed:
            self.show_letter_entry_dialog(i, j)
            return  # Return early, no further processing needed

        # If the path is not validated, handle the unvalidated path
        if not self.is_path_validated:
            self.handle_unvalidated_path(i, j)
            return  # Return early, no further processing needed

        # If we've gotten this far, handle the validated path
        self.handle_validated_path()

    def handle_unvalidated_path(self, i, j):
        """
        Handles an unvalidated path in the word grid.

        Args:
            i: The row index of the button in the grid.
            j: The column index of the button in the grid.

        Returns:
            None

        Examples:
            handle_unvalidated_path(2, 3)
        """
        self.buttons[(i, j)].config(style="Green.TButton")
        self.word_from_path.append(self.my_array[i][j])
        current_word = "".join(self.word_from_path).lower()

        if current_word == self.word.lower():
            self.update_for_correct_path()
        elif (
            len(self.word_from_path) >= len(self.word)
            and current_word != self.word.lower()
        ):
            self.reset_for_incorrect_path()

    def handle_validated_path(self):
        """Handles actions when a cell is clicked and
        the player's move path is already validated."""
        self.update_game_board()
        self.update_scoreboard()
        self.update_valid_cells()
        self.master.after(500, self.cpu_move)

    def update_for_correct_path(self):
        """Update actions for a correct path."""
        self.played_words.append(self.word)
        self.player_words.append(self.word)
        self.player_score += calculate_score(self.word)
        self.update_scoreboard()

        # Introduce a delay then update game board and valid cells
        self.master.after(1750, self.post_correct_path_updates)

    def post_correct_path_updates(self):
        """Actions to perform after a delay following a correct path selection."""
        self.update_game_board()
        self.update_valid_cells()
        self.is_player_first_click = True
        self.master.after(500, self.cpu_move)
        self.is_path_validated = True
        self.word_from_path = []

    def reset_for_incorrect_path(self):
        """Reset actions for an incorrect path."""
        self.re_do_path.config(state=tk.NORMAL)
        self.word_from_path = []

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

    def handle_pass(self):
        """Handle the event when the player decides to pass their turn."""
        self.player_words.append("( Pass )")
        self.update_scoreboard()
        self.reset_timer()
        self.cpu_move()
        # DEBUG lines
        # print(self.played_words)
        # print(self.my_array)

    def start_timer(self):
        pass

    def update_timer(self):
        pass

    def reset_timer(self):
        pass

    def stop_timer(self):
        pass

    def setup_endgame_scenario(self):
        """_summary_"""
        for i, j in itertools.product(range(5), range(5)):
            self.my_array[i][j] = "A"  # Set all cells to 'A'

        # Leave the last cell empty to simulate one cell left
        self.my_array[4][4] = "#"
        self.player_score = 1250
        self.update_game_board()
        self.update_valid_cells()

    def setup_client(self):
        # Set up client socket to connect to game server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(
            ("127.0.0.1", 65432)
        )  # Connect to server on localhost
        welcome_message = self.client_socket.recv(1024)
        print(welcome_message.decode())


parser = argparse.ArgumentParser(description="Five-by-Five Word Game")
parser.add_argument(
    "-lang",
    "--language",
    type=str,
    default="pl",
    choices=["eng", "pl"],
    help="Language for the dictionary (default: pl)",
)
args = parser.parse_args()

if __name__ == "__main__":
    # mode = input("Choose game mode (single/multi): ").strip().lower()
    root = tk.Tk()
    # app = WordGameGUI(root, mode=mode)
    app = WordGameGUI(root, mode="single")
    root.mainloop()
