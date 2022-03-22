from typing import Iterable
from abc import ABC , abstractmethod
from typing import Iterable
from numpy import array_str , all , array
from collections import deque
class SearchAgent(ABC):
    frontier : Iterable

    def __init__(self,state) -> None:
        super().__init__()
        self.state = state

    @abstractmethod
    def search(self,state):
        pass

    class Results:

        def __init__(self,moves: list,found: bool,states: int) -> None:
            self.moves = moves
            self.found = found
            self.states = states

class DFS(SearchAgent):

    def __init__(self,state) -> None:
        super().__init__(state)
        self.frontier=deque([])

    def search(self):
        state = self.frontier.popleft()
        State.states.add(state)
        while self.frontier :
            State.states.add(self.frontier.pop())
            if self.state.checkWin():
                return SearchAgent.Results(state.backtrack(),True,len(State.states))

            for neighbour in self.state.true_neighbours():
                if neighbour not in self.frontier:
                    self.frontier.append(neighbour)
        return False
    

class BFS(SearchAgent):

    def __init__(self,state) -> None:
        super().__init__(state)
        self.frontier = deque([])

    def search(self):        
        self.frontier.append(self.state)
        while self.frontier :
            print(len(State.states))
            state = self.frontier.popleft()
            State.states.add(state)
            if state.checkWin():
                return SearchAgent.Results(state.backtrack(),True,len(State.states))
      
            for neighbour in self.state.true_neighbours():
                if neighbour not in self.frontier:
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
    goal = array([[0,1,2],[3,4,5],[6,7,8]])

    def __init__(self, grid ,parent ,blank: tuple) -> None:
        self.grid = grid
        self.parent = parent
        self.blank = blank

    def true_neighbours(self) -> list:
        aval_states = []
        for num in self.availableStates():
            state = self.switchState(num)
            if not state.isExplored():
                aval_states.append(state)
        return aval_states

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

    def checkWin(self):   
        return (self.grid == self.goal).all()
            
    def backtrack(self):
        st = self
        moves = [st.blank]
        while st.parent is not None:
            st = st.parent
            moves.append(st.blank)

        return moves.reverse()
