from math import sqrt
from threading import Thread
from time import sleep, time
from typing import Iterable
from abc import ABC , abstractmethod
from numpy import array2string , all , array, reshape
from collections import deque
import heapq

class SearchAgent(ABC):

    frontier : Iterable
    found = False
    states = set() #explored states
    keys = ((0,-1),(0,1),(-1,0),(1,0))
    goal = "012345678"
    goal2 = array([[0,1,2],[3,4,5],[6,7,8]])

    def __init__(self,state,init) -> None:
        super().__init__()
        s = array2string(reshape(state.grid,-1),separator="")
        state.grid = s[1:10]
        self.state = state
        self.state.blank = self.state.blank[0]*3 + self.state.blank[1]
        self.frontier = init([])

    @abstractmethod
    def search(self):
        pass

    class Results:

        def __init__(self,moves: list,found: bool,states: int,depth) -> None:
            self.moves = moves
            self.found = found
            self.states = states
            self.depth = depth

def timer(f,type=None):
    ts = time()
    if type is not None:
        res = f(type)
    else:
        res = f()
    return time()-ts , res
class DFS(SearchAgent):

    def __init__(self,state) -> None:
        super().__init__(state,deque)

    def search(self):
        max_depth = 0
        self.state.depth = 0        
        self.frontier.append(self.state)
        Printer().start()
        while self.frontier :
            state = self.frontier.pop()
            if state.depth > max_depth:
                max_depth = state.depth
            SearchAgent.states.add(state.grid)
            if state.grid == SearchAgent.goal:
                SearchAgent.found = True
                return SearchAgent.Results(state.backtrack(),True,len(SearchAgent.states),max_depth)

            neighbours = state.true_neighbours()
            neighbours.reverse()
            for neighbour in neighbours:
                neighbour.depth = state.depth + 1
                if neighbour not in self.frontier:
                    self.frontier.append(neighbour)
        return SearchAgent.Results([self.state.blank],False,0,0)

class BFS(SearchAgent):

    def __init__(self,state) -> None:
        super().__init__(state,deque)

    def search(self):
        max_depth = 0
        self.state.depth = 0        
        self.frontier.append(self.state)
        Printer().start()
        while self.frontier :
            state = self.frontier.popleft()
            if state.depth > max_depth:
                max_depth = state.depth
            SearchAgent.states.add(state.grid)
            if state.grid == SearchAgent.goal:
                SearchAgent.found = True
                return SearchAgent.Results(state.backtrack(),True,len(SearchAgent.states),max_depth)

            for neighbour in state.true_neighbours():
                neighbour.depth = state.depth + 1
                if neighbour not in self.frontier:
                    self.frontier.append(neighbour)
        return SearchAgent.Results([self.state.blank],False,0,0)

class AStar(SearchAgent):

    def __init__(self, state) -> None:
        super().__init__(state,list)

    def search(self,type):
        max_depth = 0
        state = self.state
        state.cost = 0
        state.depth = 0
        heapq.heappush(self.frontier,state)
        Printer().start()
        while self.frontier:
            state = heapq.heappop(self.frontier)
            if state.depth > max_depth:
                max_depth = state.depth
            SearchAgent.states.add(state.grid)
            if state.grid == SearchAgent.goal:
                SearchAgent.found = True
                return SearchAgent.Results(state.backtrack(),True,len(SearchAgent.states),max_depth)

            for neighbour in state.true_neighbours():
                neighbour.cost = state.cost + 1 + self.heu(neighbour,type)
                neighbour.depth = state.depth + 1
                if neighbour not in self.frontier:
                    heapq.heappush(self.frontier,neighbour)
                else:
                    self.decreaseKey(state,neighbour.cost,self.frontier.index(neighbour))
        return SearchAgent.Results([self.state.blank],False,0,0)


    def heu(self,state,type):
        """
        calculates heuristics for a given state
        """
        sum = 0
        if type == 1:
            for i in range(3):
                for j in range(3):
                    num = int(state.grid[i*3 +j])
                    if num == 0:
                        continue
                    x = (num%3) - j
                    y = (num//3) - i
                    sum += abs(x) + abs(y)
        else:
            for i in range(3):
                for j in range(3):
                    num = int(state.grid[i*3 +j])
                    if num == 0:
                        continue
                    x = (num%3) - j
                    y = (num//3) - i
                    sum += sqrt((x**2) + (y**2))
        return sum

    def decreaseKey(self,parent,cost: int,index: int):
        state = self.frontier[index]
        if state.cost > cost:
            state.cost = cost
            state.parent = parent


class State:
    """
    Stores all data relevant to a specific grid state to facilitate searching
    """

    def __init__(self, grid ,parent ,blank: tuple) -> None:
        self.grid = grid
        self.parent = parent
        self.blank = blank

    def __lt__(self,other):
        return self.cost < other.cost 

    def true_neighbours(self) -> list:
        aval_states = []
        for num in self.availableNodes():
            state = self.newState(num)
            if not state.isExplored():
                aval_states.append(state)
        return aval_states

    def isExplored(self) -> bool:
        """
        checks if this state was already explored
        """
        hash = self.grid
        return hash in SearchAgent.states

    def availableNodes(self):
        blank = self.blank
        aval_nodes = []
        if blank - 3 > -1:
            aval_nodes.append(blank - 3)
        if blank + 3 < 9:
                aval_nodes.append(blank + 3)
        if blank < 3:
            if blank - 1 > -1:
                aval_nodes.append(blank - 1)
            if blank + 1 < 3:
                aval_nodes.append(blank + 1)
        elif blank < 6:
            if blank - 1 > 2:
                aval_nodes.append(blank - 1)
            if blank + 1 < 6:
                aval_nodes.append(blank + 1)
        elif blank < 9:
            if blank - 1 > 5:
                aval_nodes.append(blank - 1)
            if blank + 1 < 9:
                aval_nodes.append(blank + 1)
        return aval_nodes


    def isavailable(self , key):
        blank = self.blank
        num = ((blank[0]+key[0]),(blank[1]+key[1]))
        if -1 < num[0] < 3 and -1 < num[1] < 3 :
            return True
        return False

    def newState(self,num):    
        blank = self.blank
        l = list(self.grid)
        l[blank] , l[num] = l[num] , l[blank]
        l = "".join(l)
        return State(l,self,num)

    def backtrack(self):
        st = self
        blank = (st.blank//3,st.blank%3)
        moves = [blank]
        while st.parent is not None:
            st = st.parent
            blank = (st.blank//3,st.blank%3)
            moves.append(blank)
        moves.reverse()
        return moves

class Printer(Thread):

    def run(self):
        while not SearchAgent.found:
            print(len(SearchAgent.states))



def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def isSolvable(puzzle) :
    inv_count = getInvCount([j for sub in puzzle for j in sub])
    return (inv_count % 2 == 0)
