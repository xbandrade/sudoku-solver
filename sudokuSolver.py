import sudokuLists
from sudokuLists import *
from itertools import combinations
# from termcolor import colored, cprint

board = []
board_start = []

l9 = list(range(1, 10))  # 1-9 list
empty_pos = []  # list of current empty positions
candidates = {}  # Possible numbers for each empty cell
solved = False  #


def clear_b():
    global board, board_start
    board = [[0 for _ in range(9)] for _ in range(9)]
    board_start = [[0 for _ in range(9)] for _ in range(9)]
    sudokuLists.empty_start = []


def digits_left():
    return sum(board[i][j] == 0 for i in range(9) for j in range(9))


def check_solved():
    """Returns True if there are no empty cells and if all rows, cols and boxes are valid."""
    s = all([board[i][j] != 0 for i in range(9) for j in range(9)])
    return s and check_rows() and check_cols() and check_boxes()


def update_board(step):
    global empty_pos, candidates
    empty_pos = []  # show digit in green if cell is filled in this step
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_pos.append((i, j))
                if step == 1:  # starts dictionary with (cell position): [candidate numbers]
                    candidates[(i, j)] = check_board(i, j)
    if step == 1:
        sudokuLists.empty_start = empty_pos[:]
        # print(sudokuLists.first_pos)


def transpose():
    board_t = [[board[y][x] for y in range(9)] for x in range(9)]
    return board_t


def boxes_list():
    board_s = [[board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)] for i in range(0, 9, 3)
               for j in range(0, 9, 3)]
    return board_s


def check_rows():
    """Runs through rows and returns True if all rows are valid."""
    invalid_rows = []
    for k, lines in enumerate(board):
        line = [n for n in lines if n != 0]
        if len(line) != len(set(line)):
            invalid_rows.append(k)
            # print(f'row {k} is not valid!')
    return len(invalid_rows) == 0


def check_cols():
    """Runs through columns and returns True if all columns are valid."""
    invalid_cols = []
    board_t = transpose()
    for k, lines in enumerate(board_t):
        line = [n for n in lines if n != 0]
        if len(line) != len(set(line)):
            invalid_cols.append(k)
            # print(f'col {k} is not valid!')
    return len(invalid_cols) == 0


def check_boxes():
    """Runs through boxes and returns True if all boxes are valid."""
    invalid_boxes = []
    board_b = boxes_list()
    for k, lines in enumerate(board_b):
        line = [n for n in lines if n != 0]
        if len(line) != len(set(line)):
            invalid_boxes.append(k)
            # print(f'box {k} is not valid!')
    return len(invalid_boxes) == 0


def check_board(x, y):
    """Checks all candidates in position (x, y)"""
    board_t = transpose()
    board_b = boxes_list()
    q = box_position[(x, y)]
    candidates_row = [n for n in l9 if n not in board[x]]  # all numbers missing in the row
    candidates_col = [n for n in l9 if n not in board_t[y]]  # all numbers missing in the column
    candidates_box = [n for n in l9 if n not in board_b[q]]  # all numbers missing in the box
    return [n for n in l9 if n in candidates_row and n in candidates_col and n in candidates_box]


def pop_solved(solved_cells):
    """Pops solved cell from the dictionary of candidates."""
    global candidates
    if len(solved_cells) > 0:
        for item in solved_cells:
            candidates.pop((item[0], item[1]), None)


def update_candidates(solved_pos, digit):
    """Updates candidates in row, column and box of the solved cell."""
    for r in row_list[solved_pos[0]]:
        if r in candidates and digit in candidates[r]:
            candidates[r].remove(digit)
    for c in col_list[solved_pos[1]]:
        if c in candidates and digit in candidates[c]:
            candidates[c].remove(digit)
    for b in box_list[box_position[solved_pos]]:
        if b in candidates and digit in candidates[b]:
            candidates[b].remove(digit)


def naked_single():
    """Checks if there is only one candidate number for an empty cell."""
    solved_cells = []
    for pos in candidates:
        if len(candidates[pos]) == 1:
            board[pos[0]][pos[1]] = candidates[pos][0]
            solved_cells.append((pos[0], pos[1]))
            update_candidates(pos, candidates[pos][0])
    pop_solved(solved_cells)  # pops solved cells from dictionary


