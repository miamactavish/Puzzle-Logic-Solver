import requests
import math

curr_size = "6x6-easy"
height = 6
width = 6
board = []
for i in range(height):
    row = []
    for j in range(width):
        row.append(' ')
    board.append(row)
      

get_puzzle_url = (
    #f"https://www.puzzles-mobile.com/binairo/random/{curr_size}/get?fromSolved="
    f"https://www.puzzle-binairo.com/binairo-{curr_size}"

)
post_puzzle_url = f"https://www.puzzles-mobile.com/binairo/random/{curr_size}"

def get_puzzle():
    # Send a POST request to get a new puzzle
    resp = requests.post(
        url=get_puzzle_url,
        data={
        "new": "   New Puzzle   "
        },
        cookies={
        "api-token": "To9fqzSnyTdA9kOxjYfFRznIlD3KLjAdVbMiBeXY8Y0PX6uyIeVZXBVuDQmy",
        }
    )
    # The response we get is the entire html for a page with a new puzzle.
    # Parse it to find the puzzle data.
    html = resp.text
    task_index = html.find("var task = '") + len("var task = '")
    task = ""
    while html[task_index] != "'":
        task += html[task_index]
        task_index += 1
    
    print(task)

    param_index = html.find('name=" param " value="') + len('name=" param " value="')
    while html[param_index] != '"':
        param += html[param_index]
        param_index += 1

    return task, param

def submit(token, solution):
  """submits the solution for checking"""
  resp = requests.post(
        url=get_puzzle_url,
        data={
        "param": param,
        "ansH": solution,
        "robot": "1",
        "ready": "1"
        },
        cookies={
        "api-token": "To9fqzSnyTdA9kOxjYfFRznIlD3KLjAdVbMiBeXY8Y0PX6uyIeVZXBVuDQmy",
        }
    )
  print(resp) # testing purposes
  return resp["status"]

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

# find the number of times a piece occurs in a given row.
def get_col_count(piece, col):
    count = 0
    for i in range(height):
        if piece == board[i][col]:
            count += 1
    return count

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

task = (get_puzzle())

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
       
for row in board:
    print(row)
print()
# now work on actually solving
# find places with two consecutive pieces of the same colour
has_change = True
while has_change:
    has_change = fill_around_2() or fill_gaps() or fill_complete_rows('0') or fill_complete_rows('1') or \
                 fill_complete_columns('0') or fill_complete_columns('1')

for row in board:
    print(row)

solution = ""
for row in board:
    for piece in row:
        solution += piece

#submit(token, solution)