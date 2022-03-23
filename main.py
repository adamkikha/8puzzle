from time import sleep
from tkinter import messagebox
from Puzzle import Puzzle
import SearchAgent

p = Puzzle()
if messagebox.askyesno("play style","play by yourself? \nselect no to let the AI find the solution"):
    p.getEvents()
else:
    agent = SearchAgent.AStar(p.state)
    res = agent.search(1)
    s = "Total number of moves: " + str(len(res.moves)-1)
    if messagebox.askyesno("display moves","display solution moves?\n"+s):
        i = 0
        while i+1 < len(res.moves):
            p.drawSwap(res.moves[i],res.moves[i+1])
            sleep(1)
            i += 1
    p.getEvents()