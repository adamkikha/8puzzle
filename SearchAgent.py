class State():
    """
    Stores all data relevant to a specific grid state to facilitate searching
    """
    def __init__(self,grid: list,pastMoves: list,blank: int) -> None:
        self.grid = grid
        self.pastMoves = pastMoves
        self.blank = blank
