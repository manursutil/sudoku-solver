import random

def is_valid_for_generation(bo, num, pos):
    """Checks if placing a given number (num) at a given position (pos) on the board is valid according to Sudoku rules"""
    row, col = pos

    # Check row
    for i in range(len(bo[0])):
        if bo[row][i] == num and col != i: # If num exists and it's not the current cell
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][col] == num and row != i: # If num exists and it's not the current cell
            return False

    # Check box
    box_x_start = (col // 3) * 3
    box_y_start = (row // 3) * 3

    for i in range(box_y_start, box_y_start + 3):
        for j in range(box_x_start, box_x_start + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty_for_generation(bo):
    """Finds an empty cell (0) in the board"""
    for row in range(len(bo)):
        for col in range(len(bo[0])):
            if bo[row][col] == 0:
                return row, col # Return row and col of the empty cell
    return None

def fill_grid_completely(bo):
    """Take an empty board and fill it completely to make a valid Sudoku board"""
    find = find_empty_for_generation(bo)
    if not find:
        return True # Board is full, solution found
    else:
        row, col = find

    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for num in numbers:
        if is_valid_for_generation(bo, num, (row, col)):
            bo[row][col] = num # Place the number

            if fill_grid_completely(bo):
                return True # Solution found

            # if False, num didn't work, solution not found
            # Backtrack and reset
            bo[row][col] = 0

    return False

def create_puzzle_board(empty_cells=45):
    """
    Generates a new Sudoku puzzle
    1. Creates an empty 9x9 board
    2. Fills it completely
    3. Removes 'empty_cells' number of cells
    """

    # 1.
    new_board = [[0 for _ in range(9)] for _ in range(9)]

    # 2.
    if not fill_grid_completely(new_board):
        print("Couldn't generate a full Sudoku solution")
        return False

    # 3.
    cells_removed_count = 0

    all_cell_coordinates = []
    for row in range(9):
        for col in range(9):
            all_cell_coordinates.append((row, col))

    random.shuffle(all_cell_coordinates) # Shuffle to pick random cells ofr removal

    # Iterate through the shuffled coordinates and remove 'empty_cells'
    for i in range(empty_cells):
        if i < len(all_cell_coordinates):
            row, col = all_cell_coordinates[i]
            if new_board[row][col] != 0:
                new_board[row][col] = 0
                cells_removed_count += 1
            else:
                break

    return new_board

board = create_puzzle_board(empty_cells=45)