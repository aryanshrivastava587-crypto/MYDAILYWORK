import tkinter as tk
import math

# ------------------ GAME LOGIC ------------------

board = [" " for _ in range(9)]
buttons = []

def check_winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def minimax(is_maximizing):
    result = check_winner()
    if result == "X": return 1
    if result == "O": return -1
    if result == "Draw": return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(False)
                board[i] = " "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(True)
                board[i] = " "
                best = min(best, score)
        return best

def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ------------------ GUI FUNCTIONS ------------------

def on_click(index):
    if board[index] != " ":
        return

    board[index] = "O"
    buttons[index]["text"] = "O"

    if end_game():
        return

    ai = best_move()
    board[ai] = "X"
    buttons[ai]["text"] = "X"

    end_game()

def end_game():
    result = check_winner()
    if result:
        msg = "Draw!" if result == "Draw" else f"{result} wins!"
        status_label.config(text=msg)
        for b in buttons:
            b.config(state="disabled")
        return True
    return False

def reset():
    global board
    board = [" " for _ in range(9)]
    status_label.config(text="Your turn (O)")
    for b in buttons:
        b.config(text=" ", state="normal")

# ------------------ GUI SETUP ------------------

root = tk.Tk()
root.title("Tic Tac Toe AI (Minimax)")

for i in range(9):
    btn = tk.Button(
        root,
        text=" ",
        font=("Arial", 24),
        width=5,
        height=2,
        command=lambda i=i: on_click(i)
    )
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status_label = tk.Label(root, text="Your turn (O)", font=("Arial", 14))
status_label.grid(row=3, column=0, columnspan=3)

reset_btn = tk.Button(root, text="Reset", font=("Arial", 12), command=reset)
reset_btn.grid(row=4, column=0, columnspan=3)

root.mainloop()
