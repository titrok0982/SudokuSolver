question = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

complete_board = [
    [1,2,3,6,7,8,9,4,5],
    [5,8,4,2,3,9,7,6,1],
    [9,6,7,1,4,5,3,2,8],
    [3,7,2,4,6,1,5,8,9],
    [6,9,1,5,8,3,2,7,4],
    [4,5,8,7,9,2,6,1,3],
    [8,3,6,9,2,4,1,5,7],
    [2,1,9,8,5,7,4,3,6],
    [7,4,5,3,1,6,8,9,2]
]


empty_board = [
    [1,2,0,6,0,8,0,0,0],
    [5,8,4,2,3,9,7,0,1],
    [0,6,0,1,4,0,0,0,0],
    [3,7,0,0,6,1,5,8,0],
    [6,9,1,0,8,0,2,7,4],
    [4,5,8,7,0,2,0,1,3],
    [0,3,0,0,2,4,1,5,0],
    [2,0,9,8,5,0,4,3,6],
    [0,0,0,3,0,6,0,9,2]
]

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i,j
    return -1,-1

def valid(num, board, line, col):
    if num in board[line]:
        return False
    for i in range(len(board)):
        if board[i][col] == num:
            return False
    square_x, square_y = 3 * (line//3),3 * (col//3)
    for k in range(square_x, square_x+3):
        for l in range(square_y, square_y+3):
            if board[k][l] == num:
                return False
    return True

def pretty_print(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - - ")
        for j in range(len(board[i])):
            if j % 3 == 0 and j != 0 :
                print(" | ",end="")
            if j == 8 :
                print(board[i][j])
            else:
                print(board[i][j], " ",end="")

def solve(board):
    next_square = find_empty(board)

    #Board Full
    if next_square == (-1,-1):
        # print("Solved !")
        # pretty_print(board)
        return True
    
    #Try all numbers for empty square
    for possibility in range(1,10):
        if valid(possibility, board, next_square[0], next_square[1]):
            board[next_square[0]][next_square[1]] = possibility
            if solve(board) :
                return True
            board[next_square[0]][next_square[1]] = 0
    return False