def hidden_single():
    """Checks if a number is a candidate for a single cell in a row, column or box."""
    solved_cells = []
    for row in row_list:
        candidate_positions = dict()
        for i in range(1, 10):
            candidate_positions[str(i)] = list()  # (candidate): [positions]
        for pos in row:
            if pos in candidates:  # if cell is empty
                # print(f'{pos}:')
                for i in candidates[pos]:
                    candidate_positions[str(i)].append(pos)
                    # print(i)
        for digit in candidate_positions:
            if len(candidate_positions[digit]) == 1:
                board[candidate_positions[digit][0][0]][candidate_positions[digit][0][1]] = int(digit)
                solved_cells.append((candidate_positions[digit][0][0], candidate_positions[digit][0][1]))
                update_candidates(candidate_positions[digit][0], int(digit))
    for col in col_list:
        candidate_positions = dict()
        for i in range(1, 10):
            candidate_positions[str(i)] = list()
        for pos in col:
            if pos in candidates:  # if cell is empty
                # print(f'{pos}:')
                for i in candidates[pos]:
                    candidate_positions[str(i)].append(pos)
                    # print(i)
        for digit in candidate_positions:
            if len(candidate_positions[digit]) == 1:
                board[candidate_positions[digit][0][0]][candidate_positions[digit][0][1]] = int(digit)
                solved_cells.append((candidate_positions[digit][0][0], candidate_positions[digit][0][1]))
                update_candidates(candidate_positions[digit][0], int(digit))
    for box in box_list:
        candidate_positions = dict()
        for i in range(1, 10):
            candidate_positions[str(i)] = list()
        for pos in box:
            if pos in candidates:  # if cell is empty
                # print(f'{pos}:')
                for i in candidates[pos]:
                    candidate_positions[str(i)].append(pos)
                    # print(i)
        for digit in candidate_positions:
            if len(candidate_positions[digit]) == 1:
                board[candidate_positions[digit][0][0]][candidate_positions[digit][0][1]] = int(digit)
                solved_cells.append((candidate_positions[digit][0][0], candidate_positions[digit][0][1]))
                update_candidates(candidate_positions[digit][0], int(digit))
                # print(f'solved cell: {dict1[d]}')
    pop_solved(solved_cells)


def locked_candidates():
    """If all possible cells for a candidate in a box are in the same row/column,
       deletes that candidate from the rest of the row/column.
       If all possible cells for a candidate in a row/box are in the same box,
       deletes that candidate from the rest of the box. """
    # box
    for i, box in enumerate(box_list):
        # print(f'\nBox {i}:')
        candidates_position = dict()
        for j in range(1, 10):
            candidates_position[str(j)] = list()
        for pos in box:
            if pos in candidates:
                for item in candidates[pos]:
                    candidates_position[str(item)].append(pos)  # stores all positions for each number
                    # print(pos, dict_pos[pos])
        for digit in candidates_position:  # runs through dictionary of positions for each number
            if 2 <= len(candidates_position[digit]) <= 3:
                # print(f'{n} - {dict1[n]} - {len(dict1[n])}')
                # checks if numbers make a column or a row
                is_row = all([candidates_position[digit][0][0] == candidates_position[digit][k][0]
                              for k in range(len(candidates_position[digit]))])
                is_col = all([candidates_position[digit][0][1] == candidates_position[digit][k][1]
                              for k in range(len(candidates_position[digit]))])
                if is_row:
                    # print(f' Number {n} makes a row in box {i}!')
                    for r in row_list[candidates_position[digit][0][0]]:
                        if r not in candidates_position[digit] and r in candidates and int(digit) in candidates[r]:
                            candidates[r].remove(int(digit))
                            # print(r)
                elif is_col:
                    # print(f' Number {n} makes a column in box {i}!')
                    for c in col_list[candidates_position[digit][0][1]]:
                        if c not in candidates_position[digit] and c in candidates and int(digit) in candidates[c]:
                            candidates[c].remove(int(digit))
    # row
    for r, row in enumerate(row_list):
        candidates_position = dict()
        for i in range(1, 10):
            candidates_position[str(i)] = list()
        for pos in row:
            if pos in candidates:  # if cell is empty
                # print(f'{pos}:')
                for item in candidates[pos]:
                    candidates_position[str(item)].append(pos)
                    # print(i)
        for digit in candidates_position:  # runs through numbers 1-9 in dict1
            if 2 <= len(candidates_position[digit]) <= 3:
                l1 = list()
                # print(f'digit {d}: {dict1[d]}')
                for position in candidates_position[digit]:
                    l1.append(box_position[position])
                if len(set(l1)) == 1:  # if all positions of number d are in the same box
                    # print(r, d, l1)
                    for b in box_list[l1[0]]:  # runs through positions in that box and deletes number d
                        if b in candidates and int(digit) in candidates[b] and b not in candidates_position[digit]:
                            # print(dict1[d])
                            candidates[b].remove(int(digit))
                            # print(f'{d} removed from box {l1[0]}!')
                            # pass
    # col
    for c, col in enumerate(col_list):
        candidates_position = dict()
        for i in range(1, 10):
            candidates_position[str(i)] = list()
        for pos in col:
            if pos in candidates:  # if cell is empty
                # print(f'{pos}:')
                for item in candidates[pos]:
                    candidates_position[str(item)].append(pos)
                    # print(i)
        for digit in candidates_position:
            if 2 <= len(candidates_position[digit]) <= 3:
                l1 = list()
                # print(f'digit {d}: {dict1[d]}')
                for position in candidates_position[digit]:
                    l1.append(box_position[position])
                if len(set(l1)) == 1:
                    # print(c, d, l1)
                    for b in box_list[l1[0]]:
                        if b in candidates and int(digit) in candidates[b] and b not in candidates_position[digit]:
                            candidates[b].remove(int(digit))
                            # print(f'{d} removed from box {l1[0]}!')


