import unittest
import sys

sys.path.append("..")

from cells_func import cell_neighbors, create_array
from typing import List

# Assuming the cell_neighbors and cell_inside functions are defined here or imported


class TestCellNeighbors(unittest.TestCase):
    def test_cell_neighbors(self):
        test_array: List[List[str]] = [
            ["#", "#", "#", "#", "#"],
            ["#", "A", "#", "B", "#"],
            ["#", "#", "#", "#", "#"],
            ["#", "C", "#", "D", "#"],
            ["#", "#", "#", "#", "#"],
        ]

        empty_char = "#"

        # Test cases
        test_cases = [
            ((1, 1), [("A", [])]),
            ((1, 3), [("B", [])]),
            ((3, 1), [("C", [])]),
            ((3, 3), [("D", [])]),
            ((0, 0), [(empty_char, [(0, 1), (1, 0)])]),
            ((0, 2), [(empty_char, [(0, 1), (0, 3)])]),
            ((2, 0), [(empty_char, [(1, 0), (3, 0)])]),
            ((2, 2), [(empty_char, [])]),
        ]

        for cell, expected_neighbors in test_cases:
            with self.subTest(cell=cell):
                neighbors = cell_neighbors(cell, test_array, empty_char)
                self.assertEqual(len(neighbors), len(expected_neighbors))

                for neighbor, expected_neighbor in zip(neighbors, expected_neighbors):
                    x, y = neighbor
                    self.assertEqual(test_array[x][y], expected_neighbor[0])
                    self.assertIn(neighbor, expected_neighbor[1])


if __name__ == "__main__":
    unittest.main()
