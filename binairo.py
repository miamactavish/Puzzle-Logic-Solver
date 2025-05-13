import math
import network

curr_size = 10
width = curr_size
height = curr_size
board = []
for i in range(curr_size):
    row = []
    for j in range(curr_size):
        row.append(' ')
    board.append(row)
    

def print_board():
    for i in range (height):
        row = board[i]
        row_str = ""
        for piece in row:
            if piece == " ":
                row_str += "- " 
            else:
                row_str += piece + " "
        
        row_str += "| " + str(get_remaining_row("0", i)) + ", " + str(get_remaining_row("1", i) )
        print(row_str)
    
    bottom = ""
    for i in range(width):
        bottom += "--"
    print(bottom)

    count_str = ""
    for i in range(width):
        count_str += str(get_remaining_col("0", i)) + " "
    print(count_str)
    count_str = ""
    for i in range(height):
        count_str += str(get_remaining_col("1", i)) + " "
    print(count_str)  

    print()

# place a piece in the specified location. Accounts for out-of range errors
def place_piece(piece, x, y, x_dir, y_dir):
    new_x = x + x_dir
    new_y = y + y_dir
    if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
        if board[new_y][new_x] == ' ':
            board[new_y][new_x] = piece
            return True

    return False

def get_opposite(piece):
    if piece == '0':
        return '1'
    else:
        return '0'

# fill pieces around areas with two consecutive pieces of the same type. --00-- becomes -1001-, for example
def fill_around_2():
    has_change = False
    # check horizontally first
    for i in range(height):
        for j in range(width - 1):
            if board[i][j] != ' ':
                piece = board[i][j]
                if board[i][j + 1] == piece:
                    opp = get_opposite(piece)
                    # log that a change was made if a new piece is successfully placed
                    if place_piece(opp, j, i, -1, 0) or place_piece(opp, j, i, 2, 0):
                        has_change = True

    # now check vertically
    for i in range(height - 1):
        for j in range(width):
            if board[i][j] != ' ':
                piece = board[i][j]
                if board[i + 1][j] == piece:
                    opp = get_opposite(piece)
                    # log that a change was made if a new piece is successfully placed
                    if place_piece(opp, j, i, 0, -1) or place_piece(opp, j, i, 0, 2):
                        has_change = True

    return has_change

# fill in gaps where a line of three would be created. --0-0-- becomes --010--, for example
def fill_gaps():
    has_change = False
    # check horizontally first
    for i in range(height):
        for j in range(width - 2):
            if board[i][j] != ' ':
                piece = board[i][j]
                if board[i][j + 1] == ' ' and board[i][j + 2] == piece:
                    opp = get_opposite(piece)
                    # log that a change was made if a new piece is successfully placed
                    if place_piece(opp, j, i, 1, 0):
                        has_change = True

    # now check vertically
    for i in range(height - 2):
        for j in range(width):
            if board[i][j] != ' ':
                piece = board[i][j]
                if board[i + 1][j] == ' ' and board[i + 2][j] == piece:
                    opp = get_opposite(piece)
                    # log that a change was made if a new piece is successfully placed
                    if place_piece(opp, j, i, 0, 1):
                        has_change = True

    return has_change

# find the number of times a piece occurs in a given row.
def get_row_count(piece, row):
    count = 0
    for p in board[row]:
        if piece == p:
            count += 1
    return count

def get_remaining_row(piece, row):
    return int((width / 2) - get_row_count(piece, row))

# find the number of times a piece occurs in a given row.
def get_col_count(piece, col):
    count = 0
    for i in range(height):
        if piece == board[i][col]:
            count += 1
    return count

def get_remaining_col(piece, col):
    return int((height / 2) - get_col_count(piece, col))

# if a row already has all of one piece placed, fill the rest with the remaining piece
def fill_complete_rows(piece):
    has_change = False
    for i in range(height):
        if get_row_count(piece, i) == (width / 2.0):
            for j in range(width):
                if board[i][j] == ' ':
                    board[i][j] = get_opposite(piece)
                    has_change = True
    return has_change

# if a column already has all of one piece placed, fill the rest with the remaining piece
def fill_complete_columns(piece):
    has_change = False
    for i in range(width):
        if get_col_count(piece, i) == (height / 2.0):
            for j in range(height):
                if board[j][i] == ' ':
                    board[j][i] = get_opposite(piece)
                    has_change = True
    return has_change

'''
A "guaranteed placement" is a row where you may not know exactly where a piece goes,
but information about the remaining amount of pieces tells you a *range* of spaces within which
it must be placed. For example in the following row:
1 - - 0 1 - 0 1 | 2, 1
the remaining 1 must go in one of the two leftmost empty spaces, otherwise you will get
three consecutive 0's in a row. 
'''
def find_guaranteed_placements_row():
    has_change = False
    for i in range(height):
        piece = ""
        rem_0 = get_remaining_row("0", i)
        rem_1 = get_remaining_row("1", i)
        if rem_0 == 1 and rem_1 > 1:
            piece = "0"
        elif rem_0 > 1 and rem_1 == 1:
            piece = "1"
        else:
            continue
        
        # find the starting place of a forced placement range
        starts = []
        opposite = get_opposite(piece)
        for j in range(width - 2):
            if board[i][j] != piece and board[i][j+1] != piece and board[i][j+2] != piece:
                starts.append(j)

        for start in starts:
            print("Has row? Start at " + str(start))
            print(board[i])
            for j in range(width):
                if j == start or j == start + 1 or j == start + 2 or board[i][j] != " ":
                    continue
                else:
                    print("Has row " + str(i))
                    print(board[i])
                    board[i][j] = opposite
                    has_change = True
                    print(board[i])

    return has_change
            

def find_guaranteed_placements_col():
    has_change = False
    for j in range(width):
        piece = ""
        rem_0 = get_remaining_col("0", j)
        rem_1 = get_remaining_col("1", j)
        if rem_0 == 1 and rem_1 > 1:
            piece = "0"
        elif rem_0 > 1 and rem_1 == 1:
            piece = "1"
        else:
            continue
        
        # find the starting place of a forced placement range
        starts = []
        opposite = get_opposite(piece)
        for i in range(height - 2):
            if board[i][j] != piece and board[i+1][j] != piece and board[i+2][j] != piece:
                starts.append(i)

        for start in starts:
            for i in range(height):
                if i == start or i == start + 1 or i == start + 2 or board[i][j] != " ":
                    continue
                else:
                    print("Has col " + str(i))
                    #print(board[i])
                    board[i][j] = opposite
                    has_change = True
                    #print(board[i])

    return has_change

task, param = (network.get_puzzle(f"https://www.puzzle-binairo.com/binairo-10x10-hard"))

cur_index = 0
# parse puzzle from get request
for char in task:
    # numberical characters encode how many empty spaces there are before the next filled space
    if char.isalpha():
       skip = ord(char) - 96

       for i in range(skip):
            cur_index += 1
    
    # otherwise it is just a black or white piece
    else:
        x = cur_index % width
        y = math.floor(float(cur_index) / width)
        board[y][x] = char
        cur_index += 1
       
print_board()

# now work on actually solving
# find places with two consecutive pieces of the same colour
has_change = True
while has_change:
    has_change = fill_around_2() or fill_gaps() or fill_complete_rows('0') or fill_complete_rows('1') or \
                 fill_complete_columns('0') or fill_complete_columns('1') or \
                    find_guaranteed_placements_row() or find_guaranteed_placements_col()


print_board()

solution = ""
for row in board:
    for piece in row:
        solution += piece


#submit(param, solution)