import copy
import os

def initialize_board():
    return [[0, 0, 0] for _ in range(3)]

def print_board(board):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in board:
        print(" ".join(map(lambda x: "O" if x == 1 else "X" if x == 2 else " ", row)))
        print("------")

def check_win(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]

    for row in board:
        for cell in row:
            if cell == 0:
                return -1  # Game still ongoing

    return 0  # It's a draw

def best_choice(board, zeroes):
    to_play = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 1
                to_play.append((minmax(copy.deepcopy(board), zeroes - 1, 2), (i, j)))
                board[i][j] = 0

    to_play.sort()
    return to_play[-1][1]

def minmax(board, zeroes, player):
    result = check_win(board)
    if result == 0:
        return 0
    elif result == 1:
        return zeroes
    elif result == 2:
        return -zeroes

    best_score = float('-inf') if player == 1 else float('inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player
                score = minmax(copy.deepcopy(board), zeroes - 1, 2 if player == 1 else 1)
                if player == 1:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)
                board[i][j] = 0

    return best_score

def print_choices(choices):
    for choice in choices:
        print(f"{choice[0]} Move: {choice[1][0] + 1} {choice[1][1] + 1}")

def main():
    board = initialize_board()
    print_board(board)
    play = 0

    while check_win(board) == -1:
        # Player's turn
        x, y = map(int, input("Your play...\n").split())
        while board[x - 1][y - 1] != 0:
            print("Invalid move. Try again.")
            x, y = map(int, input().split())
        board[x - 1][y - 1] = 2
        print_board(board)

        if check_win(board) != -1:
            break

        # AI's turn
        print('AI\'s turn:')
        play += 1
        ai_play = best_choice(board, 10 - play)
        board[ai_play[0]][ai_play[1]] = 1
        print_board(board)
        print_choices([(minmax(copy.deepcopy(board), 10 - play, 2), ai_play)])
        play += 1

    result = check_win(board)
    if result == 1:
        print("You lost!")
    elif result == 2:
        print("You won!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