def naked_subsets(n=2):  # n=2 -> pairs, n=3 -> triples, n=4 -> quads
    """Checks for pairs, triples and quads in the row/column/box and deletes those digits from
        candidates for other cells in the row/column/box"""
    if n < 2 or n > 4:
        print('Invalid n!')
        return
    # row
    for i, row in enumerate(row_list):
        empty_positions = list()
        # print(f'Row {i}')
        for pos in row:
            if pos in candidates:
                empty_positions.append(pos)  # lists all empty cells in row 'i'
        # print(list1)
        combinations_list = list(combinations(empty_positions, n))  # all combinations of n empty cells in the row
        for c in combinations_list:
            set1 = set()
            for p in c:
                set1.update(candidates[p])
            if len(set1) == n:
                # print(f'Found a {["pair", "triple", "quad"][n-2]} in row {i}! {c} - {sorted(set1)}')
                # print(c, set1)
                for item in empty_positions:  # item in list of empty cells in the row
                    if item not in c:  # not a cell that makes the pair
                        for number in set1:  # deletes pair from other cells
                            if number in candidates[item]:
                                candidates[item].remove(number)

    # column
    for i, col in enumerate(col_list):
        empty_positions = list()
        # print(f'Col {i}')
        for pos in col:
            if pos in candidates:
                empty_positions.append(pos)  # lists all empty cells in col 'i'
        # print(list1)
        combinations_list = list(combinations(empty_positions, n))  # all combinations of n empty cells in the column
        for c in combinations_list:
            set1 = set()
            for p in c:
                set1.update(candidates[p])
            if len(set1) == n:
                # print(f'Found a {["pair", "triple", "quad"][n-2]} in col {i}! {c} - {sorted(set1)}')
                # print(c, set1)
                for item in empty_positions:  # item in list of empty cells in the column
                    if item not in c:  # not a cell that makes the pair
                        for number in set1:  # deletes pair from other cells
                            if number in candidates[item]:
                                candidates[item].remove(number)

    # box
    for i, box in enumerate(box_list):
        empty_positions = list()
        # print(f'Box {i}')
        for pos in box:
            if pos in candidates:
                empty_positions.append(pos)  # lists all empty cells in box 'i'
        # print(list1)
        combinations_list = list(combinations(empty_positions, n))  # all combinations of n empty cells in the box
        for c in combinations_list:
            set1 = set()
            for p in c:
                set1.update(candidates[p])
            if len(set1) == n:
                # print(f'Found a {["pair", "triple", "quad"][n-2]} in box {i}! {c} - {sorted(set1)}')
                # print(c, set1)
                for item in empty_positions:  # item in list of empty cells in the box
                    if item not in c:  # not a cell that makes the pair
                        for number in set1:  # deletes pair from other cells
                            if number in candidates[item]:
                                candidates[item].remove(number)


