import numpy as np
from random import shuffle, randrange
from sudoku_lists import box_list
from dancing_links import dlx


def generate(diff):
    diff_table = {
        'Easy': (36, 44),
        'Medium': (31, 35),
        'Hard': (24, 28),
        'Expert': (21, 23),
        'Evil': (17, 20),
        'Random': (17, 40),
    }
    new_board = np.array([[0 for _ in range(9)] for _ in range(9)])
    numbers = [k for k in range(1, 10)]
    for b in [0, 4, 8]:
        shuffle(numbers)
        for cell, num in zip(box_list[b], numbers):
            new_board[cell] = num
    dlx(new_board)
    remove_cells = 81 - randrange(diff_table[diff][0], diff_table[diff][1])
    while remove_cells > 0:
        x, y = randrange(0, 9), randrange(0, 9)
        if new_board[x, y] != 0:
            new_board[x, y] = 0
            remove_cells -= 1
    return new_board


if __name__ == '__main__':
    generate()
