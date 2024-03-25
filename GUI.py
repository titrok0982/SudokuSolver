from solver import valid, find_empty, solve
import pygame
pygame.init()
import time


class Grid:
    board = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]


    
    def __init__(self, rows, cols, width, height, win, board=None):
        self.rows = rows
        self.cols = cols
        if board is not None:
            self.board=board
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win
        solve(self.board)
    
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            if self.board[row][col] == val:
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
    def sketch(self,val):
        row,col = self.selected
        self.cubes[row][col].set_temp(val)
    
    def draw(self):
        gap = self.width / 9
        
        for i in range(self.rows+1):
            thick = 4 if (i % 3 == 0 and i != 0) else 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)    
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
    
    def select(self, row, col):
        if self.selected:
            self.cubes[self.selected[0]][self.selected[1]].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)
    
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None
        
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    
    def solve(self, gui=False):
        self.update_model()
        next_empty = find_empty(self.model)
        if next_empty == (-1,-1):
            return True
        
        row, col = next_empty[0], next_empty[1]
        for possibility in range(1,10):
            if valid(possibility, self.model, row, col):
                self.model[row][col] = possibility
                if (gui):
                    self.cubes[row][col].set(possibility)
                    self.cubes[row][col].draw_change(self.win, True)
                    self.update_model()
                    pygame.display.update()
                    pygame.time.delay(20)

                if self.solve(gui):
                    return True
                
                self.model[row][col] = 0
                if gui:
                    self.cubes[row][col].set(0)
                    self.update_model()
                    self.cubes[row][col].draw_change(self.win, False)
                    pygame.display.update()
                    pygame.time.delay(20)

        return False

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x+(gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x,y, gap, gap), 3)
    
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x+(gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        color = (0, 255, 0) if g else (255, 0, 0)
        pygame.draw.rect(win, color, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val

def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 40)
    fmt_time = format_time(time)
    time_text = fnt.render("Time : " + fmt_time, 1, (0, 0, 0))
    win.blit(time_text, (315, 540))
    strikes_text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(strikes_text, (20, 560))
    board.draw()

def format_time(seconds):
    formated = " " + str(seconds//60) + ":"
    if seconds % 60 < 10:
        formated += "0" + str(seconds%60)
    else :
        formated += str(seconds%60)
    return formated

def main(board=None):
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win, board)
    key = None
    run = True
    timer = True
    start = time.time()
    strikes = 0
    while run:
        if (timer):
            play_time = round(time.time()-start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_1 | pygame.K_KP1:
                        key = 1
                    case pygame.K_2 | pygame.K_KP2:
                        key = 2
                    case pygame.K_3 | pygame.K_KP3:
                        key = 3
                    case pygame.K_4 | pygame.K_KP4:
                        key = 4
                    case pygame.K_5 | pygame.K_KP5:
                        key = 5
                    case pygame.K_6 | pygame.K_KP6:
                        key = 6
                    case pygame.K_7 | pygame.K_KP7:
                        key = 7
                    case pygame.K_8 | pygame.K_KP8:
                        key = 8
                    case pygame.K_9 | pygame.K_KP9:
                        key = 9
                    
                    case pygame.K_DELETE:
                        board.clear()
                        key = None
                    
                    case pygame.K_SPACE:
                        board.solve(True)

                    case pygame.K_RETURN | pygame.K_KP_ENTER:
                        i, j = board.selected
                        if board.cubes[i][j].temp != 0:
                            if board.place(board.cubes[i][j].temp):
                                print("Success")
                            else:
                                print("Wrong")
                                strikes += 1
                            key = None

                            if board.is_finished():
                                print("Game over")
        if board.selected and key != None:
            board.sketch(key)                    
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()
    pygame.quit()