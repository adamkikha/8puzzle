from typing import Iterable
from abc import ABC , abstractmethod

class SearchAgent(ABC):

    frontier : Iterable
    

    def search(self,state):
        pass

class State:
    """
    Stores all data relevant to a specific grid state to facilitate searching
    """
    
    states = dict() #explored states
    
    def __init__(self,grid: tuple ,pastMoves: list ,blank: int) -> None:
        self.grid = grid
        self.pastMoves = pastMoves
        self.blank = blank     

    def neighbours(self) -> Iterable:
        pass

    def isExplored(self) -> bool:
        """
        checks if this state was already explored , if it wasn't it adds it to explored states
        """
        hash = str(self.grid)
        if not hash in self.states:
            State.states[hash] = self
            return False
        return True
            