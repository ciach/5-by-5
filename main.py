import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as messagebox
import random
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


short_words, long_words = load_words("rzeczowniki_rm.txt", 4, 10)
ARRAY = create_array(5, 5, "#")


class WordGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("5 by 5 Game")
        self.short_words = []
        self.long_words = []
        self.ARRAY = []
        self.last_button_clicked = None  # To keep track of the last button clicked
        self.state = (
            "input_letter"  # This can be "input_letter", "input_word", or "select_word"
        )

        self.current_player = 1  # Player 1 starts

        # Create a frame for the grid and scoreboard
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create a frame for the grid
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create the 5 by 5 grid of buttons
        self.grid_buttons = []
        for row in range(5):
            button_row = []
            for col in range(5):
                button = tk.Button(self.grid_frame, text="", width=10, height=2)
                button.grid(row=row, column=col, padx=2, pady=2)
                button.config(command=lambda btn=button: self.on_button_click(btn))
                button_row.append(button)
            self.grid_buttons.append(button_row)

        self.clicked_buttons = []  # List to keep track of clicked buttons in order
        self.word = ""  # The current word being formed by the user
        self.clicked_word = ""  # The word that is being clicked by the user

        # Create a frame for the scoreboard
        self.scoreboard_frame = tk.Frame(self.main_frame)
        self.scoreboard_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create a label for the scoreboard
        self.scoreboard_label = tk.Label(self.scoreboard_frame, text="Words Played:")
        self.scoreboard_label.pack(side=tk.TOP)

        # Create a label for the scoreboard
        self.scoreboard_label = tk.Label(self.scoreboard_frame, text="Turn: {}")
        self.scoreboard_label.pack(side=tk.TOP)
        self.update_scoreboard()

        # Create a text widget for the scoreboard
        self.scoreboard_text = tk.Text(
            self.scoreboard_frame, width=20, height=15, wrap=tk.WORD
        )
        self.scoreboard_text.pack(side=tk.TOP)

        # Create a frame for the control buttons
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create control buttons
        self.new_game_button = tk.Button(
            self.control_frame, text="New Game", command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = tk.Button(self.control_frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.LEFT, padx=5)
        self.new_game()

    def on_button_click(self, button):
        if self.current_player == 1:
            if self.state == "input_letter" and button["text"] == "":
                letter = self.get_letter()
                if letter:
                    button.config(text=letter)
                    self.get_word_from_user()
            elif self.state == "select_word":
                self.add_button_to_word(button)

    def get_word(self):
        word = ""
        while not word:
            word = simpledialog.askstring(
                "Enter Word", f"Player {self.current_player}, enter your word:"
            )
        return word

    def is_valid_word(self, word):
        if len(word) <= 4:
            return word in self.short_words
        else:
            return word in self.long_words

    def get_letter(self):
        letter = ""
        while not letter:
            letter = simpledialog.askstring(
                "Enter Letter", f"Player {self.current_player}, enter a letter:"
            )
            if letter:
                letter = letter[0].upper()  # Get only the first character

                # Check if the input is a letter
                if not letter.isalpha():
                    messagebox.showinfo("Invalid Input", "Please enter a letter.")
                    letter = ""
        return letter

    def switch_player(self):
        self.current_player = 3 - self.current_player
        self.update_scoreboard()
        if self.current_player == 2:
            self.computer_move()

    def update_scoreboard(self):
        player_name = "Computer" if self.current_player == 2 else "Player One"
        self.scoreboard_label.config(text=f"Turn: {player_name}")

    def computer_move(self):
        empty_buttons = [
            (r, c)
            for r, row in enumerate(self.grid_buttons)
            for c, button in enumerate(row)
            if button["text"] == ""
        ]
        if empty_buttons:
            row, col = random.choice(empty_buttons)
            letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            self.grid_buttons[row][col].config(text=letter)
            self.switch_player()

            if self.board_full():
                messagebox.showinfo("Game Over", "All spaces are filled!")
                self.new_game()

    def new_game(self):
        # Reset the grid buttons
        for row in self.grid_buttons:
            for button in row:
                button.config(text="")

        # Load words from the file
        self.short_words, self.long_words = load_words("rzeczowniki_rm.txt", 4, 10)

        # Create the initial state of the game board
        self.ARRAY = create_array(5, 5, "#")

        # Set the third row to contain a 5-letter word
        START_WORD = start_word(5, self.long_words)
        START_WORD = START_WORD.upper()

        for col, letter in enumerate(START_WORD):
            self.grid_buttons[2][col].config(text=letter)
            self.ARRAY[2][col] = letter  # Update the ARRAY with the START_WORD

        # Update the current player
        self.current_player = 1
        self.update_scoreboard()

    def board_full(self):
        for row in self.grid_buttons:
            for button in row:
                if button["text"] == "":
                    return False
        return True

    def remove_last_letter(self):
        if self.last_button_clicked:
            self.last_button_clicked.config(text="")
            self.last_button_clicked = None  # Reset the last button clicked

    def get_word_from_user(self):
        word = simpledialog.askstring("Enter Word", "Player 1, enter your word:")
        if word:
            if self.word_exists(word.upper()):
                self.word = word.upper()
                self.state = "select_word"
            else:
                messagebox.showinfo(
                    "Invalid Word", "The word you entered does not exist."
                )
                # Remove the last inputted letter
                for row in self.grid_buttons:
                    for button in row:
                        if button["text"] == "":
                            button.config(text="")
                            break
                self.switch_player()

    def add_button_to_word(self, button):
        if button["text"] != "":
            if not self.clicked_buttons:  # If the clicked buttons list is empty
                self.clicked_buttons.append(button)
                self.clicked_word += button["text"]
            else:  # If there are already buttons in the clicked buttons list
                last_button = self.clicked_buttons[-1]
                last_button_row, last_button_col = self.get_button_position(last_button)
                button_row, button_col = self.get_button_position(button)

                # Only add the button to the clicked buttons list if it is adjacent to the last button
                if (
                    abs(button_row - last_button_row) <= 1
                    and abs(button_col - last_button_col) <= 1
                ):
                    self.clicked_buttons.append(button)
                    self.clicked_word += button["text"]

            if self.clicked_word == self.word:
                messagebox.showinfo("Correct", f"Correct word: {self.clicked_word}")
                self.state = "input_letter"  # Reset the state
                self.word = ""  # Reset the word
                self.clicked_word = ""  # Reset the clicked word
                self.clicked_buttons = []  # Reset the clicked buttons list
                self.switch_player()

    def word_exists(self, word):
        if len(word) <= 4:
            return word in self.short_words
        else:
            return word in self.long_words


if __name__ == "__main__":
    app = WordGame()
    app.mainloop()

# Now, there's a scoreboard on the right-hand side of the grid.
# You can add words to the scoreboard_text widget by using the insert method, for example:
# self.scoreboard_text.insert(tk.END, f"{word}\n")
