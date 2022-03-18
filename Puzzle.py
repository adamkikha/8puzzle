
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

    BLACK , GREY , WHITE = (0,0,0) , (100,100,100) , (255,255,255)
    WIDTH , HEIGHT = 480 , 480
    keys = ((-1,0),(1,0),(0,-1),(0,1))
    goal = ((0,1,2),(3,4,5),(6,7,8))
    state : State
    Tiles = []
    screen : surface.Surface
    rec : Rect
    fnt : font


    def __init__(self) -> None:
        init()
        self.screen = display.set_mode((800,600))
        self.rec = Rect(160,59,self.WIDTH,self.HEIGHT)
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

    def availableMoves(self , blank , key = None) -> list:
        pass

    def move(self,key: tuple) -> bool:
        """
        moves the blank tile in the desired direction if it is possible
        and appends it to state.pastMoves
        returns: False if the move can't be played
                    True otherwise
        """
        blank = self.state.blank
        num = ((blank[0]+key[0]),(blank[1] + key[1]))
        if (-1,-1) < num < (3,3):
            self.switchState(blank,num)
            self.drawSwap(num,blank)
            return True
        return False

    def initiateGrid(self,random: bool):
        """
        takes input from user or uses a rng to initiate the grid for the first time
        """
        cell = [self.rec.x,self.rec.y]
        c = 0
        nums = [0,1,2,3,4,5,6,7,8]
        tempRow = []
        tempGrid = []
        if not random:
            cursor = self.fnt.render("_",1,self.BLACK)
            while len(tempGrid) < 9:
                time.Clock().tick(60)
                k = event.get([KEYDOWN,QUIT])
                self.screen.blit(cursor,(cell[0]+35,cell[1]-10))
                display.update()
                while len(k) < 1:
                    k = event.get([KEYDOWN,QUIT])
                for ev in k:
                    if ev.type == QUIT:
                        self.stop()
                    elif ev.key < 57 and ev.key > 47 :
                        num = ev.key - 48
                        if num in nums:
                            nums.remove(num)
                            tile = Puzzle.Tile(cell[0],cell[1],num)
                            self.Tiles.append(tile)
                            tempRow.append(num)
                            self.drawTile(tile)
                            cell[0] += self.WIDTH/3 + 4
                            c += 1
                            if c == 3:
                                tempGrid.append(tuple(tempRow))
                                tempRow=[]
                                cell[0] = self.rec.x
                                cell[1] += self.HEIGHT/3 + 4
                                c = 0
        else:
            blank = None
            while(len(tempGrid)<9):
                num = randint(0,8)
                if num == 0 and blank is None:
                    blank = (len(tempRow)-1,len(tempGrid)-1)
                if num in nums :
                    nums.remove(num)
                    tempRow.append(num)
                    tile = Puzzle.Tile(cell[0],cell[1],num)
                    self.Tiles.append(tile)
                    self.drawTile(tile)
                    cell[0] += self.WIDTH/3 + 4
                    c += 1
                    if c == 3:
                        tempGrid.append(tuple(tempRow))
                        tempRow=[]
                        cell[0] = self.rec.x
                        cell[1] += self.HEIGHT/3 + 4
                        c = 0

        self.state = State(tuple(tempGrid),list(),blank)  
        self.state.isExplored()

        self.getEvents()              

    def stop(self):
        """
        exits the program
        """
        display.quit()
        quit()
        exit()

    def drawTile(self,t):
        tile = Rect(t.x,t.y,153,153)
        if t.num > 0:
            text = self.fnt.render(str(t.num),1,self.BLACK)
            draw.rect(self.screen,(self.WHITE),tile)
            self.screen.blit(text,(t.x+35,t.y))
        else:
            draw.rect(self.screen,(self.GREY),tile)
        display.update()
        
    def drawSwap(self,blank: tuple,num: tuple) -> None:
        cellb = [self.rec.x , self.rec.y]
        celln = [self.rec.x , self.rec.y]
        text = self.fnt.render(str(self.state.grid[num]),1,self.BLACK)
        while blank > 2:
            cellb[1] += self.HEIGHT/3 + 4 
            blank -= 3
        while blank > 0:
            cellb[0] += self.WIDTH/3 + 4
            blank -= 1
        while num > 2:
            celln[1] += self.HEIGHT/3 + 4
            num -= 3
        while num > 0:
            celln[0] += self.WIDTH/3 + 4
            num -= 1
        draw.rect(self.screen,(self.WHITE),Rect(celln[0],celln[1],153,153))
        self.screen.blit(text,(celln[0]+35,celln[1]))
        draw.rect(self.screen,(self.GREY),Rect(cellb[0],cellb[1],153,153))
        display.update()

    def switchState(self,blank: int,num: int) -> None: 
        l = list(self.state.grid)
        l[blank] , l[num] = l[num] , l[blank]
        self.state =  State(tuple(l),self,num)
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
            self.screen.blit(fnt.render("MABROOOOK YA M3lMM!!!",1,self.BLACK),(0,250))
            display.update()
            time.wait(6)
            i = (1 + i) % 255
            j = (1 + j) % 255
            k = (1 + k) % 255
            bg = (i,j,k)
            for ev in event.get(QUIT):
                self.stop()

    def checkWin(self):   
        if self.state.grid == self.goal:
            self.won()

    def getEvents(self):
        while True:
            time.Clock().tick(60)
            for ev in event.get([QUIT,KEYDOWN]):
                if ev.type == QUIT:
                    self.stop()
                elif ev.type == KEYDOWN:
                    self.move(self.keys[ev.key-K_RIGHT])
                    self.checkWin()
