from typing import Iterable
from abc import ABC , abstractmethod

class SearchAgent(ABC):

    frontier : Iterable
    

    def search(self,state):
        pass

class DFS(SearchAgent):
    pass

class BFS(SearchAgent):
    pass

class AStar(SearchAgent):
    pass

class State:
    """
    Stores all data relevant to a specific grid state to facilitate searching
    """
    
    states = set() #explored states
    
    def __init__(self,grid: tuple ,parent ,blank: tuple) -> None:
        self.grid = grid
        self.parent = parent
        self.blank = blank     

    def neighbours(self) -> Iterable:
        pass

    def isExplored(self) -> bool:
        """
        checks if this state was already explored , if it wasn't it adds it to explored states
        """
        hash = str(self.grid)
        if not hash in self.states:
            State.states.add(hash)
            return False
        return True
            