def x_wing():
    # row x-wing
    # list of dictionaries of type 'candidate number': possible positions
    candidates_positions = [{str(n): list() for n in range(1, 10)} for _ in range(9)]
    for k, row in enumerate(row_list):
        for pos in row:
            if pos in candidates:
                for d in candidates[pos]:
                    candidates_positions[k][str(d)].append(pos)
    # for i in list1:
    #     print(i)
    for n in range(1, 10):
        rows_dict = dict()  # dictionary of type 'row': positions, contains rows where the number appears only twice
        for i, d in enumerate(candidates_positions):  # i = row, d = dictionary in row i
            if len(d[str(n)]) == 2:  # if number n appears only in 2 cells
                rows_dict[str(i)] = d[str(n)]  # rows_dict[row i] = cells that contain number n
                # print(f'row {i},', n, d[str(n)])
        # print(rows_dict)
        if len(rows_dict) == 2:  # if the number appears only twice in two rows
            cols = list()
            rows = list()
            for number in rows_dict:
                rows.append(rows_dict[number][0][0])
                rows.append(rows_dict[number][1][0])
                cols.append(rows_dict[number][0][1])
                cols.append(rows_dict[number][1][1])
            if len(set(cols)) == 2:  # checks if the cells are aligned -> it's an X-wing
                # print(f'{n}: {rows_dict}')
                # print(f'Found an X-wing on number {n}!')
                for s in set(cols):
                    # print(s)
                    for c in col_list[s]:
                        if c in candidates and n in candidates[c] and c[0] not in rows:
                            candidates[c].remove(n)

    # col x-wing
    # list of dictionaries of type 'candidate number': possible positions
    candidates_positions = [{str(n): list() for n in range(1, 10)} for _ in range(9)]
    for k, col in enumerate(col_list):
        for pos in col:
            if pos in candidates:
                # print(pos)
                for d in candidates[pos]:
                    candidates_positions[k][str(d)].append(pos)
    # for i in list1:
    #     print(i)
    for n in range(1, 10):
        cols_dict = dict()  # dictionary of type 'col': positions, contains cols where the number appears only twice
        for i, d in enumerate(candidates_positions):  # i = col, d = dictionary in col i
            if len(d[str(n)]) == 2:  # if number n appears only in 2 cells
                cols_dict[str(i)] = d[str(n)]  # cols_dict[col i] = cells that contain number n
                # print(f'col {i},', n, d[str(n)])
        # print(cols_dict)
        if len(cols_dict) == 2:  # if the number appears only twice in two cols
            rows = list()
            cols = list()
            for number in cols_dict:
                rows.append(cols_dict[number][0][0])
                rows.append(cols_dict[number][1][0])
                cols.append(cols_dict[number][0][1])
                cols.append(cols_dict[number][1][1])
            if len(set(rows)) == 2:  # checks if the cells are aligned -> it's an X-wing
                # print(f'{n}: {cols_dict}')
                # print(rows, cols)
                for s in set(rows):
                    for r in row_list[s]:
                        # print(r)
                        if r in candidates and n in candidates[r] and r[1] not in cols:
                            candidates[r].remove(n)


