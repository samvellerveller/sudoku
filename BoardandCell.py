import pygame

class Cell:
    CS=500/9
    pygame.init()
    font=pygame.font.Font(None, 30)  

    def __init__(self, row, col, screen, value = 0,cs=500/9):
        self.row = row
        self.col = col
        self.screen = screen
        self.value = value
        self.cs=cs
        self.sketched_value = 0 

    def set_cell_value(self, value): self.value = value
    def set_sketched_value(self, value): self.sketched_value = value
    def draw(self, cell_selected = False):
        cell_x, cell_y = self.col * self.cs, self.row * self.cs 
        pygame.draw.rect(self.screen, "white", (cell_x, cell_y, Cell.CS, Cell.CS)) #cell background
        pygame.draw.rect(self.screen, "red" if cell_selected else "black", (cell_x, cell_y,Cell.CS, Cell.CS), width=1) #cell border
        if self.value != 0: self.screen.blit((src:=Cell.font.render(str(self.value), True, (0,0,0))), \
            dest:=(cell_x+(Cell.CS-src.get_size()[0])//2, cell_y+(Cell.CS-src.get_size()[1])//2))
        if self.sketched_value!= 0: self.screen.blit((src:=Cell.font.render(str(self.sketched_value), True, (128,128,128))), dest:=(cell_x+5, cell_y+5))

class Board:
    def __init__(self, width, height, screen, board):
        self.width,self.height,self.screen,self.board=width,height,screen,board
        self.original_board = [[val for val in row] for row in board]
        self.grid=[[Cell(row,col,self.screen,val) for (col,val) in enumerate(board[row])] for row in range(len(board))]
        self.selected_cell = None

    def draw(self):
        #check if the cell has been selected and pass in whether it has or not to Cell.draw() to determine border color
        for row in range(0,9): [self.grid[row][col].draw(self.selected_cell == (row, col)) for col in range(0,9)]

        #draw thick lines
        for i in range(0, 4): 
            pygame.draw.line(self.screen, color = "black", start_pos= (0,3*Cell.CS*i), end_pos=(self.width, 3*Cell.CS*i), width = 3) # H
            pygame.draw.line(self.screen, color="black", start_pos= (3*Cell.CS*i, 0), end_pos = (3*Cell.CS*i, self.width), width = 3) # V

    def select(self, row, col): self.selected_cell = (row, col) if None not in (row,col) else None

    def click(self, x, y): return (int(y // Cell.CS),int(x // Cell.CS)) if 0 < x < self.width and 0 < y < self.width else None
        #if the x, y position of the click is inside the board, the row is the y coordinate // cell size, column is x-coordinate // cell size
        #if the click is outside the board return None


    def clear(self):
        self.selected_cell.set_sketched_value(0)
    def sketch(self, value): self.grid[self.selected_cell[0]][self.selected_cell[1]].set_sketched_value(value)
    def place(self): 
        self.grid[self.selected_cell[0]][self.selected_cell[1]].value=self.grid[self.selected_cell[0]][self.selected_cell[1]].sketched_value
        self.grid[self.selected_cell[0]][self.selected_cell[1]].set_sketched_value(0)
    def is_full(self): return all([cell.value!=0 for row in self.grid for cell in row])
    def check_board(self):
        b_rows=([[_+(3*(i//3)) for _ in range(3)] for i in range(9)]) # box indexes, zip with box cols
        b_cols=([([(3*(i//3),3+3*(i//3)) for i in range(9)]*3)[g:g+3] for g in range(0,27,3)])
        b_values=[[[j for j in (self.grid[r][cs:ce])] for r,(cs,ce) in zip(R,C)] for R,C in zip(b_rows, b_cols)]
        return self.is_full() and all([set(r)==set([_ for _ in range(1,10)]) for r in self.grid]) and \
        all([[set([self.grid[r][c] for r in [_ for _ in range(9)]])==set([_ for _ in range(1,10)])] for c in range(len(self.grid))]) and \
            all([set([num for row in rows3 for num in row])==set(range(1,10)) for rows3 in b_values]) #checks rows,cols,boxes
    def reset_to_original(self):
        for row_idx, row in enumerate(self.original_board):
            for col_idx, val in enumerate(row):
                self.grid[row_idx][col_idx].set_cell_value(val)
                self.grid[row_idx][col_idx].set_sketched_value(0)
    def update_board(self):
        for i in len(self.board):
            for j in len(i):
                self.board[i][j] = self.grid[i][j].value
#finds empty cells in the grid
    def find_empty(self):
        for row in self.grid:
            for cell in row:
                if cell.value == 0:
                    return cell

# def main():
#     pygame.init()
#
#
#     screen = pygame.display.set_mode((500, 500))
#     board = Board(500, 500, screen, "easy")
#
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 #get x, y coordinates of the click and pass them in to Board.click() to get the corresponding row, col
#                 click_x, click_y = event.pos
#
#                 cell_clicked = board.click(click_x, click_y)
#                 print(cell_clicked)
#
#                 if cell_clicked is not None:
#                 #use cell_clicked to select the cell at row, col
#                     row, col = cell_clicked
#                     board.select(row, col)
#
#
#
#
#
#
#         screen.fill("white")
#
#         board.draw()
#
#         pygame.display.flip()
#
# if __name__ == "__main__":
#     main()





