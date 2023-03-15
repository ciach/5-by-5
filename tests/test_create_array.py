import sys

sys.path.append("..")
import numpy as np
import unittest
from cells_func import create_array


class TestCreateArray(unittest.TestCase):
    def test_create_array(self):
        # Test Case 1: Check if the function returns a 2D array with the correct shape
        rows = 3
        cols = 4
        empty_char = "#"
        result = create_array(rows, cols, empty_char)
        self.assertEqual(result.shape, (rows, cols))

        # Test Case 2: Check if the array is filled with the correct empty character
        rows = 5
        cols = 5
        empty_char = "#"
        result = create_array(rows, cols, empty_char)
        expected_output = np.full((rows, cols), empty_char, dtype=np.unicode)
        np.testing.assert_array_equal(result, expected_output)

        # Test Case 3: Check if the function correctly handles different empty characters
        rows = 3
        cols = 4
        empty_char = "*"
        result = create_array(rows, cols, empty_char)
        expected_output = np.full((rows, cols), empty_char, dtype=np.unicode)
        np.testing.assert_array_equal(result, expected_output)


if __name__ == "__main__":
    unittest.main()
