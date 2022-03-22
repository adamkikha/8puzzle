from os import stat_result
from sre_parse import State
from typing import Iterable
from abc import ABC , abstractmethod
from numpy import array_str
import numpy
from collections import deque
from Puzzle import Puzzle
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
    
    def __init__(self, grid ,parent ,blank: tuple) -> None:
        self.grid = grid
        self.parent = parent
        self.blank = blank     

    def neighbours(self) -> Iterable:

        pass

    def isExplored(self) -> bool:
        """
        checks if this state was already explored , if it wasn't it adds it to explored states
        """
        hash = array_str(self.grid)
        if not hash in self.states:
            State.states.add(hash)
            return False
        return True
            