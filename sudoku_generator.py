#!/usr/bin/python3
import math, random


class SudokuGenerator:
    # INITIALIZES
    def __init__(self, row_len, rem):
        self.rows = self.cols = self.row_len = self.col_len = row_len
        self.board = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self.box_len = int(math.sqrt(self.rows))
        self.rem = rem

# DEF FUNCTIONS

    # GET BOARD
    def get_board(self) -> list[list]:
        return self.board

    # PRINTS BOARD
    def print_board(self):
        for r in self.board: print(r)
        print('------')

    # RETURNS BOOL (DEPENDS ON IF VALID IN ROW)
    def valid_in_row(self, row, num) -> bool:
        return False if num in self.board[row] else True

    # RETURNS BOOL (DEPENDS ON IF VALID IN COL)
    def valid_in_col(self, col, num) -> bool:
        return False if num in [self.board[r][col] for r in range(0, self.row_len)] else True

    # RETURNS BOOL (DEPENDS ON IF VALID IN BOX)
    def valid_in_box(self, row_start, col_start, num):
        return False if num in [n for row in [self.board[r][c:c + 3] for r, c in
                                              zip(range(row_start, row_start + 3), (col_start,) * 3)] for n in
                                row] else True


    def is_valid(self, row, col, num):
        return all((self.valid_in_row(row, num), self.valid_in_col(col, num),
                    self.valid_in_box(row // self.box_len * self.box_len, col // self.box_len * self.box_len, num)))

    def fill_box(self, row_start, col_start):
        rs, re, cs, ce = row_start, row_start + 3, col_start, col_start + 3
        for r in range(rs, re):
            for c in range(cs, ce):
                while 1:
                    if self.valid_in_box(rs, cs, n := random.randint(1, 9)):
                        self.board[r][c] = n
                        break

    def fill_diagonal(self):
        for s in range(0, self.row_len, self.box_len):
            self.fill_box(s, s)

    def fill_remaining(self, r, c):
        if r < self.row_len - 1 and c == self.row_len: r, c = r + 1, 0  # row end
        if r == self.row_len - 1 and c == self.row_len: return True  # board end
        if self.board[r][c] != 0: return self.fill_remaining(r, c + 1)  # next col
        if r < self.box_len and c < self.box_len:
            c = self.box_len  # when r,c in first diagonal, c->second box [r,3]
        elif r < self.row_len - self.box_len and c == r // self.box_len * self.box_len:
            c += self.box_len  # when r,c in second diagonal, c->third box [r,6]
        elif r >= self.row_len - self.box_len and c == self.row_len - self.box_len:  # last diagonal is already generated, move to next row + base check
            r, c = r + 1, 0
            if r == self.row_len: return True
        for n in range(1, 10):
            if valid := self.is_valid(r, c, n):
                self.board[r][c] = n
                if self.fill_remaining(r, c + 1): return True
                self.board[r][c] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_len)

    def remove_cells(self):
        idx = []
        for _ in range(self.rem):
            while 1:
                i, j = random.randint(0, 8), random.randint(0, 8);
                if (i, j) not in idx: idx.append((i, j));break
        for (i, j) in idx: self.board[i][j] = 0
        return idx