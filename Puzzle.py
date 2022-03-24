import numpy as np
from random import randint
import random
from sys import exit
from tkinter import messagebox
from pygame import *
from SearchAgent import SearchAgent, State, isSolvable

class Puzzle:

    class Tile:

        def __init__(self,x,y,num) -> None:
            self.x = x
            self.y = y
            self.num = num

        def swap(self,other):
            self.num , other.num = other.num , self.num

    BLACK , GREY , WHITE = (0,0,0) , (100,100,100) , (255,255,255)
    WIDTH , HEIGHT = 480 , 480
    state : State
    Tiles = np.zeros((3,3),Tile)
    screen : surface.Surface
    rec : Rect
    fnt : font

    def drawBG(self):
        grid = image.load("Grid.png").convert_alpha()
        self.screen.fill((self.WHITE))
        draw.rect(self.screen,self.GREY,self.rec)
        self.screen.blit(grid,(150,50))
        display.update()

    def __init__(self) -> None:
        init()
        self.screen = display.set_mode((800,600))
        self.rec = Rect(160,59,self.WIDTH,self.HEIGHT)
        display.set_caption("8puzzle")
        font.init()
        self.fnt = font.SysFont("calibri",167)
        self.drawBG()
        random = False
        if messagebox.askyesno("initiation","randomly generate the grid?"):
            random = True
        self.initiateGrid(random)

    def move(self,key: tuple) -> bool:
        """
        moves the blank tile in the desired direction if it is possible
        and appends it to state.pastMoves
        returns: False if the move can't be played
                    True otherwise
        """
        blank = self.state.blank
        if self.state.isavailable(key) :
            num = ((blank[0]+key[0]),(blank[1] + key[1]))
            self.state = self.switchState(num)
            self.drawSwap(num,blank)
            return True
        return False

    def initiateGrid(self,random: bool):
        """
        takes input from user or uses a rng to initiate the grid for the first time
        """
        grid = np.full((3,3),-1,np.int8)
        c = 0
        i = 0
        j = 0
        if not random:
            cursor = self.fnt.render("_",1,self.BLACK)
            while i < 9:
                time.Clock().tick(60)
                k = event.get([KEYDOWN,QUIT])
                self.screen.blit(cursor,(self.rec.x+ 35 + (c*(self.WIDTH/3 + 4)),self.rec.y - 10 + (j*(self.HEIGHT/3 + 4))))
                display.update()
                while len(k) < 1:
                    k = event.get([KEYDOWN,QUIT])
                for ev in k:
                    if ev.type == QUIT:
                        self.stop()
                    elif ev.key < 57 and ev.key > 47 :
                        num = ev.key - 48
                        if num not in grid:
                            if num == 0:
                                blank = (j,c)
                            grid[j][c] = num
                            tile = Puzzle.Tile(self.rec.x+ (c*(self.WIDTH/3 + 4)),self.rec.y + (j*(self.HEIGHT/3 + 4)),num)
                            self.Tiles[j][c] = tile
                            self.drawTile(tile)
                            i += 1
                            c = i % 3
                            j = i // 3
        else:
            blank = None
            grid = self.shuffle()
            while not isSolvable(grid):
                print("unsolvable! ",grid)
                grid = self.shuffle()
            
            for i in range(9):
                num = grid[i//3][i%3]
                if blank is None and num == 0:
                    blank = ((i//3),(i%3))
                tile = Puzzle.Tile(self.rec.x + ((i%3)*(self.WIDTH/3 + 4)),self.rec.y + ((i//3)*(self.HEIGHT/3 + 4)), num)
                self.drawTile(tile)
                self.Tiles[(i//3)][(i%3)] = tile

        self.state = State(grid,None,blank)
        SearchAgent.states.add(np.array_str(self.state.grid))

    def shuffle(self):
        grid = random.sample(range(9), 9)
        grid = np.reshape(grid, (3, 3))
        return grid

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
        tile_b = self.Tiles[num]
        tile_n = self.Tiles[blank]
        tile_b.swap(tile_n)
        self.drawTile(tile_n)
        self.drawTile(tile_b)


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
        return (self.state.grid == SearchAgent.goal2).all()

    def switchState(self,num):
        blank = self.state.blank
        l = self.state.grid.copy()
        l[blank] , l[num] = l[num] , l[blank]
        return State(l,self.state,num)

    def checkQuit(self):
        if event.get([QUIT]):
            self.stop()

    def getEvents(self):
        time.Clock().tick(60)
        for ev in event.get([QUIT,KEYDOWN]):
            if ev.type == QUIT:
                self.stop()
            elif ev.type == KEYDOWN and K_RIGHT <= ev.key <= K_UP:
                self.move(SearchAgent.keys[ev.key-K_RIGHT])
                if self.checkWin():
                    self.won()
