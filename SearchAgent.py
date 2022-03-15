from typing import Iterable

class State():
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
        hsh = hash(self.grid)
        s = State.states.get(hsh,[])
        if len(s) == 0:
            State.states[hsh] = list([self])
        else:
            found = False
            for st in s:
                if st.grid == self.grid:
                    return True
            s.append(self)
            return False
            