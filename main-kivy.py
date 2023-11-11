import itertools
import socket
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
    calculate_score,
    get_current_state_words,
)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.core.window import Window


class HoverButton(ButtonBehavior, Label):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)
    # This is just an example color. Adjust as you see fit.
    normal_color = ListProperty([1, 1, 1, 1])  # white
    hover_color = ListProperty([0.8, 0.8, 0.8, 1])  # light gray

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.bind(size=self._trigger_update_graphics, pos=self._trigger_update_graphics)
        self._trigger_update_graphics()

    def on_mouse_pos(self, *args):
        pos = args[1]
        # Check mouse position to determine if mouse is inside the button
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.hovered = inside

    def _trigger_update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.hover_color if self.hovered else self.normal_color)
            Rectangle(pos=self.pos, size=self.size)


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.my_array = []
        self.played_words = []
        self.player_words_list = []
        self.cpu_words_list = []
        self.player_score = 0
        self.cpu_score = 0
        self.turn = "Player"
        self.my_array = create_array(5, 5, "#")
        self.short_words, self.long_words = load_words("rzeczowniki_rm.txt", 4, 10)
        self.grid_buttons = []
        self.player_score_label = Label()
        self.cpu_score_label = Label()
        self.cpu_words = BoxLayout()

    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation="vertical")

        # List to store the button references
        grid = GridLayout(rows=5, cols=5)
        for _ in range(25):
            cell_button = HoverButton(text="", font_size=20, color=(0, 0, 0, 1))
            # pylint: disable=no-member
            cell_button.bind(on_press=self.cell_clicked)
            grid.add_widget(cell_button)
            self.grid_buttons.append(cell_button)  # Add button to the list
        main_layout.add_widget(grid)

        # Buttons: Pass and Restart
        button_layout = BoxLayout(size_hint=(1, 0.1))
        pass_button = Button(text="Pass")
        # pylint: disable=no-member
        pass_button.bind(on_press=self.cpu_move_wrapper)
        # pylint: disable=no-member
        restart_button = Button(text="Restart")
        restart_button.bind(on_press=self.restart_game_wrapper)
        button_layout.add_widget(pass_button)
        button_layout.add_widget(restart_button)
        main_layout.add_widget(button_layout)

        # Score and Turn Labels
        score_layout = BoxLayout(size_hint=(1, 0.2))
        self.player_score_label.text = f"Player Score: {self.player_score}"
        self.cpu_score_label.text = f"CPU Score: {self.cpu_score}"
        self.turn = Label(text="Turn: Player")
        score_layout.add_widget(self.player_score_label)
        score_layout.add_widget(self.cpu_score_label)
        score_layout.add_widget(self.turn)
        main_layout.add_widget(score_layout)

        # Word Lists with headers
        words_layout = BoxLayout()

        # Player Words Column
        self.player_words = BoxLayout(orientation="vertical", spacing=5)
        player_header = Label(
            text="Player Words", size_hint_y=None, height=44, bold=True
        )
        self.player_words.add_widget(player_header)
        words_layout.add_widget(self.player_words)

        # CPU Words Column
        self.cpu_words = BoxLayout(orientation="vertical", spacing=5)
        cpu_header = Label(text="CPU Words", size_hint_y=None, height=44, bold=True)
        self.cpu_words.add_widget(cpu_header)
        words_layout.add_widget(self.cpu_words)

        main_layout.add_widget(words_layout)

        self.initialize_game()

        return main_layout

    def cell_clicked(self, instance):
        # This function gets triggered when a cell is clicked
        print(f"{instance.text} was clicked!")
        # Add additional logic here as needed

    def initialize_game(self):
        # Clear the board and played words
        self.my_array = create_array(5, 5, "#")
        self.played_words.clear()

        # Reset player and CPU scores
        self.player_score = 0
        self.cpu_score = 0

        # Reset the player and CPU word lists
        self.player_words_list.clear()
        self.cpu_words_list.clear()

        # Clear the grid buttons
        for button in self.grid_buttons:
            button.text = ""
            button.disabled = False

        first_word = start_word(
            5, self.long_words
        )  # Getting a 5-letter word for initialization
        set_first_word(self.my_array, first_word, "horizontal")
        self.played_words.append(first_word.lower())
        start_row = 2
        start_col = 0

        for i, letter in enumerate(first_word):
            # Calculate index for the grid_buttons list
            index = start_row * 5 + (start_col + i)
            self.grid_buttons[index].text = letter.upper()
            self.grid_buttons[index].disabled = False

        self.update_scoreboard()

    def update_scoreboard(self):
        # Clear previous entries
        for widget in self.player_words.children[:]:
            self.player_words.remove_widget(widget)
        for widget in self.cpu_words.children[:]:
            self.cpu_words.remove_widget(widget)

        # Add back the headers
        player_header = Label(
            text="Player Words", size_hint_y=None, height=44, bold=True
        )
        self.player_words.add_widget(player_header)
        cpu_header = Label(text="CPU Words", size_hint_y=None, height=44, bold=True)
        self.cpu_words.add_widget(cpu_header)

        # Add player words and scores
        for word in self.player_words_list:
            score = calculate_score(word)
            entry = Label(
                text=f"{word} - {score}",
                size_hint_y=None,
                height=44,
                valign="top",
                halign="left",
                text_size=(self.player_words.width, None),
            )
            self.player_words.add_widget(entry)

        # Add a stretching widget to push words to the top
        self.player_words.add_widget(Widget())

        # Add CPU words and scores
        for word in self.cpu_words_list:
            score = calculate_score(word)
            entry = Label(text=f"{word} - {score}")
            self.cpu_words.add_widget(entry)

        # Add a stretching widget to push words to the top
        self.cpu_words.add_widget(Widget())

    def update_valid_cells(self):
        # Then enable only the valid cells
        valid_cells = cells_to_play(self.my_array, "#")
        for i, j in valid_cells:
            index = i * 5 + j
            self.grid_buttons[index].disabled = False

        # Check if the game is over (e.g., no empty cell left on the board)
        empty_cells = sum(
            self.my_array[i][j] == "#" for i, j in itertools.product(range(5), range(5))
        )
        if empty_cells == 0:
            self.update_scoreboard()
            self.announce_winner()

    def announce_winner(self):
        # Determine the winner
        if self.player_score > self.cpu_score:
            winner_message = "Congratulations! You won!"
        elif self.player_score < self.cpu_score:
            winner_message = "Sorry! The computer won. Better luck next time."
        else:
            winner_message = "It's a tie!"

        # Create a popup to show the winner announcement
        popup = Popup(
            title="Game Over", content=Label(text=winner_message), size_hint=(0.8, 0.4)
        )
        popup.open()

        self.restart_game()

    def restart_game(self):
        """Handle restart game event."""
        self.initialize_game()
        self.update_valid_cells()

    def restart_game_wrapper(self, _):
        """Wrapper function to handle restart button press."""
        self.restart_game()

    def cpu_move(self):
        self.turn.text = "Turn: CPU"

        """Handle pass turn event (CPU's play)."""
        possible_paths = my_bad_function(
            self.my_array, cells_to_play(self.my_array, "#")
        )
        # Check if the game is over (e.g., no cell left on the board)
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

        # Making sure the chosen word is not in played_words
        while next_word in self.played_words:
            next_word_list = choice(matching_words)
            next_word = choice(next_word_list[1])

        for letter, position in zip(next_word, next_word_list[2]):
            add_letter(self.my_array, letter, position[0], position[1])
            index = position[0] * 5 + position[1]
            self.grid_buttons[
                index
            ].text = letter.upper()  # Update the button text in Kivy

        self.played_words.append(next_word)
        self.cpu_words_list.append(next_word)
        self.cpu_score += calculate_score(next_word)

        # Assuming you have a Label widget to display the CPU's score:
        self.cpu_score_label.text = f"CPU Score: {self.cpu_score}"

        self.update_valid_cells()
        self.update_scoreboard()

    def cpu_move_wrapper(self, _):
        """Wrapper function to handle the 'Pass' button press."""
        self.cpu_move()


if __name__ == "__main__":
    MainApp().run()
