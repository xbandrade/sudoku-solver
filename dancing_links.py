def dlx(board, size=9):
    header = {}
    head = ColumnNode()
    dlx_cols = 324  # 9 rows * 9 columns * 4 conditions
    for i in range(dlx_cols):
        c = ColumnNode(i)
        header[i] = c
        for j in range(size):
            node = DancingNode(c)
            c.link_down(node)
            if j == 0:
                node.down = c
                c.up = node
        if i == 0:
            head.link_right(c)
        else:
            header[i - 1].link_right(c)
        if i == dlx_cols - 1:
            c.right = head
            head.left = c
    for i in range(size * size):
        for j in range(size):
            row_index = row_range(i, size)[j]
            r = find_node(header.get(col_range(row_index, size)[0]), 
                          size, row_index, col_range(row_index, size)[0])
            for k in range(3, 0, -1):
                c = find_node(header.get(col_range(row_index, size)[k]), 
                                size, row_index, col_range(row_index, size)[k])
                r.link_right(c)
                if k == 3:
                    r.left = c
                    c.right = r
    for r in range(size):
        for c in range(size):
            val = board[r, c]
            if val != 0:
                row_index = val + r * size ** 2 + c * size - 1
                for k in range(4):
                    cover(header[col_range(row_index, size)[k]])
    solved = dance(size, head, [], board)
    return solved


def dance(size, head, solution, board):
    if head.right == head:
        for i in solution:
            while i.col.n >= size ** 2:
                i = i.left
            row = i.col.n // size
            column = i.col.n % size
            board[row, column] = i.right.col.n - size ** 2 - row * size + 1
        return True
    c = find_min_col(head, size)
    if c == head: 
        return False
    r = c.down
    cover(c)
    while r != c:
        solution.append(r)
        j = r.right
        while j != r:
            cover(j.col)
            j = j.right
        if dance(size, head, solution, board): 
            return True
        solution.remove(r)
        j = r.left
        while j != r:
            uncover(j.col)
            j = j.left
        r = r.down
    uncover(c)
    return False


def row_range(col_index, size):
    rows = [0] * size
    k = col_index // size ** 2
    if k == 0:
        col = col_index % size
        row = col_index // size
        for i in range(size):
            rows[i] = row * size ** 2 + col * size + i
    elif k == 1:
        col_index -= size ** 2
        row = col_index // size
        val_index = col_index % size
        for c in range(size):
            rows[c] = row * size ** 2 + c * size + val_index
    elif k == 2:
        col_index -= size ** 2 * 2
        col = col_index // size
        val_index = col_index % size
        for r in range(size):
            rows[r] = r * size ** 2 + col * size + val_index
    else:
        col_index -= size ** 2 * 3
        val_index = col_index % size
        box = int(col_index / size)
        box_size = int(size ** 0.5)
        for r in range(box // box_size * box_size, (box // box_size + 1) * box_size):
            for c in range(box % box_size * box_size, (box % box_size + 1) * box_size):
                rows[(r - box // box_size * box_size) * box_size + 
                     (c - box % box_size * box_size)] = r * size ** 2 + c * size + val_index
    return rows


def col_range(row_index, size):
    cols = [0] * 4
    row = row_index // size ** 2
    col = row_index % (size ** 2) // size
    val_index = (row_index % size ** 2) % size
    cols[0] = size * row + col
    cols[1] = size ** 2 + row * size + val_index
    cols[2] = size ** 2 * 2 + col * size + val_index
    cols[3] = size ** 2 * 3 + (row // size ** 0.5 * size ** 0.5 + col // size ** 0.5) * size + val_index
    return cols


def find_node(col, size, row_index, col_index):
    node = col.down
    for i in range(size):
        if row_range(col_index, size)[i] == row_index:
            break
        node = node.down
    return node


def find_min_col(head, size):
    t = head.right
    min = head
    m = size + 1
    while t != head:
        if t.size == 0:
            min = head
            break
        elif t.size < m:
            m = t.size
            min = t
        t = t.right
    return min


def cover(c):
    c.unlink_left_right()
    i = c.down
    while i != c:
        j = i.right
        while j != i:
            j.unlink_up_down()
            j = j.right
        i = i.down


def uncover(c):
    i = c.up
    while i != c:
        j = i.left
        while j != i:
            j.relink_up_down()
            j = j.left
        i = i.up
    c.relink_left_right()


class DancingNode:
    def __init__(self, col=None):
        self.up = self.down = self.left = self.right = self
        self.col = col

    def link_right(self, node):
        node.left = self
        node.right = self.right
        self.right.left = node
        self.right = node

    def link_down(self, node):
        node.up = self
        self.down.up = node
        node.down = self.down
        self.down = node
        self.col.size += 1

    def unlink_left_right(self):
        self.left.right = self.right
        self.right.left = self.left

    def unlink_up_down(self):
        self.up.down = self.down
        self.down.up = self.up
        self.col.size -= 1

    def relink_left_right(self):
        self.left.right = self
        self.right.left = self

    def relink_up_down(self):
        self.up.down = self
        self.down.up = self
        self.col.size += 1


class ColumnNode(DancingNode):
    def __init__(self, n=None):
        super().__init__(self)
        self.size = 0
        self.n = n
