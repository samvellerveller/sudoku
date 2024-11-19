#!/usr/bin/python3

import math,random

class SudokuGenerator:
    def __init__(self, row_len, removed_cells):
		self.rows=self.cols=self.row_len=self.col_len=row_len
		self.board= [[0 for _ in range(self.rows)] for _ in range(self.cols)]
		self.box_len=int(math.sqrt(self.rows))

    def get_board(self)->list[list]:
		# get nums as 2d-array
        pass

    def print_board(self):
        pass


    def valid_in_row(self, row, num)->bool:
		# if num in specified row (index) 
        pass
	
    def valid_in_col(self, col, num):
		# if num in specified col (index) 
        pass


    def valid_in_box(self, row_start, col_start, num):
		# if num in specified box (index) 
        pass
    

    def is_valid(self, row, col, num):
		# will use the above 3 methods
        pass


    def fill_box(self, row_start, col_start):
		rs,re,cs,ce=row_start, row_start+2,col_start,col_start+2
		for r in range(rs,re):
			for c in range(cs,ce):
				self.board[r][c]=random.randint(1,10)
    

    def fill_diagonal(self):
		for s in range(0, self.row_len, self.box_len):
			self.fill_box(s, s)

    '''
    Should be called after the diagonal boxes have been filled
	row, col specify the coordinates of the first empty (0) cell
	returns boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False


    def fill_values(self):
	#creates solution
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
    #Removes the appropriate number of cells from the board, uses 0 as place-holder
        pass


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
