box_position = dict()
box_number = -1
for c1 in range(0, 9, 3):
    for c2 in range(0, 9, 3):
        box_number += 1
        for p1 in range(c1, c1 + 3):
            for p2 in range(c2, c2 + 3):
                box_position[(p1, p2)] = box_number

# all positions within each 3x3 box
box_list = [[(x, y) for x in range(i, i + 3) for y in range(j, j + 3)]
            for i in range(0, 9, 3) for j in range(0, 9, 3)]

# all positions in rows
row_list = [[(x, y) for y in range(9)] for x in range(9)]

# all position in columns
col_list = [[(x, y) for x in range(9)] for y in range(9)]

# list of empty positions on the starting board
empty_start = []  
