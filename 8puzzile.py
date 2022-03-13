from array import array
import sys
from pygame import *
class State():
    def __init__(self,currentGrid,pastMoves) -> None:
        self.currentGrid = currentGrid
        self.pastMoves = pastMoves

font.init()
pastMoves = list
currentGrid = []
frontier = list
font = font.SysFont("calibri",167)
BLACK = (0,0,0)
GREY = (100,100,100)
WHITE = (255,255,255)

def move(key) -> bool:
    """
    moves the blank tile in the desired direction if it is possible
    
    returns: False if the move can't be played
                 True otherwise
    """
    pass

def initiateGrid():
    """
    takes inut from user to initiate the grid for the first time
    """
    cursor = font.render("_",1,BLACK)
    cell = [rec.x,rec.y]
    drawn = False
    c = 0
    while len(currentGrid) < 9:
        time.Clock().tick(60)
        k = event.get([KEYDOWN,QUIT])
        ts = time.get_ticks()
        while len(k) < 1:
            te = time.get_ticks() - ts
            if not drawn and te > 500:
                screen.blit(cursor,(cell[0]+45,cell[1]))
                display.update()
                drawn = True
                ts = time.get_ticks()
            elif drawn and te > 500:
                redraw()
                drawscreen()
                drawn = False
                ts = time.get_ticks()
            k = event.get([KEYDOWN,QUIT])
        for ev in k:
            if ev.type == QUIT:
                stop()
            elif ev.key < 58 and ev.key > 47 :
                num = ev.key - 48
                if currentGrid.count(num) == 0:
                    currentGrid.append(num)
                    cell[0] += 167
                    c += 1
                    if c == 3:
                        cell[0] = rec.x
                        cell[1] += 167
                        c = 0
        drawn = False
    display.update()

def redraw():
    """
    redraws the basic background elements of the window
    """
    screen.fill((WHITE))
    draw.rect(screen,GREY,rec)
    screen.blit(image.load("Grid.png"),(150,50))
    display.update()

def stop():
    """
    exits the program
    """
    display.quit()
    quit()
    sys.exit()

def drawscreen():
    redraw()
    cell = [rec.x,rec.y]
    c = 0
    for num in currentGrid:
        time.Clock().tick(60)
        if num > 0:
            draw.rect(screen,(WHITE),Rect(cell[0]+10,cell[1]+10,152,152))
            screen.blit(font.render(str(num),1,BLACK),(cell[0]+45,cell[1]+10))
            display.update()
        cell[0] += 167
        c += 1
        if c == 3:
            cell[0] = rec.x
            cell[1] += 167
            c = 0
    for ev in event.get([QUIT,KEYDOWN]):
        if ev.type == QUIT:
            stop()
        elif ev.type == KEYDOWN:
            move(ev.key)
    

init()
screen = display.set_mode((800,600))
rec = Rect(150,50,500,500)
display.set_caption("8puzzle")
initiateGrid()
while True:
    drawscreen()