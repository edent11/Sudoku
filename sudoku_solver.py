import random
import copy

def valid_check(board, row, col, new_number):
  """
    valid_check makes validation of number in place board[row][col].

    :param board: Sudoku board 
    :param row: row's index
    :param col: column's index
    :param new_number: optional number to check it's validity
    :return: True if board[row][col] valued as new_number is valid , False otherwise
  """ 
  cube_dim = len(board)
  # checks if new_number shows up in row or column.
  for index in range (0, cube_dim):
    if board[row][index] == new_number or board[index][col] == new_number:
      return False
  
  # start_row and start_col makes the first cell in 3x3 cube which allowed to have one of every number 
  if row % 3 == 0:
    start_row = row
  elif row % 3 == 1:
    start_row = row - 1
  elif row % 3 == 2:
    start_row = row - 2
      
  if col % 3 == 0 :
    start_col = col
  elif col % 3 == 1:
    start_col = col - 1
  elif col % 3 == 2:
    start_col = col - 2
    
  for cube_row in range (start_row, start_row + 3):
    if cube_row == row:
      continue
    for cube_col in range (start_col, start_col + 3):
      if cube_col == col:
        continue
      if board[cube_row][cube_col] == new_number:
        return False
  return True    
  

def check_possibilities(board, row, col):
  """
    check_possibilities makes list of possible numbers in place board[row][col] according to Sudoku restrictions.

    :param board: Sudoku board 
    :param row: row's index
    :param col: column's index
    :return: list of possible numbers
  """
  possible_numbers = []
  cube_dim = len(board)
  # loop over all numbers and list valid numbers in possible_numbers list.
  for number in range (1, cube_dim + 1):
    if valid_check(board, row, col, number):
      possible_numbers.append(number)
  return possible_numbers

def random_possibility(possible_numbers):
  """
    random_possibility randoms value in list, removes and returns this value.

    :param possible_numbers: list of values 
    :return: random value from the list.
  """
  number = random.choice(possible_numbers)  
  possible_numbers.remove(number)
  return number
 

def next_cell(board, row, col):
  """
    next_cell checks for the next empty cell in the board.

    :param board: Sudoku board 
    :param row: current row's index
    :param col: current column's index
    :return: row and column of the next empty cell if exists, otherwise None.
  """
  
  cube_dim = len(board)  
  for row_board in range (0, cube_dim):
    for col_board in range (0, cube_dim): 
      if row_board == row and col_board == col:
        continue
      if board[row_board][col_board] == 0:     
        return row_board, col_board
  return None, None    
       
  

def make_solution(board, row, col):
  """
    make_solution solve Sudoku board using Backtracking system and returns True if solution exists, otherwise False.

    :param board: Sudoku board 
    :param row: current row's index
    :param col: current column's index
    :return: True if solution exists, False otherwise.
  """
  # if the board is solved, return True.
  if row == None:
    return True
  # get the next empty cell in the board.
  new_row, new_col = next_cell(board, row, col)
  
  # in case that the first cell is not empty.
  if(board[row][col] != 0):
     solution = make_solution(board, new_row, new_col)
  else:
     
    solution = False
    # create list of possible numbers to put in board[row][col].
    possible_numbers = check_possibilities(board, row, col) 
    
    # loop through all possible numbers as long as solution is not found.
    while not solution and len(possible_numbers) > 0:
          
      board[row][col] = random_possibility(possible_numbers)   
      solution = make_solution(board, new_row, new_col)  
  
  # backtrack in order to find solution and delete the last try from the board.     
  if not solution:
    board[row][col] = 0
    return False
  
  # if the solution is found, return True.
  return True

def make_hint(board, row, col):
  """
    make_hint makes hint for value in place board[row][col] by solving the current board.

    :param board: Sudoku board 
    :param row: current row's index
    :param col: current column's index
    :return: The solution in place board[row][col].
  """
  
  temp_board = copy.deepcopy(board)
  make_solution(temp_board)
  return temp_board[row][col]
      
def print_board(board):
  for row in range(0, 9):
    if row % 3 == 0 and row != 0:
      print("______________________________", end="\n")
    
    for col in range(0, 9):
      if col % 3 == 0:
        print("||", end=" ")
      print(board[row][col], end=" ")
    print()  

  
   
# def main():
#   board = [[5, 0, 0, 0, 6, 0, 0, 0, 0],
#            [0, 0, 4, 5, 0, 7, 0, 9, 0],
#            [0, 3, 0, 0, 0, 0, 8, 0, 0],
#            [8, 0, 0, 2, 0, 6, 9, 0, 0],
#            [0, 0, 0, 0, 4, 0, 0, 6, 0], 
#            [0, 0, 2, 0, 1, 0, 0, 0, 0],
#            [0, 0, 5, 9, 0, 2, 0, 7, 0],
#            [0, 0, 0, 1, 0, 0, 0, 0, 0],
#            [4, 0, 0, 0, 0, 0, 0, 0, 5]]

#   print(board)
#   kif = make_solution(board, 0, 1)
#   print(kif)
#   print_board(board)

# if __name__ == "__main__":
#     main()
