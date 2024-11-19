import pygame

cell_size = 500 / 9

class Cell:
    def __init__(self, row, col, screen, value = 0):
        self.row = row
        self.col = col
        self.screen = screen
        self.value = value

        self.sketched_value = None

    def set_cell_value(self, value):
        self.value = value


    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, cell_selected = False):


        cell_x = self.col * cell_size
        cell_y = self.row * cell_size

        unselected_border = "black"
        selected_border = "red"

        #border will be red if cell (row, col) matches that of the selected cell
        border_color = selected_border if cell_selected else unselected_border

        #cell background
        pygame.draw.rect(self.screen, "white", (cell_x, cell_y, cell_size, cell_size))

        #cell border
        pygame.draw.rect(self.screen, border_color, (cell_x, cell_y, cell_size, cell_size), width=1)

        #draw value in cell
        if self.value != 0:
            pass






class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        #draw 9x9 grid with each square being Cell object
        self.grid = [[Cell(row, col, screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def draw(self):
        # draw cells
        for row in range(9):
            for col in range(9):
                #check if the cell has been selected and pass in whether it has or not to Cell.draw() to determine border color
                cell_selected = self.selected_cell == (row, col)
                self.grid[row][col].draw(cell_selected)


        #draw thick horizontal lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, color = "black", start_pos= (0, i * self.width/3), end_pos=(self.width, i * self.width/3), width = 10)

        #draw thick vertical lines
        for i in range(1, 3):
            pygame.draw.line(self.screen, color="black", start_pos= (i * self.width/3 , 0), end_pos = (i * self.width/3 , self.width), width = 10)

    def select(self, row, col):
        self.selected_cell = (row, col)

    def click(self, x, y):
        #if the x, y position of the click is inside the board, the row is the y coordinate // cell size, column is x-coordinate // cell size
        #if the click is outside the board return None
        if 0 < x < self.width and 0 < y < self.width:
            row = int(y // cell_size)
            col = int(x // cell_size)
            return (row, col)
        return None


    def clear(self):
        pass

    def sketch(self, value):
        pass






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






#         screen.fill("white")
#
#         board.draw()
#
#         pygame.display.flip()
#
# if __name__ == "__main__":
#     main()
