
import pygame


class Cell:
   CS=500/9
   pygame.init()
   font=pygame.font.Font(None, 30)
   #ITITIALIZES
   def __init__(self, row, col, screen, value = 0,cs=500/9):
       self.row = row
       self.col = col
       self.screen = screen
       self.value = value
       self.cs=cs
       self.sketched_value = 0


   # SETS CELL VALUE
   def set_cell_value(self, value): self.value = value
   # SETS SKETCHED VALUE
   def set_sketched_value(self, value): self.sketched_value = value
   # DRAWS CELL WITH VALUE
   def draw(self, cell_selected = False):
       cell_x, cell_y = self.col * self.cs, self.row * self.cs
       pygame.draw.rect(self.screen, "white", (cell_x, cell_y, Cell.CS, Cell.CS)) #cell background
       pygame.draw.rect(self.screen, "red" if cell_selected else "black", (cell_x, cell_y,Cell.CS, Cell.CS), width=1) #cell border
       if self.value != 0: self.screen.blit((src:=Cell.font.render(str(self.value), True, (0,0,0))), \
           dest:=(cell_x+(Cell.CS-src.get_size()[0])//2, cell_y+(Cell.CS-src.get_size()[1])//2))
       if self.sketched_value!= 0: self.screen.blit((src:=Cell.font.render(str(self.sketched_value), True, (128,128,128))), dest:=(cell_x+5, cell_y+5))

class Board:
   # INITIALIZES
   def __init__(self, width, height, screen, board):
       self.width,self.height,self.screen,self.board=width,height,screen,board
       self.grid=[[Cell(row,col,self.screen,val) for (col,val) in enumerate(board[row])] for row in range(len(board))]
       self.original_board = [[val for val in row] for row in board]
       self.selected_cell = None
       self.initial_cell = []
       for i, row in enumerate(board):
           for j, value in enumerate(row):
                  if value != 0:
                      self.initial_cell.append((i, j))


   def draw(self):
       #check if the cell has been selected and pass in whether it has or not to Cell.draw() to determine border color
       for row in range(0,9): [self.grid[row][col].draw(self.selected_cell == (row, col)) for col in range(0,9)]

       #draw thick lines
       for i in range(0, 4):
           pygame.draw.line(self.screen, color = "black", start_pos= (0,3*Cell.CS*i), end_pos=(self.width, 3*Cell.CS*i), width = 3) # H
           pygame.draw.line(self.screen, color="black", start_pos= (3*Cell.CS*i, 0), end_pos = (3*Cell.CS*i, self.width), width = 3) # V

   # MARKS THE CELL
   def select(self, row, col):
       self.selected_cell = (row, col) if None not in (row, col) else None

   # RETURNS A TUPLE OR NONE
   def click(self, x, y): return (int(y // Cell.CS),int(x // Cell.CS)) if 0 < x < self.width and 0 < y < self.width else None
       #if the x, y position of the click is inside the board, the row is the y coordinate // cell size, column is x-coordinate // cell size
       #if the click is outside the board return None

   # CLEARS VALUE CELL
   def clear(self):
       if self.selected_cell is not None:
           self.selected_cell.set_sketched_value(0)
   # SETS THE SKETCH VALUE
   def sketch(self, value):
          if self.selected_cell in self.initial_cell:
               pass
          else:
               self.grid[self.selected_cell[0]][self.selected_cell[1]].set_sketched_value(value)
   # SETS VALUE
   def place(self):
       if self.selected_cell in self.initial_cell:
           pass
       else:
           self.grid[self.selected_cell[0]][self.selected_cell[1]].value=self.grid[self.selected_cell[0]][self.selected_cell[1]].sketched_value
           self.grid[self.selected_cell[0]][self.selected_cell[1]].set_sketched_value(0)

   # CHECKS IF BOARD IS FULL
   def is_full(self): return all([cell.value!=0 for row in self.grid for cell in row])

   # CHECKS IF BOARD IS FILLED OUT CORRECTLY
   def check_board(self):
       # row indexes, zip with col indexes
       # find whether to start at 1st/2nd/3rd group of rows (top boxes are in 1st group) then add row number to get row 0-8
       b_rows = [[3 * (i // 3) + row for row in range(3)] for i in range(9)]
       # col indexes
       # iterate over each box and find its column indexes (0,1,2 for top left, 3,4,5 for center top, etc)
       b_cols = [[3 * (i // 3) + j for j in range(3)] for i in range(9)]

       # values in each box starting from top left box
       b_values = [[int(self.grid[r][c].value) for r in row for c in col] for row, col in zip(b_rows, b_cols)]

       # check each row to make sure there are numbers 1-9 with no duplicates
       row_check = all(set(int(cell.value) for cell in row) == set(range(1, 10)) for row in self.grid)
       # check columns for numbers 1-9, no duplicates
       col_check = all(set(int(self.grid[r][c].value) for r in range(9)) == set(range(1, 10)) for c in range(9))
       # check each box for numbers 1-9, no duplicates
       box_check = all(set(box) == set(range(1, 10)) for box in b_values)
       return self.is_full() and row_check and col_check and box_check
   # RESET BOARD TO ORIGINAL
   def reset_to_original(self):
       for row_idx, row in enumerate(self.original_board):
           for col_idx, val in enumerate(row):
               self.grid[row_idx][col_idx].set_cell_value(val)
               self.grid[row_idx][col_idx].set_sketched_value(0)
   # UPDATES BOARD
   def update_board(self):
       for i in len(self.board):
           for j in len(i):
               self.board[i][j] = self.grid[i][j].value
   # FINDS AN EMPTY CELL
   def find_empty(self):
       for row in self.grid:
           for cell in row:
               if cell.value == 0:
                   return cell