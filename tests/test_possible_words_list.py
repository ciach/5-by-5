import sys

sys.path.append("..")

import unittest
from cells_func import possible_words_list, create_array


class TestPossibleWordsList(unittest.TestCase):
    def test_possible_words_list(self):
        # Test Case 1: Check if the function returns the correct word and path
        paths_list = [[(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0)]]
        my_array = create_array(3, 1, "#")
        my_array[0][0] = "A"
        my_array[1][0] = "B"
        expected_output = {"AB#": [(0, 0), (1, 0), (2, 0)]}
        self.assertEqual(possible_words_list(paths_list, my_array), expected_output)

        # Test Case 2: Check if the function returns an empty dictionary
        # when there are no possible words
        paths_list = [[(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0)]]
        my_array = create_array(3, 1, "#")
        my_array[0][0] = "A"
        my_array[1][0] = "B"
        my_array[2][0] = "C"
        expected_output = {}
        self.assertEqual(possible_words_list(paths_list, my_array), expected_output)

        # Test Case 3: Check if the function correctly handles multiple possible words
        paths_list = [[(0, 0), (1, 0)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 0)]]
        my_array = create_array(3, 1, "#")
        my_array[1][0] = "B"
        my_array[2][0] = "C"
        expected_output = {"#BC": [(0, 0), (1, 0), (2, 0)], "#B": [(0, 0), (1, 0)]}
        self.assertEqual(possible_words_list(paths_list, my_array), expected_output)


if __name__ == "__main__":
    unittest.main()
