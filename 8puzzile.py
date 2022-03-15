from random import randint
import sys
from tkinter import messagebox
from pygame import *
from SearchAgent import *
import tkinter

def move(key) -> bool:
    """
    moves the blank tile in the desired direction if it is possible
    and appends it to state.pastMoves
    returns: False if the move can't be played
                 True otherwise
    """
    moved = False
    blank = state.grid.index(0)
    num = 0
    if key == K_UP:
        if blank - 3 > -1:
            num = blank - 3
            switchState(blank,num)
            moved = True
    elif key == K_DOWN: 
        if blank + 3 < 9:
            num = blank + 3
            switchState(blank,num)
            moved = True
    elif blank < 3:
        if key == K_LEFT:
            if blank - 1 > -1:
                num = blank - 1
                switchState(blank,num)
                moved = True
        elif key == K_RIGHT:
            if blank + 1 < 3:
                num = blank + 1
                switchState(blank,num)
                moved = True
    elif blank < 6:
        if key == K_LEFT:
            if blank - 1 > 2:
                num = blank - 1
                switchState(blank,num)
                moved = True
        elif key == K_RIGHT:
            if blank + 1 < 6:
                num = blank + 1
                switchState(blank,num)
                moved = True
    elif blank < 9:
        if key == K_LEFT:
            if blank - 1 > 5:
                num = blank - 1
                switchState(blank,num)
                moved = True
        elif key == K_RIGHT:
            if blank + 1 < 9:
                num = blank + 1
                switchState(blank,num)
                moved = True
    if moved:
        state.pastMoves.append[key]
        drawSwap(num,blank)
        return True
    return False

def initiateGrid(option: int = 0):
    """
    takes input from user or uses a rng to initiate the grid for the first time
    """
    cursor = fnt.render("_",1,BLACK)
    cell = [rec.x,rec.y]
    c = 0
    draw.rect(screen,GREY,rec)
    screen.blit(grid,(150,50))
    tempGrid = []
    while len(tempGrid) < 9:
        time.Clock().tick(60)
        k = event.get([KEYDOWN,QUIT])
        screen.blit(cursor,(cell[0]+45,cell[1]))
        display.update()
        while len(k) < 1:
            k = event.get([KEYDOWN,QUIT])
        for ev in k:
            if ev.type == QUIT:
                stop()
            elif ev.key < 57 and ev.key > 47 :
                num = ev.key - 48
                if tempGrid.count(num) == 0:
                    tempGrid.append(num)
                    drawTile(cell,num)
                    cell[0] += 167
                    c += 1
                    if c == 3:
                        cell[0] = rec.x
                        cell[1] += 167
                        c = 0
    global state
    state = State(tuple(tempGrid),tempGrid.index(0),[])  
    state.isExplored()                  

def stop():
    """
    exits the program
    """
    display.quit()
    quit()
    sys.exit()

#randint([0:8])

def drawTile(cell,num):
    tile = Rect(cell[0]+10,cell[1]+10,152,152)
    if num > 0:
        text = fnt.render(str(num),1,BLACK)
        draw.rect(screen,(WHITE),tile)
        screen.blit(text,(cell[0]+45,cell[1]+10))
    else:
        draw.rect(screen,(GREY),tile)
    display.update()
    
def drawSwap(blank: int,num: int) -> None:
    cellb = [rec.x , rec.y]
    celln = [rec.x , rec.y]
    text = fnt.render(str(state.grid[num]),1,BLACK)
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
    draw.rect(screen,(GREY),Rect(cellb[0]+10,cellb[1]+10,152,152))
    display.update()

def switchState(blank: int,num: int) -> None:
    global state 
    l = list(state.grid)
    l[blank] , l[num] = l[num] , l[blank]
    state = State(tuple(l),state.pastMoves,num)
    if state.isExplored():
        messagebox.showwarning("RAKEZ!","El3ab 3edel enta kont hena abl keda")
def won():
    i = 0
    j = 200
    k = 100
    bg = (0,0,0)
    fnt = font.SysFont("calibri",65)
    while True:
        screen.fill((bg))
        screen.blit(fnt.render("MABROOOOK YA KOSOMAK!!!",1,BLACK),(0,250))
        display.update()
        time.wait(6)
        i = (1 + i) % 255
        j = (1 + j) % 255
        k = (1 + k) % 255
        bg = (i,j,k)
        for ev in event.get(QUIT):
            stop()

def checkWin():
    didWin = True
    i = 0   
    while i < 9:
        if state.grid[i] != goal[i]:
            didWin = False
            break
        i += 1
    if didWin:
        won()

goal = [0,1,2,3,4,5,6,7,8]
state = State
font.init()
fnt = font.SysFont("calibri",167)
BLACK = (0,0,0)
GREY = (100,100,100)
WHITE = (255,255,255)

init()
screen = display.set_mode((800,600))
rec = Rect(150,50,500,500)
grid = image.load("Grid.png").convert_alpha()
display.set_caption("8puzzle")
screen.fill((WHITE))
initiateGrid()
while True:
    time.Clock().tick(60)
    for ev in event.get([QUIT,KEYDOWN]):
        if ev.type == QUIT:
            stop()
        elif ev.type == KEYDOWN:
            move(ev.key)
            checkWin()