# all positions within each 3x3 box
box_list = [[(x, y) for x in range(i, i + 3) for y in range(j, j + 3)]
            for i in range(0, 9, 3) for j in range(0, 9, 3)]

# all positions in rows
row_list = [[(x, y) for y in range(9)] for x in range(9)]

# all position in columns
col_list = [[(x, y) for x in range(9)] for y in range(9)]

# list of empty positions on the starting board
empty_start = []  
