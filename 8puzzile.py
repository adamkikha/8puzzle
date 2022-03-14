from array import array
from ast import Compare, Return
from random import randint
import sys
from pygame import *
class State():
    def __init__(self,currentGrid,pastMoves) -> None:
        self.currentGrid = currentGrid
        self.pastMoves = pastMoves

goal = [0,1,2,3,4,5,6,7,8]
pastMoves = list
currentGrid = []
frontier = list
font.init()
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
    moved = False
    blank = currentGrid.index(0)
    num = 0
    if key == K_UP:
        if blank - 3 > -1:
            num = blank - 3
            swap(blank,num)
            moved = True
    if key == K_DOWN: 
        if blank + 3 < 9:
            num = blank + 3
            swap(blank,num)
            moved = True
    if blank < 3:
        if key == K_LEFT:
            if blank - 1 > -1:
                num = blank - 1
                swap(blank,num)
                moved = True
        if key == K_RIGHT:
            if blank + 1 < 3:
                num = blank + 1
                swap(blank,num)
                moved = True
    elif blank < 6:
        if key == K_LEFT:
            if blank - 1 > 2:
                num = blank - 1
                swap(blank,num)
                moved = True
        if key == K_RIGHT:
            if blank + 1 < 6:
                num = blank + 1
                swap(blank,num)
                moved = True
    elif blank < 9:
        if key == K_LEFT:
            if blank - 1 > 5:
                num = blank - 1
                swap(blank,num)
                moved = True
        if key == K_RIGHT:
            if blank + 1 < 9:
                num = blank + 1
                swap(blank,num)
                moved = True
    if moved:
        drawGrid(num,blank)
        return True
    return False


def initiateGrid():
    """
    takes input from user to initiate the grid for the first time
    """
    cursor = font.render("_",1,BLACK)
    cell = [rec.x,rec.y]
    c = 0
    drawBG()
    while len(currentGrid) < 9:
        time.Clock().tick(60)
        k = event.get([KEYDOWN,QUIT])
        while len(k) < 1:
            screen.blit(cursor,(cell[0]+45,cell[1]))
            display.update()
            k = event.get([KEYDOWN,QUIT])
        for ev in k:
            if ev.type == QUIT:
                stop()
            elif ev.key < 57 and ev.key > 47 :
                num = ev.key - 48
                if currentGrid.count(num) == 0:
                    currentGrid.append(num)
                    cell[0] += 167
                    c += 1
                    if c == 3:
                        cell[0] = rec.x
                        cell[1] += 167
                        c = 0
            drawIncGrid()

def drawBG():
    """
    redraws the basic background elements of the window
    """
    draw.rect(screen,GREY,rec)
    screen.blit(grid,(150,50))
    display.update()

def stop():
    """
    exits the program
    """
    display.quit()
    quit()
    sys.exit()

#randint([0:8])

def drawIncGrid():
    cell = [rec.x,rec.y]
    c = 0
    for num in currentGrid:
        time.Clock().tick(60)
        tile = Rect(cell[0]+10,cell[1]+10,152,152)
        if num > 0:
            text = font.render(str(num),1,BLACK)
            draw.rect(screen,(WHITE),tile)
            screen.blit(text,(cell[0]+45,cell[1]+10))
        else:
            draw.rect(screen,(BLACK),tile)
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
        elif ev.type == KEYDOWN and len(currentGrid) == 9:
            move(ev.key)
            
def drawGrid(blank: int,num: int) -> None:
    cellb = [rec.x , rec.y]
    celln = [rec.x , rec.y]
    text = font.render(str(currentGrid[num]),1,BLACK)
    while blank > 2:
        cellb[1] += 167
        blank -= 3
    while blank > 0:
        cellb[0] += 167
        blank -= 1
    while num > 2:
        celln[1] += 167
        num -= 3
    while num > 0:
        celln[0] += 167
        num -= 1
    draw.rect(screen,(WHITE),Rect(celln[0]+10,celln[1]+10,152,152))
    screen.blit(text,(celln[0]+45,celln[1]+10))
    draw.rect(screen,(BLACK),Rect(cellb[0]+10,cellb[1]+10,152,152))
    display.update()

def swap(a: int,b: int) -> None:
    currentGrid[a] , currentGrid[b] = currentGrid[b] , currentGrid[a]

def win():
    i = 0
    j = 255
    k = 150
    bg = (0,0,0)
    while True:
        screen.fill((bg))
        time.wait(200)
        display.update()
        i = (1 + i) % 255
        j = (1 + j) % 255
        k = (1 + k) % 255
        bg = (i,j,k) 
        for ev in event.get(QUIT):
            stop()

init()
screen = display.set_mode((800,600))
rec = Rect(150,50,500,500)
grid = image.load("Grid.png").convert_alpha()
display.set_caption("8puzzle")
screen.fill((WHITE))
initiateGrid()
while True:
    time.Clock().tick(60)
    won = True
    i = 0   
    while i < 9:
        if currentGrid[i] != goal[i]:
            won = False
            break
    if won:
        win()
    for ev in event.get([QUIT,KEYDOWN]):
        if ev.type == QUIT:
            stop()
        elif ev.type == KEYDOWN and len(currentGrid) == 9:
            move(ev.key)