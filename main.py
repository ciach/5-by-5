import argparse
import itertools
import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk, messagebox
from random import choice
from time import time
from tabulate import tabulate
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


class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.result = None  # default value
        self.label = tk.Label(self, text=message)
        self.label.pack(padx=10, pady=10)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind("<Return>", lambda event=None: self.on_ok())
        self.entry.focus_set()

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

        x_pos = parent.winfo_x() + 520
        y_pos = parent.winfo_y() + 10
        self.geometry(f"+{x_pos}+{y_pos}")

    def on_ok(self):
        """on clicking OK button"""
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        """on clicking cancel button"""
        self.result = None
        self.destroy()


class TabulateLabel(tk.Label):
    def __init__(self, parent, player_words, cpu_words, **kwargs):
        super().__init__(
            parent, font=("Consolas", 10), justify=tk.LEFT, anchor="nw", **kwargs
        )

        # Determine the length of the longer list
        max_length = max(len(player_words), len(cpu_words))

        # Dynamically create the data based on the length of the longer list
        data = [("Player", "Points", "Cpu", "Points")]
        for i in range(max_length):
            player_word = player_words[i] if i < len(player_words) else ""
            cpu_word = cpu_words[i] if i < len(cpu_words) else ""
            player_points = str(calculate_score(player_word)) if player_word else ""
            cpu_points = str(calculate_score(cpu_word)) if cpu_word else ""

            data.append(
                (player_word.upper(), player_points, cpu_word.upper(), cpu_points)
            )

        text = tabulate(data, headers="firstrow", tablefmt="github", showindex=False)
        self.configure(text=text)


# Updating the WordGameGUI class to integrate these functions
class WordGameGUI:
    def __init__(self, master, mode="single"):
        self.played_words = []  # List to store words that have been played
        self.player_words = []  # List to store words played by the player
        self.cpu_words = []  # List to store words played by the CPU
        self.player_score = 0  # Player's score
        self.word = ""  # Word entered by the player
        self.cpu_score = 0  # CPU's score
        self.is_player_move_completed = False
        self.is_path_validated = False
        self.is_timer_running = False

        self.time_limit = 60  # Default to 60 seconds (1 minute)
        self.selected_time = 180  # Default to 3 minutes (180 seconds)
        self.time_remaining = self.time_limit

        self.current_word_path = []  # List to store the current word path
        self.player_words_paths = []  # List of lists to store the player's word paths
        self.word_from_path = []

        # Choose the appropriate dictionary based on the language argument
        if args.language == "pl":
            dictionary_file = "rzeczowniki_rm.txt"
        else:  # Default to English
            dictionary_file = "singular_nouns.txt"
        self.short_words, self.long_words = load_words(dictionary_file, 4, 10)

        self.my_array = create_array(5, 5, "#")
        self.master = master
        self.master.title("Gridly / Quintix")
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
        self.time_remaining = 60  # initial time (1 minute)
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
        self.pass_button = ttk.Button(
            self.control_frame, text="Pass", command=self.handle_pass
        )
        self.pass_button.grid(row=0, column=0, padx=5, pady=5)

        # Restart Button (New Game Button removed as requested)
        self.restart_button = ttk.Button(
            self.control_frame, text="Restart", command=self.restart_game
        )
        self.restart_button.grid(row=1, column=0, padx=5, pady=5)

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
            label="No Limit", command=lambda: self.selected_time == 0
        )
        self.time_menu.add_command(
            label="1 min", command=lambda: self.selected_time == 60
        )
        self.time_menu.add_command(
            label="3 min", command=lambda: self.selected_time == 180
        )
        self.time_menu.add_command(
            label="5 min", command=lambda: self.selected_time == 300
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
        self.is_path_validated = False
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

        # Check if the game is over (e.g., only one cell left on the board)
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
        # End time
        end_time = time()
        self.played_words.append(next_word)
        self.cpu_words.append(next_word)
        self.cpu_score += calculate_score(next_word)
        self.update_scoreboard()
        self.master.update_idletasks()
        self.update_valid_cells()
        self.turn_label.config(text="Turn: Player")
        self.is_path_validated = False
        self.is_player_move_completed = False
        self.master.update_idletasks()
        self.stop_timer()
        self.start_timer()
        end_time = time()

        # Calculate and print the duration
        duration = end_time - start_time
        print(f"(INFO): cpu_move took {duration:.2f} seconds to execute.")

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
            self.master, "Input", "Enter a single letter:"
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
        """
        Called when a cell (i, j) on the board is clicked.

        if self.my_array[i][j] != "#":
            return
        """
        if self.is_player_move_completed and not self.is_path_validated:
            self.buttons[(i, j)].config(style="Green.TButton")
            self.word_from_path.append(self.my_array[i][j])
            if "".join(self.word_from_path).lower() == self.word.lower():
                self.played_words.append(self.word)
                self.player_words.append(self.word)
                self.player_score += calculate_score(self.word)
                self.update_game_board()
                self.update_scoreboard()
                self.update_valid_cells()
                self.master.after(500, self.cpu_move)
                self.is_path_validated = True
                self.word_from_path = []
        elif self.is_player_move_completed and self.is_path_validated:
            self.update_game_board()
            self.update_scoreboard()
            self.update_valid_cells()
            self.master.after(500, self.cpu_move)
        else:
            # Show the letter entry dialog box
            self.show_letter_entry_dialog(i, j)

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

    def start_timer(self):
        """Start the timer."""
        self.time_remaining = self.selected_time  # Reset to the selected time
        self.update_timer()

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
