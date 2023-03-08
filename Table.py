from tkinter import *
import time
import random
import tkinter
from tkinter import messagebox
from MiniMax import *

class Table:
   
   # column = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1] 
   # row =    [1, 2, 2, 2, 2, 1, 0, 0, 0, 0]
    def __init__(self,root):
        self.frame=Frame(root)
        self.frame.grid(row=1,column=1)

        self.action_button = [[],[]]
        self.nr_players = 1
        self.turn = 2
        self.number_of_Stones = 4
        self.create_board(root, self.number_of_Stones)

    def create_board(self, root, number_of_Stones):
        # take the data
        board = [(0, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, number_of_Stones, 0)]
        # find total number of rows and
        # columns in list
        total_rows = len(board)
        total_columns = len(board[0])

        self.action_button = [[0 for x in range(total_columns)] for x in range(total_rows)]
        
        # house of the first player on the board
        self.e = Entry(self.frame, width=5, fg='blue', font=('Arial',16,'bold'))
        self.e.grid(row=1, column=0)
        self.action_button[1][0] = tkinter.Button(self.frame, text=0, state= "disabled", bg = "#83a3ee", command= lambda x1=1, y1=0: self.move(self.action_button, x1, y1))
        self.action_button[1][0].grid(row=1, column=0, sticky="ew")
        
        # house of the second player on the board
        self.e = Entry(self.frame, width=5, fg='blue', font=('Arial',16,'bold'))
        self.e.grid(row=1, column=total_columns - 1)
        self.action_button[1][total_columns - 1] = tkinter.Button(self.frame, text=0, state= "disabled", bg = "#ef1a11", command = lambda x1=1, y1=5: self.move(self.action_button, x1, y1))
        self.action_button[1][total_columns - 1].grid(row=1, column=total_columns - 1, sticky="ew")

        # creating buttons
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.e = Entry(self.frame, width=5, fg='blue',
                               font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, board[i][j])
                self.action_button[i][j] = tkinter.Button(self.frame, text=board[i][j], command = lambda x1=i, y1=j: self.move(self.action_button, x1, y1))
                self.action_button[i][j].grid(row=i, column=j, sticky="ew")
        
        for j in range(1, total_columns-1):
                self.action_button[0][j].config(bg='#d9534f', state= "disabled")
                self.action_button[2][j].config(bg='#89cff0')
        # button for a new game
        new_game_button=tkinter.Button(root, text="New game", command=self.new_game)
        new_game_button.grid(row=5,column=0)
    
    def move(self, board, row, column):
        # find total number of columns in list
        total_columns = len(board[0])
        # get the stones number of current pit
        stones = int(board[row][column]['text'])
        if (stones != 0):
            board[row][column].config(text=0)
            changingTurn = True
            # split the stones to the next pits (anti-clockwise)
            while (stones > 0):
                if row == 0:
                    while (column > 1 and stones > 0):
                        column = column - 1
                        newStones = int(board[row][column]['text']) + 1
                        stones = stones - 1
                        if stones == 0 and self.turn == 0 and newStones == 1 and int(board[2][column]['text']) != 0:
                            board[row][column].config(text=0)
                            totalStones = int(board[1][0]['text']) + int(board[2][column]['text']) + 1
                            board[1][0].config(text=totalStones)
                            board[2][column].config(text=0)
                        else:
                            board[row][column].config(text=newStones)

                    if (column == 1  and stones > 0):
                        row = 2
                        column = 0 
                        if (self.turn == 0):
                            stones = stones - 1
                            board[1][0].config(text=int(board[1][0]['text']) + 1)
                            if stones == 0 and self.is_end_match() == False:
                                changingTurn = False
                else:
                    while (column < total_columns - 2 and stones > 0):
                        column = column + 1
                        newStones = int(board[row][column]['text']) + 1
                        stones = stones - 1
                        if stones == 0 and self.turn == 2 and newStones == 1 and int(board[0][column]['text']) != 0:
                            board[row][column].config(text=0)
                            totalStones = int(board[1][total_columns - 1]['text']) + int(board[0][column]['text']) + 1
                            board[1][total_columns - 1].config(text=totalStones)
                            board[0][column].config(text=0)
                        else:
                            board[row][column].config(text=newStones)
                    
                    if (column == total_columns - 2 and stones > 0):
                        row = 0
                        column = total_columns - 1
                        if self.turn == 2:
                            stones = stones - 1
                            board[1][total_columns - 1].config(text=int(board[1][total_columns - 1]['text']) + 1)
                            if stones == 0 and self.is_end_match() == False:
                                changingTurn = False

            if (changingTurn == True):
                self.change_turn()
            return changingTurn
            

    def change_turn(self):
        total_columns = len(self.action_button[0])
        self.is_end_match()
        # change turn
        if self.turn == 2:
            self.turn = 0
            for j in range(1, total_columns-1):
                self.action_button[2][j].config(state= "disabled")
            if self.nr_players == 2:
                for j in range(1, total_columns-1):
                    self.action_button[0][j].config(state= "normal")
            else:
                # AI player
                print ("AI algorithm searches for the best move")
                # best_move is the index of the first row between 1 and 6
                #best_move = MiniMax(self.action_button).best_move
                print("Best move from MiniMax:")

                # self.move(self.action_button, 0, best_move)
                while True and self.is_end_match() == False:
                    #while True:
                    #    best_move = random.randint(1,6)
                    #    if int(self.action_button[0][best_move]['text']) != 0:
                    #        break
                    best_move = MiniMax(self.action_button).best_move
                    print(best_move)
                    changingTurn = self.move(self.action_button, 0, best_move)
                    if changingTurn == True:
                        self.turn = 2
                        break
                print("Sleep")
        elif self.turn == 0:
            self.turn = 2
            for j in range(1, total_columns-1):
                self.action_button[2][j].config(state= "normal")
                self.action_button[0][j].config(state= "disabled")

    def choice(self, option):
        total_rows = len(self.action_button)
        total_columns = len(self.action_button[0])
        pop.destroy()
        # reinitiliaze the board with the default values
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.action_button[i][j].config(text=4)

        self.action_button[1][0].config(text=0) 
        self.action_button[1][total_columns - 1].config(text=0)

        # choose the number of players
        if option == "1":
            self.nr_players = 1
            for j in range(1, total_columns-1):
                self.action_button[2][j].config(state= "normal")
                self.action_button[0][j].config(state= "disabled")
            print ("Some code here...")
        else:
            self.nr_players = 2
            for j in range(1, total_columns-1):
                self.action_button[2][j].config(state= "normal")
                self.action_button[0][j].config(state= "normal")
            print ("Some code here...")
    
    def new_game(self):
        msg_box = tkinter.messagebox.askquestion('New game', 'Do you want to start a new game?',
                                        icon='question')
        if msg_box == 'yes':
            global pop
            pop = Toplevel(self.frame)
            pop.title("Number of players")
            pop.geometry("300x150")
            pop.config(bg="white")
            # Create a Label Text
            label = Label(pop, text="Choose the number of player:")
            label.pack(pady=20)
            # Add a Frame
            frame = Frame(pop)
            frame.pack(pady=10)
            # Add Button for making selection
            button1 = Button(frame, text="1 player", command=lambda: self.choice("1"))
            button1.grid(row=0, column=1)
            button2 = Button(frame, text="2 players", command=lambda: self.choice("2"))
            button2.grid(row=0, column=2)

    def is_end_match(self):
        total_columns = len(self.action_button[0])
        is_end_game = False
        stones0 = 0
        stones2 = 0
        for j in range(1, total_columns-1):
            stones0 = stones0 + int(self.action_button[0][j]['text'])
            stones2 = stones2 + int(self.action_button[2][j]['text'])
        
        if (stones0 == 0):
            self.action_button[1][total_columns - 1].config(text = (int(self.action_button[1][total_columns - 1]['text']) + stones2))
            for j in range(1, total_columns-1):
                self.action_button[2][j].config(text=0)
            is_end_game = True
        elif (stones2 == 0):
            self.action_button[1][0].config(text = (int(self.action_button[1][0]['text']) + stones0))
            for j in range(1, total_columns-1):
                self.action_button[0][j].config(text=0)
            is_end_game = True
        else:
            is_end_game = False
        
        if is_end_game == True:
            if (int(self.action_button[1][0]['text']) >  int(self.action_button[1][total_columns - 1]['text'])):
                tkinter.messagebox.showinfo(title="Game over", message="Player 1 won!!")
            elif (int(self.action_button[1][0]['text']) ==  int(self.action_button[1][total_columns - 1]['text'])):
                tkinter.messagebox.showinfo(title="Game over", message="It's a draw!!")
            else:
                tkinter.messagebox.showinfo(title="Game over", message="Player 2 won!!")
            self.new_game()
        return is_end_game