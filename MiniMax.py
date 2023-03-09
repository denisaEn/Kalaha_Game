
import math
import numpy as np

class MiniMax:
  def __init__(self, board):
        depth = 5
        self.maxTurn = True

        total_rows = len(board)
        total_columns = len(board[0])

        matrix = np.zeros((total_rows, total_columns))
        matrix[1][0] = int(board[1][0]['text'])
        matrix[1][total_columns - 1] = int(board[1][total_columns - 1]['text'])
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                matrix[i][j] = int(board[i][j]['text'])

        search_matrix = [[0 for x in range(total_columns)] for x in range(total_rows)]
        best_score = float('-inf')
        self.best_move  = - 1
        search_matrix = matrix.copy()

        print("Ai score")
        for i in range(1, len(matrix[0])):
              search_matrix = matrix.copy()
              if (search_matrix[0][i] > 0) :
                  depth = 5
                  self.maxTurn = True
                  ai_score = self.minimax(depth, self.maxTurn, search_matrix)
                  print (ai_score)
                  if ai_score > best_score:
                      best_score = ai_score
                      self.best_move  = i

       
  def minimax (self, curDepth, maxTurn, board):
      
      # base case : targetDepth reached
      if (curDepth == 0):
          return board[1][0]
      if (maxTurn):
          maxEval = float('-inf')
          for i in range(1, len(board[0])):
              if (board[0][i] > 0) :
                #print("Old board")
                #print(i, curDepth, self.maxTurn )
                #print (board)
                result = self.move(board, 0, i, maxTurn)
                newboard = result[0].copy()
                changingTurn = result[1]
                if changingTurn:
                    maxTurn = not maxTurn
                    eval = self.minimax(curDepth-1, maxTurn, newboard)
                else:
                    #print (newboard)
                    eval = newboard[1][0] - board[1][0] + self.minimax(curDepth, maxTurn, newboard)
                maxEval = max(maxEval, eval)
          return maxEval
      
      else:
          minEval = float('inf')
          for i in range(1, len(board[0])):
              if (board[2][i] > 0) :
                #print("Old board")
                #print(i, curDepth,  self.maxTurn)
                #print (board)
                result = self.move(board, 2, i, maxTurn)
                newboard = result[0].copy()
                changingTurn = result[1]
                if changingTurn:
                    maxTurn = not maxTurn
                    eval = self.minimax(curDepth - 1, maxTurn, newboard)
                else:
                    #print(newboard)
                    eval = newboard[1][0] - board[1][0] + self.minimax(curDepth, maxTurn, newboard)
                minEval = min(minEval, eval)
          return minEval

  def move(self, newboard, row, column, maxTurn):
          board = newboard.copy()
          # find total number of columns in list
          total_columns = len(board[0])
          # get the stones number of current pit
          stones = board[row][column]
          if (stones != 0):
              board[row][column] = 0
              changingTurn = True
              # split the stones to the next pits (anti-clockwise)
              while (stones > 0):
                  if row == 0:
                      while (column > 1 and stones > 0):
                          column = column - 1
                          newStones = board[row][column] + 1
                          stones = stones - 1
                          if stones == 0 and maxTurn == True and newStones == 1 and board[2][column] != 0:
                              board[row][column] = 0 
                              board[1][0] = board[1][0] + board[2][column] + 1
                              board[2][column] = 0
                          else:
                              board[row][column] = newStones

                      if (column == 1  and stones > 0):
                          row = 2
                          column = 0 
                          if (maxTurn == True):
                              stones = stones - 1
                              board[1][0] = board[1][0] + 1
                              if stones == 0:
                                  changingTurn = False
                  else:
                      while (column < total_columns - 2 and stones > 0):
                          column = column + 1
                          newStones = board[row][column] + 1
                          stones = stones - 1
                          if stones == 0 and maxTurn == False and newStones == 1 and board[0][column] != 0:
                              board[row][column] = 0
                              board[1][total_columns - 1] = board[1][total_columns - 1] + board[0][column] + 1
                              board[0][column] = 0
                          else:
                              board[row][column] = newStones
            
                      if (column == total_columns - 2 and stones > 0):
                          row = 0
                          column = total_columns - 1
                          if maxTurn == False:
                              stones = stones - 1
                              board[1][total_columns - 1] = board[1][total_columns - 1] + 1
                              if stones == 0:
                                  changingTurn = False
              return board, changingTurn
