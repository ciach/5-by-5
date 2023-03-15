import unittest
from typing import List, Tuple

# Assuming the step, cell_neighbors, and cell_inside functions are defined here or imported


class TestStep(unittest.TestCase):
    def test_step(self):
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
            ((1, 1), []),
            ((1, 3), []),
            ((3, 1), []),
            ((3, 3), []),
            ((0, 0), [(0, 1), (1, 0)]),
            ((0, 2), [(0, 1), (0, 3)]),
            ((2, 0), [(1, 0), (3, 0)]),
            ((2, 2), []),
        ]

        for cell, expected_steps in test_cases:
            with self.subTest(cell=cell):
                steps = step(cell, test_array, empty_char)
                self.assertEqual(len(steps), len(expected_steps))

                for step_, expected_step in zip(steps, expected_steps):
                    self.assertEqual(step_, expected_step)


if __name__ == "__main__":
    unittest.main()
