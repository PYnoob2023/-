# player.py

def get_player_move():
    row = int(input("Enter row: ")) - 1
    col = int(input("Enter col: ")) - 1
    return row, col
