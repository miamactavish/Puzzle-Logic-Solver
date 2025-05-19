import math
import network

curr_size = 4
width = curr_size
height = curr_size
board = []
symbols = []
for i in range(curr_size):
    row = []
    sym_row = []
    for j in range(curr_size):
        row.append(' ')
        sym_row.append(' ')
    board.append(row)
    symbols.append(sym_row)
    

def print_board():
    for i in range (height):
        row = board[i]
        row_str = ""
        for j in range(len(row)):
            piece = row[j]
            row_str += " " + piece + " "

            # add > or < symbols
            if symbols[i][j] == '^' or symbols[i][j] == 'v':
                row_str += " "
            else:
                row_str += symbols[i][j]

        print(row_str)

        row_str = ""
        # Add ^ or v symbols
        for j in range(len(row)):
            if symbols[i][j] == '>' or symbols[i][j] == '<':
                row_str += "    "
            else:
                row_str += " " + symbols[i][j] + "  "
        print(row_str)

    print()

task, param = (network.get_puzzle(f"https://www.puzzle-futoshiki.com/futoshiki-4x4-easy/"))

task = task.split(',')[:-1]
# parse puzzle from get request
for i in range(len(task)):
    # Letters after the initial character determine whether there are > or < symbols next to this cell
    x = i % width
    y = math.floor(float(i) / width)
    board[y][x] = task[i][0] # first character of this element is the actual number at this cell (or 0 if it's empty)
    
    char = task[i]
    for j in range(len(char)):
        if j == 0:
            continue
        if char[j] == 'U':
            symbols[y-1][x] = '^'
        elif char[j] == 'D':
            symbols[y][x] = 'v'
        elif char[j] == 'L':
            symbols[y][x-1] = '<'
        elif char[j] == 'R':
            symbols[y][x] = '>'
        
       
print_board()

#submit(param, solution)