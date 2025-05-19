import math
import network

get_url = "https://www.puzzle-futoshiki.com/futoshiki-7x7-easy/"
curr_size = 7
width = curr_size
height = curr_size
board = []
symbols = []
notes = []
for i in range(curr_size):
    row = []
    sym_row = []
    for j in range(curr_size):
        row.append(' ')
        sym_row.append(' ')
    board.append(row)
    symbols.append(sym_row)

    notes_row = []
    for j in range(curr_size):
        notes_cell = []
        for k in range(curr_size):
            notes_cell.append(k+1)
        notes_row.append(notes_cell)
    notes.append(notes_row)

def print_board():
    for i in range (height):
        row = board[i]
        row_str = ""
        for j in range(len(row)):
            piece = str(row[j])
            row_str += " " + piece + " "

            # add > or < symbols
            if '>' in symbols[i][j]:
                row_str += '>'
            elif '<' in symbols[i][j]:
                row_str += '<'
            else:
                row_str += " "

        print(row_str)

        row_str = ""
        # Add ^ or v symbols
        for j in range(len(row)):
            if '^' in symbols[i][j]:
                row_str += " ^  "
            
            elif 'v' in symbols[i][j]:
                row_str += " v  "
            
            else:
                row_str += "    "
        print(row_str)

    print()

def row_has_num(row, num):
    if num in board[row]:
        return True
    return False

def col_has_num(col, num):
    for i in range(width):
        if board[i][col] == num:
            return True
    return False

def clear_note_row(row, num):
    has_change = False
    for i in range(curr_size):
        if board[row][i] == 0 and num in notes[row][i]:
            notes[row][i].remove(num)
            has_change = True
    return has_change

def clear_note_col(col, num):
    has_change = False
    for i in range(curr_size):
        if board[i][col] == 0 and num in notes[i][col]:
            notes[i][col].remove(num)
            has_change = True
    return has_change

def find_only_option_row(row, num):
    count = 0
    index = -1
    for i in range(width):
        if num in notes[row][i]:
            count += 1
            index = i
            if count > 1:
                return False
        if board[row][i] == num:
            return False
            
    if count == 1:
        board[row][index] = num
        notes[row][index].clear()
        clear_note_row(row, num)
        clear_note_col(index, num)
        return True
    return False


def find_only_option_col(col, num):
    count = 0
    index = -1
    for i in range(height):
        if num in notes[i][col]:
            count += 1
            index = i
            if count > 1:
                return False
        if board[i][col] == num:
            return False
            
    if count == 1:
        board[index][col] = num
        notes[index][col].clear()
        clear_note_row(index, num)
        clear_note_col(col, num)
        return True
    return False

def find_onlys():
    has_change = False
    for num in range(1, curr_size + 1):
        for row in range(width):
            if find_only_option_row(row, num):
                has_change = True
        for col in range(height):
            if find_only_option_col(col, num):
                has_change = True
    return has_change

# get either the smallest/largest note, or the current cell value
def get_extreme(row, col, index):
    if board[row][col] > 0:
        return board[row][col]
    else:
        return notes[row][col][index]

def update_comparison_notes(row, col):
    has_change = False
    #Find where this element is greater than others
    smallest = -1
    updating = False
    if '>' in symbols[row][col]:
        s = get_extreme(row, col+1, 0)
        if s > smallest:
            smallest = s
            updating = True

    if 'v' in symbols[row][col]:
        s = get_extreme(row+1, col, 0)
        if s > smallest:
            smallest = s
            updating = True


    if col > 0 and '<' in symbols[row][col - 1]:
        s = get_extreme(row, col-1, 0)
        if s > smallest:
            smallest = s
            updating = True


    if row > 0 and '^' in symbols[row - 1][col]:
        s = get_extreme(row-1, col, 0)
        if s > smallest:
            smallest = s
            updating = True

    if updating:
        for i in range(1, smallest+1):
            if i in notes[row][col]:
                notes[row][col].remove(i)
                has_change = True

    # now check for cells that are larger than this cell
    largest = 100
    updating = False
    if '<' in symbols[row][col]:
        l = get_extreme(row, col+1, -1)
        if l < largest:
            largest = l
            updating = True

    if row > 0 and 'v' in symbols[row-1][col]:
        l = get_extreme(row-1, col, -1)
        if l < largest:
            largest = l
            updating = True

    if col > 0 and '>' in symbols[row][col-1]:
        l = get_extreme(row, col-1, -1)
        if l < largest:
            largest = l
            updating = True

    if '^' in symbols[row][col]:
        l = get_extreme(row+1, col, -1)
        if l < largest:
            largest = l
            updating = True

    if updating:
        for i in range(largest, curr_size+1):
            if i in notes[row][col]:
                notes[row][col].remove(i)
                has_change = True
    
    return has_change

def update_all_comparison_notes():
    has_change = False
    for i in range(height):
        for j in range(width):
            if update_comparison_notes(i, j):
                has_change = True
                #print("updated notes at " + str(i) + ", " + str(j))
    return has_change

def only_one_option(row, col):
    if len(notes[row][col]) == 1:
        board[row][col] = notes[row][col][0]
        notes[row][col].clear()
        return True
    return False

def check_all_only_one_option():
    has_change = False
    for i in range(height):
        for j in range(width):
            if only_one_option(i, j):
                has_change = True
    return has_change

# Update stored cell possibilities based on existing information
def update_notes(i, j):
    return clear_note_row(i, board[i][j]) or clear_note_col(j, board[i][j])

def update_all_notes():
    has_change = False
    for i in range(height):
        for j in range(width):
            if board[i][j] != 0:
                if update_notes(i, j):
                    has_change = True
    return has_change

task, param = (network.get_puzzle(get_url))

task = task.split(',')[:-1]
print(task)

# parse puzzle from get request
for i in range(len(task)):
    # Letters after the initial character determine whether there are > or < symbols next to this cell
    x = i % width
    y = math.floor(float(i) / width)
    board[y][x] = int(task[i][0]) # first character of this element is the actual number at this cell (or 0 if it's empty)
    if board[y][x] > 0:
        notes[y][x].clear()

    char = task[i]
    for j in range(len(char)):
        if j == 0:
            continue
        if char[j] == 'U':
            symbols[y-1][x] += '^'
        elif char[j] == 'D':
            symbols[y][x] += 'v'
        elif char[j] == 'L':
            symbols[y][x-1] += '<'
        elif char[j] == 'R':
            symbols[y][x] += '>'

has_change = True
while has_change:
    # Separate them so that python doesn't short-circuit as soon as one evaluates to true
    note = update_all_notes() 
    only = find_onlys() 
    comparison = update_all_comparison_notes() 
    one = check_all_only_one_option()

    has_change = note or only or comparison or one

    print_board()
    input()

print_board()
print(notes)

#submit(param, solution)