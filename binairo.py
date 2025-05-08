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
    f"https://www.puzzles-mobile.com/binairo/random/{curr_size}/get?fromSolved="
)
post_puzzle_url = f"https://www.puzzles-mobile.com/slant/random/{curr_size}"

def get_puzzle() -> tuple[str, str]:
  """returns task string and a token, which you need to link the retrieved puzzle to your solution submission later"""
  resp: dict[str, str] = requests.get(
    url=get_puzzle_url
  ).json()
  print(resp)
  print(requests.get(
    url=get_puzzle_url
  ))
  return resp["task"], resp["token"]

def submit(token: str, solution: str) -> bool:
  """submits the solution for checking"""
  resp = requests.post(
    url=post_puzzle_url,
    data={
      "token": token,
      "solution": solution
    },
  ).json()
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


#task, token = (get_puzzle())

#TEMP: overwrite to work w a specific puzzle
task = 'b1a1a0e00a0j1d0c0'

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
    has_change = fill_around_2()

has_change = True
while has_change:
    has_change = fill_gaps()

for row in board:
    print(row)