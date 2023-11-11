import pytest
from cells_func import cell_inside


@pytest.mark.parametrize(
    "cell, rows_, cols_, expected",
    [
        ((0, 0), 5, 5, True),  # Cell at the top-left corner
        ((4, 4), 5, 5, True),  # Cell at the bottom-right corner
        ((2, 2), 5, 5, True),  # Cell in the middle
        ((-1, 2), 5, 5, False),  # Cell with negative X position
        ((2, -1), 5, 5, False),  # Cell with negative Y position
        ((5, 2), 5, 5, False),  # Cell with X position exceeding rows
        ((2, 5), 5, 5, False),  # Cell with Y position exceeding columns
        ((0, 0), 0, 0, False),  # Empty array
        ((0, 0), 0, 5, False),  # Empty rows
        ((0, 0), 5, 0, False),  # Empty columns
    ],
)
def test_cell_inside(cell, rows_, cols_, expected):
    assert cell_inside(cell, rows_, cols_) == expected