def y_wing():
    possible_pivots = [pos for pos in candidates if len(candidates[pos]) == 2]
    found_wing = False
    for item in possible_pivots:
        rows = []
        cols = []
        boxes = []
        for r in [pos for pos in row_list[item[0]] if pos in candidates and box_position[item] != box_position[pos]]:
            if len(candidates[r]) == 2 and not all([item[k] == r[k] for k in range(2)]):
                if sum(i in candidates[r] for i in candidates[item]) == 1:
                    # print(r, candidates[r])
                    rows.append(r)
        for c in [pos for pos in col_list[item[1]] if pos in candidates and box_position[item] != box_position[pos]]:
            if len(candidates[c]) == 2 and not all([item[k] == c[k] for k in range(2)]):
                if sum(i in candidates[c] for i in candidates[item]) == 1:
                    cols.append(c)
                    # print(c, candidates[c])
        for b in [pos for pos in box_list[box_position[item]] if pos in candidates]:
            if len(candidates[b]) == 2 and not all([item[k] == b[k] for k in range(2)]):
                if sum(i in candidates[b] for i in candidates[item]) == 1:
                    boxes.append(b)
                    # print(b, candidates[b])

        # found candidate squares for the pincers
        if len(rows) > 0:  # row + col or row + box Y-wing
            for r in rows:
                found_wing = False
                common_digit = [x for x in candidates[r] if x in candidates[item]][0]
                # print(' common digit: ', common_digit)
                third_square = [x for x in candidates[r] + candidates[item] if x is not common_digit]
                n = [x for x in third_square if x is not common_digit][0]  # number to be eliminated
                # print(' third square: ', third_square)
                for c in cols:
                    if (c[0], r[1]) in candidates and all(digit in candidates[c] for digit in third_square):
                        # Found a Y-wing: pivot = item, pincer 1 = r, pincer 2 = c
                        # One square seen by both pincers
                        if n in candidates[(c[0], r[1])]:
                            candidates[(c[0], r[1])].remove(n)
                        found_wing = True
                        break  # breaks cols loop
                if not found_wing:
                    for b in boxes:
                        if all(digit in candidates[b] for digit in third_square) and r[0] != b[0]:
                            # Found a Y-wing: pivot = item, pincer 1 = r, pincer 2 = b
                            # print(f'Im here! Found Y-wing: pivot - {item}, pincer 1 - {r}, pincer 2 - {b}')
                            # Six different squares seen by both pincers
                            for p in [q for q in box_list[box_position[b]] if q in row_list[r[0]]]:
                                if p in candidates and n in candidates[p]:
                                    candidates[p].remove(n)
                                    # print(p, candidates[p])
                            for p in [q for q in box_list[box_position[r]] if q in row_list[b[0]]]:
                                if p in candidates and n in candidates[p]:
                                    candidates[p].remove(n)
                                    # print(p, candidates[p])
                            found_wing = True
                            break  # breaks boxes loop
                if found_wing:
                    break  # breaks rows loop
            if found_wing:
                continue  # breaks pivot loop

        if len(cols) > 0:  # row + col or row + box Y-wing
            for c in cols:
                found_wing = False
                common_digit = [x for x in candidates[c] if x in candidates[item]][0]
                # print(' common digit: ', common_digit)
                third_square = [x for x in candidates[c] + candidates[item] if x is not common_digit]
                n = [x for x in third_square if x is not common_digit][0]  # number to be eliminated
                # print(' third square: ', third_square)
                for r in rows:
                    if (c[0], r[1]) in candidates and all(digit in candidates[c] for digit in third_square):
                        # print('Found a Y-wing: pivot = item, pincer 1 = c, pincer 2 = r')
                        # Found a Y-wing: pivot = item, pincer 1 = c, pincer 2 = r'
                        # One square seen by both pincers
                        if n in candidates[(c[0], r[1])]:
                            candidates[(c[0], r[1])].remove(n)
                        found_wing = True
                        break  # breaks rows loop
                if not found_wing:
                    for b in boxes:
                        if all(digit in candidates[b] for digit in third_square) and c[1] != b[1]:
                            # Found a Y-wing: pivot = item, pincer 1 = c, pincer 2 = b
                            # Six different squares seen by both pincers
                            for p in [q for q in box_list[box_position[b]] if q in col_list[c[1]]]:
                                # print(p)
                                if p in candidates and n in candidates[p]:  # pivot does not contain n
                                    candidates[p].remove(n)
                            for p in [q for q in box_list[box_position[c]] if q in col_list[b[1]]]:
                                # print(p)
                                if p in candidates and n in candidates[p]:
                                    candidates[p].remove(n)
                            found_wing = True
                            break  # breaks boxes loop
                if found_wing:
                    break  # breaks col loop
            if found_wing:
                continue  # breaks pivot loop

# def print_board():
#     for i in range(9):
#         for j in range(9):
#             param = None if box_position[(i, j)] % 2 == 0 else 'on_grey'
#             if (i, j) in empty_pos:
#                 if board[i][j] != 0:
#                     cprint(colored(f' {board[i][j]} ', 'green', param), end='')
#                 else:
#                     cprint(colored(' - ', 'red', param), end='')
#             else:
#                 cprint(colored(f' {board[i][j]} ', 'white', param), end='')
#         print('')
#
#
# def print_final():
#     for i in range(9):
#         for j in range(9):
#             param = None if box_position[(i, j)] % 2 == 0 else 'on_grey'
#             if (i, j) in sudokuLists.empty_start:
#                 if board[i][j] != 0:
#                     cprint(colored(f' {board[i][j]} ', 'green', param), end='')
#                 else:
#                     cprint(colored(' - ', 'green', param), end='')
#             else:
#                 cprint(colored(f' {board[i][j]} ', 'yellow', param), end='')
#         print('')


def solver():
    global candidates, solved
    candidates = {}
    solved = False
    k = 1
    double_check = 0
    empty_cells = digits_left()
    while not solved and empty_cells > 0:
        # print(f'\nStep {k}')
        update_board(k)
        naked_single()
        hidden_single()
        for i1 in [2, 3, 4]:  # naked pairs, triples and quads
            naked_subsets(i1)
        locked_candidates()
        x_wing()
        y_wing()
        # TODO: swordfish and coloring techniques
        solved = check_solved()
        k += 1
        if digits_left() == empty_cells:  # no new filled cells, avoids infinite loop
            double_check += 1
            if double_check == 2:
                empty_cells = -1
        else:
            # print_board()
            # print(f'Empty cells: {digits_left()}\n')
            double_check = 0
            empty_cells = digits_left()
    if solved:
        print(f'\nProblem solved!')
        # print(sudokuLists.first_pos)
        # print_final()
        return board
    else:
        # print_board()
        print(f'\nFailed to solve the problem!\n')
        return None
