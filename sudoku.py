#!/venv/bin/python3
from sudoku_generator import SudokuGenerator
import pygame
from pygame.sprite import Sprite
from BoardandCell import Cell, Board

# mapping actions to buttons, as property:
# https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html

WIDTH, HEIGHT = (500,500)
WHITE=(255, 255, 255)
BLUE=(0, 0, 255)
BLACK=(0, 0, 0)

class STATE: 
    QUIT=-1
    TITLE=0
    GAME=1

def _font(fs): return pygame.font.Font(None, fs)

class Button(Sprite):
    def __init__(self, caption, font, x_pos, y_pos,action, val=None, width=100, height=50):
        self.caption, self.font=caption,font
        self.width, self.height=(100, 50)
        self.x_pos, self.y_pos=x_pos, y_pos
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.action=action
        self.val=val
        self.hover=False #do something with hover ?

    def update(self, mousepos, _up):
        self.hover=True if (col:=self.rect.collidepoint(mousepos)) else False
        if col and _up: return (self.action,self.val) if self.val is not None else self.action

            
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        src=self.font.render(self.caption,True, WHITE)
        dest=src.get_rect(center=self.rect.center)
        surface.blit(src,dest)

def title(screen):
    font=_font(32)
    running=True
    objects= [
        Button("Easy",font, .1*WIDTH, .55*HEIGHT,action=STATE.GAME,val=30), 
        Button("Med.",font, .4*WIDTH, .55*HEIGHT,action=STATE.GAME,val=40), 
        Button("Hard",font, .7*WIDTH, .55*HEIGHT,action=STATE.GAME,val=50)
        ]

    #EVENT HANDLING 
    while running:
        screen.fill("white")
        screen.blit(font.render("Sudoku!", False,BLACK), (.40*WIDTH, .25*HEIGHT))
        screen.blit(font.render("Select Difficulty:", False,BLACK), (.30*WIDTH, .35*HEIGHT))
        mouse_up=False
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False; break
            if event.type == pygame.MOUSEBUTTONUP and event.button:
                mouse_up=True 

        #LOGIC UPDATES
        for obj in objects: 
            _state=obj.update(pygame.mouse.get_pos(), mouse_up)
            if _state!=None and _state[0]!=STATE.TITLE: return _state #i.e., GAME
            obj.draw(screen)

        #DISPLAY
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH,HEIGHT), 1);pygame.display.flip()  
    return STATE.QUIT

def game(screen,dif):
    board=SudokuGenerator(9, dif);board.fill_values();board.remove_cells()
    # get list of values for board and intialize game board with cells, gridlines
    game_board=Board(WIDTH, HEIGHT, screen, board.get_board())

    font,running=_font(32),True
    #clock=pygame.time.Clock()

    objects= [
        Button("Reset",font, .1*WIDTH, .55*HEIGHT,action=STATE.GAME), 
        Button("Restart.",font, .4*WIDTH, .55*HEIGHT,action=STATE.GAME),
        Button("Exit",font, .7*WIDTH, .55*HEIGHT,action=STATE.QUIT)
        ]


    #EVENT HANDLING 
    while running:
        screen.fill("white")
        mouse_up=False
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: running = False; break
            if event.type == pygame.MOUSEBUTTONUP and event.button: mouse_up=True
            if event.type == pygame.MOUSEBUTTONDOWN: game_board.select(*(cell_clicked if (cell_clicked:=game_board.click(event.pos[0], event.pos[1])) is not None else (None,None)))
            # get x, y coordinates of the click and pass them in to Board.click() to get the corresponding row, col ^

        #LOGIC UPDATES
        for obj in objects: 
            _state=obj.update(pygame.mouse.get_pos(), mouse_up)
            if _state is not None and _state!=STATE.GAME: return _state #i.e., QUIT
            obj.draw(screen)
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH,HEIGHT), 1) #window border

        # draw game board after user selects difficulty
        game_board.draw();pygame.display.flip()  

    return STATE.QUIT

def main():
    pygame.init()
    screen,clock,running=pygame.display.set_mode((WIDTH,HEIGHT)),pygame.time.Clock(),True;pygame.display.set_caption("Sudoku!")
    state=STATE.TITLE

    while True:
        if state==STATE.QUIT: pygame.quit();return
        if state==STATE.TITLE: state,dif=title(screen)
        if state==STATE.GAME: clock.tick(60);state=game(screen,dif)


main()
