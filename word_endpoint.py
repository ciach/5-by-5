from core_func import my_bad_function
from cells_func import (
    cells_to_play,
    possible_words_list,
)
from words_func import (
    load_words,
    get_current_state_words,
)

from flask import Flask, request, jsonify
import numpy as np
from random import choice

app = Flask(__name__)
short_words, long_words = load_words("rzeczowniki_rm.txt", 4, 10)


@app.route("/get-word", methods=["POST"])
def get_word():
    # Extract my_array and played_words from the incoming JSON request
    data = request.json
    my_array_np = np.char.array(data["my_array"])
    played_words = data["played_words"]

    possible_paths = my_bad_function(my_array_np, cells_to_play(my_array_np, "#"))
    # Check if the game is over (e.g., no cell left on the board)
    if len(possible_paths) == 0:
        return jsonify({"message": "Game Over", "word": None})

    words_dict = possible_words_list(possible_paths, my_array_np)
    current_state_words = get_current_state_words(
        words_dict, played_words, tuple(long_words)
    )

    # Extract a word of maximum length that hasn't been played before
    sorted_current_state_words = sorted(current_state_words, key=lambda x: -x[0])
    max_length = sorted_current_state_words[0][0]
    matching_words = [x for x in sorted_current_state_words if x[0] == max_length]

    next_word_list = choice(matching_words)
    next_word = choice(next_word_list[1])
    next_word_path = next_word_list[2]

    # Making sure the chosen word is not in played_words
    while next_word in played_words:
        next_word_list = choice(matching_words)
        next_word = choice(next_word_list[1])
        next_word_path = next_word_list[2]

    return jsonify({"word": next_word, "path": next_word_path})


if __name__ == "__main__":
    app.run(debug=True)
