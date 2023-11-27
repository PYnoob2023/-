from concurrent.futures import ThreadPoolExecutor
import hashlib
import time

transposition_table = {}

def evaluate_position(board, player):
    # Your evaluation function
    score = 0
    # Code to calculate the score using a heuristic function
    return score

def check_continuous_pieces(board, i, j, player, count, ROWS, COLS):
    # Check for continuous pieces in a given direction
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for di, dj in directions:
        pieces_count = 0
        empty_count = 0
        for step in range(-count + 1, count):
            ni, nj = i + step * di, j + step * dj
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                if board[ni][nj] == player:
                    pieces_count += 1
                elif board[ni][nj] == 0:
                    empty_count += 1
                else:
                    break

        if pieces_count == count - 1 and empty_count == 2:
            return True

    return False

def is_terminal(board, ROWS, COLS):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def check_continuous_pieces(board, i, j, player, count, ROWS, COLS):
        for di, dj in directions:
            pieces_count = 0
            empty_count = 0
            for step in range(-count + 1, count):
                ni, nj = i + step * di, j + step * dj
                if 0 <= ni < ROWS and 0 <= nj < COLS:
                    if board[ni][nj] == player:
                        pieces_count += 1
                    elif board[ni][nj] == 0:
                        empty_count += 1
                    else:
                        break

            if pieces_count == count - 1 and empty_count == 2:
                return True

        return False

    # Rest of the function...

def hash_board(board):
    # Create a hash of the board state
    return hashlib.sha256(str(board).encode()).hexdigest()

def update_board(board, i, j, player):
    # Update the board with a move
    new_board = [row[:] for row in board]
    new_board[i][j] = player
    return new_board

# Other function definitions...

def apply_special_moves(board, player, ROWS, COLS):
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == player:
                if check_continuous_pieces(board, i, j, player, 3, ROWS, COLS):
                    for di, dj in [(-1, 0), (3, 0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < ROWS and 0 <= nj < COLS and board[ni][nj] == 0:
                            return update_board(board, ni, nj, -player)
                elif check_continuous_pieces(board, i, j, player, 4, ROWS, COLS):
                    for di, dj in [(-1, 0), (4, 0)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < ROWS and 0 <= nj < COLS and board[ni][nj] == 0:
                            return update_board(board, ni, nj, -player)
    return board

def alpha_beta_search_parallel(args):
    board, depth, alpha, beta, player, ROWS, COLS, move = args
    board_hash = hash_board(board)

    # Check the transposition table
    if board_hash in transposition_table:
        return transposition_table[board_hash]

    if depth == 0 or is_terminal(board, ROWS, COLS):
        result = evaluate_position(board, player), move
        transposition_table[board_hash] = result
        return result

    # Apply special moves
    board = apply_special_moves(board, player, ROWS, COLS)

    if player == 1:
        value = -float('inf')
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] == 0:
                    new_board = update_board(board, i, j, player)
                    score, _ = alpha_beta_search_parallel((new_board, depth - 1, alpha, beta, -player, ROWS, COLS, (i, j)))
                    if score > value:
                        value = score
                        move = (i, j)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta pruning
        result = value, move
    else:
        value = float('inf')
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] == 0:
                    new_board = update_board(board, i, j, player)
                    score, _ = alpha_beta_search_parallel((new_board, depth - 1, alpha, beta, -player, ROWS, COLS, (i, j)))
                    if score < value:
                        value = score
                        move = (i, j)
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # Alpha pruning
        result = value, move

    transposition_table[board_hash] = result
    return result

def get_ai_move(board, player, ROWS, COLS):
    # Use iterative deepening to adjust the search depth
    start_time = time.time()
    time_limit = 10  # seconds
    depth = 1
    best_move = None
    while True:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(alpha_beta_search_parallel, [(board, depth, -float('inf'), float('inf'), player, ROWS, COLS, None)] * COLS))

        best_move = max(results, key=lambda x: x[0])[1]
        end_time = time.time()
        elapsed_time = end_time - start_time
        if elapsed_time > time_limit or depth > ROWS * COLS:
            break
        depth += 1
    return best_move
