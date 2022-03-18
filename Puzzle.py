from msilib.schema import Font
from random import randint
from sys import exit
from tkinter import messagebox
from pygame import *
from SearchAgent import State

class Puzzle:

    class Tile:

        def __init__(self,x,y,num) -> None:
            self.x = x
            self.y = y
            self.num = num

        def swap(self,other):
            self.x , other.x = other.x , self.x
            self.y , other.y = other.y , self.y
            self.num , other.num = other.num , self.num

    goal = [0,1,2,3,4,5,6,7,8]
    state : State
    Tiles = []
    screen : Surface
    rec : Rect
    fnt : Font
    BLACK = (0,0,0)
    GREY = (100,100,100)
    WHITE = (255,255,255)


    def __init__(self) -> None:
        init()
        self.screen = display.set_mode((800,600))
        self.rec = Rect(150,50,500,500)
        grid = image.load("Grid.png").convert_alpha()
        display.set_caption("8puzzle")
        font.init()
        self.fnt = font.SysFont("calibri",167)
        self.screen.fill((self.WHITE))
        draw.rect(self.screen,self.GREY,self.rec)
        self.screen.blit(grid,(150,50))
        display.update()
        random = False
        if messagebox.askyesno("initiation","randomly generate the grid?"):
            random = True
        self.initiateGrid(random)
        



    def move(self,key) -> bool:
        """
        moves the blank tile in the desired direction if it is possible
        and appends it to state.pastMoves
        returns: False if the move can't be played
                    True otherwise
        """
        moved = False
        blank = self.state.grid.index(0)
        num = 0
        if key == K_UP:
            if blank - 3 > -1:
                num = blank - 3
                self.switchState(blank,num)
                moved = True
        elif key == K_DOWN: 
            if blank + 3 < 9:
                num = blank + 3
                self.switchState(blank,num)
                moved = True
        elif blank < 3:
            if key == K_LEFT:
                if blank - 1 > -1:
                    num = blank - 1
                    self.switchState(blank,num)
                    moved = True
            elif key == K_RIGHT:
                if blank + 1 < 3:
                    num = blank + 1
                    self.switchState(blank,num)
                    moved = True
        elif blank < 6:
            if key == K_LEFT:
                if blank - 1 > 2:
                    num = blank - 1
                    self.switchState(blank,num)
                    moved = True
            elif key == K_RIGHT:
                if blank + 1 < 6:
                    num = blank + 1
                    self.switchState(blank,num)
                    moved = True
        elif blank < 9:
            if key == K_LEFT:
                if blank - 1 > 5:
                    num = blank - 1
                    self.switchState(blank,num)
                    moved = True
            elif key == K_RIGHT:
                if blank + 1 < 9:
                    num = blank + 1
                    self.switchState(blank,num)
                    moved = True
        if moved:
            self.state.pastMoves.append(key)
            self.drawSwap(num,blank)
            return True
        return False

    def initiateGrid(self,random: bool):
        """
        takes input from user or uses a rng to initiate the grid for the first time
        """
        cell = [self.rec.x,self.rec.y]
        c = 0
        tempGrid = []
        if not random:
            cursor = self.fnt.render("_",1,self.BLACK)
            while len(tempGrid) < 9:
                time.Clock().tick(60)
                k = event.get([KEYDOWN,QUIT])
                self.screen.blit(cursor,(cell[0]+45,cell[1]))
                display.update()
                while len(k) < 1:
                    k = event.get([KEYDOWN,QUIT])
                for ev in k:
                    if ev.type == QUIT:
                        self.stop()
                    elif ev.key < 57 and ev.key > 47 :
                        num = ev.key - 48
                        if tempGrid.count(num) == 0:
                            tempGrid.append(num)
                            self.drawTile(cell,num)
                            cell[0] += 167
                            c += 1
                            if c == 3:
                                cell[0] = self.rec.x
                                cell[1] += 167
                                c = 0
        else:
            while(len(tempGrid)<9):
                num = randint(0,8)
                if tempGrid.count(num) == 0:
                    tempGrid.append(num)
                    self.drawTile(cell,num)
                    cell[0] += 167
                    c += 1
                    if c == 3:
                        cell[0] = self.rec.x
                        cell[1] += 167
                        c = 0

        self.state = State(tuple(tempGrid),list(),tempGrid.index(0))  
        self.state.isExplored()

        self.getEvents()              

    def stop(self):
        """
        exits the program
        """
        display.quit()
        quit()
        exit()

    def drawTile(self,cell,num):
        tile = Rect(cell[0]+10,cell[1]+10,152,152)
        if num > 0:
            text = self.fnt.render(str(num),1,self.BLACK)
            draw.rect(self.screen,(self.WHITE),tile)
            self.screen.blit(text,(cell[0]+45,cell[1]+10))
        else:
            draw.rect(self.screen,(self.GREY),tile)
        display.update()
        
    def drawSwap(self,blank: int,num: int) -> None:
        cellb = [self.rec.x , self.rec.y]
        celln = [self.rec.x , self.rec.y]
        text = self.fnt.render(str(self.state.grid[num]),1,self.BLACK)
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
        draw.rect(self.screen,(self.WHITE),Rect(celln[0]+10,celln[1]+10,152,152))
        self.screen.blit(text,(celln[0]+45,celln[1]+10))
        draw.rect(self.screen,(self.GREY),Rect(cellb[0]+10,cellb[1]+10,152,152))
        display.update()

    def switchState(self,blank: int,num: int) -> None: 
        l = list(self.state.grid)
        l[blank] , l[num] = l[num] , l[blank]
        self.state =  State(tuple(l),self.state.pastMoves,num)
        self.state.isExplored()
            #messagebox.showwarning("RAKEZ!","El3ab 3edel enta kont hena abl keda")


    def won(self):
        i = 0
        j = 200
        k = 100
        bg = (0,0,0)
        fnt = font.SysFont("calibri",65)
        while True:
            self.screen.fill((bg))
            self.screen.blit(fnt.render("MABROOOOK YA KOSOMAK!!!",1,self.BLACK),(0,250))
            display.update()
            time.wait(6)
            i = (1 + i) % 255
            j = (1 + j) % 255
            k = (1 + k) % 255
            bg = (i,j,k)
            for ev in event.get(QUIT):
                self.stop()

    def checkWin(self):
        didWin = True
        i = 0   
        while i < 9:
            if self.state.grid[i] != self.goal[i]:
                didWin = False
                break
            i += 1
        if didWin:
            self.won()

    def getEvents(self):
        while True:
            time.Clock().tick(60)
            for ev in event.get([QUIT,KEYDOWN]):
                if ev.type == QUIT:
                    self.stop()
                elif ev.type == KEYDOWN:
                    self.move(ev.key)
                    self.checkWin()
