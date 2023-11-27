import tkinter as tk
from board import create_board
from game import check_win, make_move
from player import get_player_move
from ai import get_ai_move
from ai import hash_board


ROWS = 15
COLS = 15
CELL_SIZE = 30

def draw_board(canvas):
    for i in range(ROWS):
        for j in range(COLS):
            canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE, (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE, fill="white", outline="black")

def draw_stone(canvas, row, col, color):
    canvas.create_oval(col * CELL_SIZE, row * CELL_SIZE, (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE, fill=color)

def play_game():
    board = create_board()
    current_player = 1

    def on_click(event):
        nonlocal current_player
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        if make_move(board, row, col, current_player, ROWS, COLS):
            draw_stone(canvas, row, col, "black" if current_player == 1 else "white")
            if check_win(board, current_player, ROWS, COLS):
                winner = "玩家" if current_player == 1 else "电脑"
                show_winner(winner)
                return

            current_player = 2 if current_player == 1 else 1

            if current_player == 2:
                ai_row, ai_col = get_ai_move(board, current_player, ROWS, COLS)
                make_move(board, ai_row, ai_col, current_player, ROWS, COLS)
                draw_stone(canvas, ai_row, ai_col, "white")

                if check_win(board, current_player, ROWS, COLS):
                    winner = "玩家" if current_player == 1 else "电脑"
                    show_winner(winner)
                    return

                current_player = 1

    def show_winner(winner):
        result = f"{winner}获胜！"
        top = tk.Toplevel()
        top.title("游戏结果")
        msg = tk.Label(top, text=result)
        msg.pack()
        btn = tk.Button(top, text="关闭", command=top.destroy)
        btn.pack()

    root = tk.Tk()
    root.title("五子棋")
    canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
    canvas.pack()

    canvas.bind("<Button-1>", on_click)
    draw_board(canvas)

    root.mainloop()

if __name__ == "__main__":
    play_game()
