<<<<<<< HEAD
from os import stat_result
from sre_parse import State
from typing import Iterable
=======
>>>>>>> a34fdb52d6b0a106dba21fd73dbddd394d504bc0
from abc import ABC , abstractmethod
from typing import Iterable
from numpy import array_str
<<<<<<< HEAD
import numpy
from collections import deque
from Puzzle import Puzzle
=======
>>>>>>> a34fdb52d6b0a106dba21fd73dbddd394d504bc0
class SearchAgent(ABC):

    frontier : Iterable
    
    @abstractmethod
    def search(self,state):
        pass

class DFS(SearchAgent):

    def __init__(self) -> None:
        super().__init__()
        self.frontier=deque([])

    def search(self, state):
        #return super().search(state)
        self.frontier.append(state)
        while self.frontier :
            State.isExplored()
            if Puzzle.goal == state.grid :
                return True
      
            for neighbour in State.neighbours():
                if neighbour not in self.frontier and not state.isExplored():
                    self.frontier.append(neighbour)
        return False
    

class BFS(SearchAgent):

    def __init__(self) -> None:
        super().__init__()
        self.frontier=deque([])

    def  search(self, state):
            #return super().search(state)
            self.frontier.append(state)
            while self.frontier :
                State.states.append(self.frontier.pop)
                if Puzzle.goal == state.grid :
                    return True
      
            for neighbour in State.neighbours():
                if neighbour not in self.frontier and not state.isExplored():
                    self.frontier.append(neighbour)
            return False
             

class AStar(SearchAgent):
    pass

class State:
    """
    Stores all data relevant to a specific grid state to facilitate searching
    """
    
    states = set() #explored states
    keys = ((0,-1),(0,1),(-1,0),(1,0))

    def __init__(self, grid ,parent ,blank: tuple) -> None:
        self.grid = grid
        self.parent = parent
        self.blank = blank

<<<<<<< HEAD
    def neighbours(self) -> Iterable:

        pass
=======
    def true_neighbours(self) -> list:
        aval_states = []
        for num in self.availableStates():
            state = self.switchState(num)
            if not state.isExplored():
                aval_states.append(state)
        return aval_states
>>>>>>> a34fdb52d6b0a106dba21fd73dbddd394d504bc0

    def isExplored(self) -> bool:
        """
        checks if this state was already explored
        """
        hash = array_str(self.grid)
        return hash in State.states
        

    def availableStates(self , keys = None):
        i = 1
        key = keys
        if keys is None:
            keys = self.keys
            i = 4
            key = keys[0]
        aval_nums = []
        blank = self.blank
        for c in range(i):
            num = ((blank[0]+key[0]),(blank[1]+key[1]))
            if -1 < num[0] < 3 and -1 < num[1] < 3 :
                aval_nums.append(num)
            key = keys[(c % 3)+1]

        if len(aval_nums) < 2:
            return bool(aval_nums)
        return aval_nums
            
    def switchState(self,num: tuple):    
        l = self.grid.copy()
        blank = self.blank
        l[blank] , l[num] = l[num] , l[blank]
        return State(l,self,num)
        