
import math
import numpy as np

class MiniMax:
  def __init__(self, board):

        total_rows = len(board)
        total_columns = len(board[0])
 
        # convert the board into a matrix of integers
        matrix = np.zeros((total_rows, total_columns))
        matrix[1][0] = int(board[1][0]['text'])
        matrix[1][total_columns - 1] = int(board[1][total_columns - 1]['text'])
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                matrix[i][j] = int(board[i][j]['text'])
        
        best_score = float('-inf')
        self.best_move  = -1

        # for each available move, compute the AI score and choose the best move
        for i in range(1, len(matrix[0]) - 1):
              search_matrix = matrix.copy()

              if (search_matrix[0][i] > 0) :
                  # initialize the parameters for a new search
                  depth = 5
                  max_turn = True
                  alfa = float('-inf')
                  beta = float('inf')
                  
                  # compute the AI score based on the minimax algorithm
                  ai_score = self.minimax(depth, max_turn, search_matrix, i, alfa, beta)
                  print (ai_score)
                 
                  # choose the best move based on the based score
                  if ai_score >= best_score:
                      best_score = ai_score
                      self.best_move  = i

       
  def minimax (self, cur_depth, max_turn, board, move, alfa, beta):
      
      # base case : targetDepth reached
      if (cur_depth == 0 or self.is_end_game(board)):
          return self.evaluate(board, move)
      
      if (max_turn):
          max_eval = float('-inf')
          result = self.move(board, 0, move, max_turn)
          new_board = result[0]
          # after each move, check if the game ended
          if (self.is_end_game(result[0])):
              return self.evaluate(new_board, move)
          
          for i in range(1, len(board[0]) - 1):
                # get the new board and the turn after the movement
                new_board = result[0]
                changing_turn = result[1]

                # check if the turn ended or the player can do another move
                if changing_turn:
                    # check if it is an available move to do
                    if (new_board[2][i] > 0) :
                        # change turn
                        max_turn = False
                        eval = self.minimax(cur_depth-1, max_turn, new_board, i, alfa, beta)
                        max_eval = max(max_eval, eval)
                        alfa = max(alfa, max_eval)
                        if (beta <= alfa):
                            break
                else:
                    if (new_board[0][i] > 0) :
                        # do not change turn
                        max_turn = True
                        # apply minimax algorithm with the same depth (one more move for the same player)
                        eval =  self.minimax(cur_depth, max_turn, new_board, i, alfa, beta)
                        max_eval = max(max_eval, eval)
                        alfa = max(alfa, max_eval)
                        if (beta <= alfa):
                            break
          return max_eval
      
      else:
          min_eval = float('inf')
          result = self.move(board, 2, move, max_turn)
          new_board = result[0]
          # after each move, check if the game ended
          if (self.is_end_game(result[0])):
            return self.evaluate(new_board, move)
          
          for i in range(1, len(board[0])-1):
                # update the board and the turn after each movement
                new_board = result[0]
                changing_turn = result[1]

                # check if the turn ended or the player can do another move
                if changing_turn:
                    # check if it is an available move to do
                    if (new_board[0][i] > 0) :
                        # change turn
                        max_turn = True
                        eval = self.minimax(cur_depth - 1, max_turn, new_board, i, alfa, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, min_eval)
                        if (beta <= alfa):
                            break
                else:
                    if (new_board[2][i] > 0) :
                        # do not change turn
                        max_turn = False
                        # apply minimax algorithm with the same depth (one more move for the same player)
                        eval =  self.minimax(cur_depth, max_turn, new_board, i, alfa, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, min_eval)
                        if (beta <= alfa):
                            break
          return min_eval
      
  def evaluate(self, board, move):
      # number of stones of AI store
      store_AI = board[1][0]
      # number of stones of player store
      store_player = 0.5 * board[1][len(board[0]) - 1]
      # check if the last move was the right most move
      right_most_move = 0.5 * self.rightMost(move, board)
      
      return store_AI - store_player + right_most_move

  def rightMost(self, move, board):
      is_right_most = False
      for i in range(1, len(board[0])-1):
          if (board[0][i] > 0):
            if (i == move):
                is_right_most = True
            break
      if (is_right_most == False):
        return 0
      return 1       
              

  def move(self, new_board, row, column, max_turn):
          board = new_board.copy()
          # find total number of columns in list
          total_columns = len(board[0])
          # get the stones number of current pit
          stones = board[row][column]
          if (stones != 0):
              board[row][column] = 0
              changing_turn = True
              # split the stones to the next pits (anti-clockwise)
              while (stones > 0):
                  # north side player
                  if row == 0:
                      while (column > 1 and stones > 0):
                          column = column - 1
                          new_stones = board[row][column] + 1
                          stones = stones - 1

                          # steal the stones from the south position if the first player ends up in a empty pit
                          if stones == 0 and max_turn == True and new_stones == 1 and board[2][column] != 0:
                              board[row][column] = 0 
                              board[1][0] = board[1][0] + board[2][column] + 1
                              board[2][column] = 0
                          else:
                              board[row][column] = new_stones

                      # move to south side
                      if (column == 1  and stones > 0):
                          row = 2
                          column = 0 

                          # deposit one stone in your store if it is first player turn
                          if (max_turn == True):
                              stones = stones - 1
                              board[1][0] = board[1][0] + 1
                              if stones == 0:
                                  changing_turn = False

                  # south side player
                  else:
                      while (column < total_columns - 2 and stones > 0):
                          column = column + 1
                          new_stones = board[row][column] + 1
                          stones = stones - 1

                          # steal the stones from the north position if the second player ends up in a empty pit
                          if stones == 0 and max_turn == False and new_stones == 1 and board[0][column] != 0:
                              board[row][column] = 0
                              board[1][total_columns - 1] = board[1][total_columns - 1] + board[0][column] + 1
                              board[0][column] = 0
                          else:
                              board[row][column] = new_stones

                      # move to north side
                      if (column == total_columns - 2 and stones > 0):
                          row = 0
                          column = total_columns - 1

                          # deposit one stone in your store if it is second player turn
                          if max_turn == False:
                              stones = stones - 1
                              board[1][total_columns - 1] = board[1][total_columns - 1] + 1
                              if stones == 0:
                                  changing_turn = False
              return board, changing_turn

  def is_end_game(self, board):
        total_columns = len(board[0])
        stones0 = 0
        stones2 = 0

        # sum the number of stones for each player
        for j in range(1, total_columns-1):
            stones0 = stones0 + int(board[0][j])
            stones2 = stones2 + int(board[2][j])
        
        if (stones0 == 0 or stones2 == 0):
            return True
        return False