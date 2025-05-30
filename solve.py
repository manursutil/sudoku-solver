from generate import board as generated_board

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

def valid(bo, num, pos):
    """Checks if placing a given number (num) at a given position (pos) on the board is valid according to Sudoku rules"""

    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("----------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("|", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def find_empty(bo):
    """Finds an empty cell (0) in the board"""

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j   # row, col
    return None

current_board = generated_board

if current_board:
    print("Generated Sudoku Board (to be solved):")
    print_board(current_board)

    if solve(current_board):
        print("_____________________________")
        print("Solved Sudoku Board:")
        print_board(current_board)
    else:
        print("_____________________________")
        print("This Sudoku bard has no solution.")
else:
    print("Failed to generate a board from generate.py")