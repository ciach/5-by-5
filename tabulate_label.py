import tkinter as tk
from tabulate import tabulate
from words_func import (
    calculate_score,
)


class TabulateLabel(tk.Label):
    def __init__(self, parent, player_words, cpu_words, **kwargs):
        super().__init__(parent, justify=tk.LEFT, anchor="nw", **kwargs)

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
