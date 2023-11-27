def make_move(board, row, col, player, ROWS, COLS):
    if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == 0:
        board[row][col] = player
        return True
    return False

def check_win(board, player, ROWS, COLS):
    # 检查水平方向
    for i in range(ROWS):
        for j in range(COLS - 4):
            if board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == player and board[i][j + 4] == player:
                return True

    # 检查垂直方向
    for i in range(ROWS - 4):
        for j in range(COLS):
            if board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == player and board[i + 4][j] == player:
                return True

    # 检查主对角线方向
    for i in range(ROWS - 4):
        for j in range(COLS - 4):
            if board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and board[i + 3][j + 3] == player and board[i + 4][j + 4] == player:
                return True

    # 检查副对角线方向
    for i in range(ROWS - 4):
        for j in range(4, COLS):
            if board[i][j] == player and board[i + 1][j - 1] == player and board[i + 2][j - 2] == player and board[i + 3][j - 3] == player and board[i + 4][j - 4] == player:
                return True

    return False
