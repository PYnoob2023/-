# board.py

ROWS = 15
COLS = 15

def create_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    return board
