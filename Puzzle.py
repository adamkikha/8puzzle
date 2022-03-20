from typing import Tuple
import numpy as np
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
            self.num , other.num = other.num , self.num

    BLACK , GREY , WHITE = (0,0,0) , (100,100,100) , (255,255,255)
    WIDTH , HEIGHT = 480 , 480
    keys = ((0,-1),(0,1),(-1,0),(1,0))
    goal = np.array([[0,1,2],[3,4,5],[6,7,8]])
    state : State
    Tiles = np.zeros((3,3),Tile)
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

    def availableMoves(self , blank: Tuple, keys = None | Tuple):
        c = 0
        i = 1
        key = keys
        if keys is None:
            keys = self.keys
            i = 4
            key = keys[0]
        aval_keys = []
        while c < i:
            num = ((blank[0]+key[0]),(blank[1]+key[1]))
            if -1 < num[0] < 3 and -1 < num[1] < 3 :
                aval_keys.append(key)
            c += 1
        if len(aval_keys) < 2:
            return bool(aval_keys)
        return aval_keys

    def move(self,key: tuple) -> bool:
        """
        moves the blank tile in the desired direction if it is possible
        and appends it to state.pastMoves
        returns: False if the move can't be played
                    True otherwise
        """
        blank = self.state.blank
        if self.availableMoves(blank,key) :
            num = ((blank[0]+key[0]),(blank[1] + key[1]))
            self.switchState(blank,num)
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
            while i < 9:
                num = randint(0,8)
                if blank is None and num == 0:
                    blank = (j,c)
                if num not in grid :
                    grid[j][c] = num
                    tile = Puzzle.Tile(self.rec.x+ (c*(self.WIDTH/3 + 4)),self.rec.y + (j*(self.HEIGHT/3 + 4)),num)
                    self.Tiles[j][c] = tile
                    self.drawTile(tile)
                    i += 1
                    c = i % 3
                    j = i // 3

        self.state = State(grid,None,blank)  
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
        tile_b = self.Tiles[num]
        tile_n = self.Tiles[blank]
        tile_b.swap(tile_n)
        self.drawTile(tile_n)
        self.drawTile(tile_b)

    def switchState(self,blank: tuple,num: tuple) -> None: 
        l = self.state.grid
        l[blank] , l[num] = l[num] , l[blank]
        self.state =  State(l,self,num)
        if self.state.isExplored():
            messagebox.showwarning("RAKEZ!","El3ab 3edel enta kont hena abl keda")


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
        if (self.state.grid == self.goal).all() :
            self.won()

    def getEvents(self):
        while True:
            time.Clock().tick(60)
            for ev in event.get([QUIT,KEYDOWN]):
                if ev.type == QUIT:
                    self.stop()
                elif ev.type == KEYDOWN and K_RIGHT <= ev.key <= K_UP:
                    self.move(self.keys[ev.key-K_RIGHT])
                    self.checkWin()
