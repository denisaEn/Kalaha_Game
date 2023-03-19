from tkinter import *
import tkinter
from MiniMax import *
from tkinter import messagebox
import tkinter.font as font

class Table:
   
    def __init__(self,root):
        self.frame=Frame(root)
        self.frame.grid(row=1,column=1)

        # initialize parameters
        self.buttons = [[],[]]
        self.nr_players = 1
        # self.turn = 0 - player1, self.turn = 2 - player2
        self.turn = 2
        self.nr_stones = 4
        self.difficulty = "Hard"
        self.create_board(root, self.nr_stones)

    def create_board(self, root, nr_stones):
        button_font = font.Font(size=15)
        house_font  =  font.Font(size=30)
        # create a board with 6 pits for each player
        # row[0] - player1 pits, row[2]-player2 pits
        board = [(0, nr_stones, nr_stones, nr_stones, nr_stones, nr_stones, nr_stones, 0),
                 (0, 0, 0, 0, 0, 0, 0, 0),
                 (0, nr_stones, nr_stones, nr_stones, nr_stones, nr_stones, nr_stones, 0)]
        
        # find total number of rows and columns
        total_rows = len(board)
        total_columns = len(board[0])

        self.buttons = [[0 for x in range(total_columns)] for x in range(total_rows)]
        
        # store of the first player on the board
        self.buttons[1][0] = tkinter.Button(self.frame, text=0, state= "disabled", bg = "#ef1a11", font=house_font, command= lambda row=1, column=0: self.move(self.buttons, row, column))
        self.buttons[1][0].grid(row=1, column=0, sticky="ew")
        
        # store of the second player on the board
        self.buttons[1][total_columns - 1] = tkinter.Button(self.frame, text=0, state= "disabled", font=house_font, bg = "#83a3ee", command = lambda row=1, column=total_columns-1: self.move(self.buttons, row, column))
        self.buttons[1][total_columns - 1].grid(row=1, column=total_columns - 1, sticky="ew")

        # creating buttons
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.e = Entry(self.frame, width=5, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, board[i][j])
                self.buttons[i][j] = tkinter.Button(self.frame, text=board[i][j], command = lambda row=i, column=j: self.move(self.buttons, row, column))
                self.buttons[i][j].grid(row=i, column=j, sticky="ew")
        
        for j in range(1, total_columns-1):
                self.buttons[0][j].config(bg='#d9534f', font=button_font, fg = "white", disabledforeground="#343333", state= "disabled")
                self.buttons[2][j].config(bg='#89cff0', font=button_font, fg = "white", disabledforeground="#343333")
        # button for a new game
        new_game_button=tkinter.Button(self.frame, text="New game", command=self.new_game)
        new_game_button.grid(row=5, column=0)

        # this will create a label widget
        l1 = Label(self.frame, text = "Number players: " + str(self.nr_players))
        l2 = Label(self.frame, text = "Difficulty: " + self.difficulty)
        
        # grid method to arrange labels in respective
        # rows and columns as specified
        l1.grid(row = 6, column = 0, sticky = W, pady = 2)
        l2.grid(row = 7, column = 0, sticky = W, pady = 2)
    
    def move(self, board, row, column):
        total_columns = len(board[0])
        # get the nr_stones of current pit
        stones = int(board[row][column]['text'])
        if (stones != 0):
            board[row][column].config(text=0)
            changing_turn = True
            # split the stones to the next pits (anti-clockwise)
            while (stones > 0):
                # north side player
                if row == 0:
                    while (column > 1 and stones > 0):
                        column = column - 1
                        new_stones = int(board[row][column]['text']) + 1
                        stones = stones - 1

                        # steal the stones from the south position if the first player ends up in a empty pit
                        if stones == 0 and self.turn == 0 and new_stones == 1 and int(board[2][column]['text']) != 0:
                            board[row][column].config(text=0)
                            total_stones = int(board[1][0]['text']) + int(board[2][column]['text']) + 1
                            board[1][0].config(text=total_stones)
                            board[2][column].config(text=0)
                        else:
                            board[row][column].config(text=new_stones)

                    # move to south side
                    if (column == 1  and stones > 0):
                        row = 2
                        column = 0 

                        # deposit one stone in your store if it is first player turn
                        if (self.turn == 0):
                            stones = stones - 1
                            board[1][0].config(text=int(board[1][0]['text']) + 1)
                            if stones == 0 and self.is_end_match() == False:
                                changing_turn = False

                # south side player
                else:
                    while (column < total_columns - 2 and stones > 0):
                        column = column + 1
                        new_stones = int(board[row][column]['text']) + 1
                        stones = stones - 1

                        # steal the stones from the north position if the second player ends up in a empty pit
                        if stones == 0 and self.turn == 2 and new_stones == 1 and int(board[0][column]['text']) != 0:
                            board[row][column].config(text=0)
                            total_stones = int(board[1][total_columns - 1]['text']) + int(board[0][column]['text']) + 1
                            board[1][total_columns - 1].config(text=total_stones)
                            board[0][column].config(text=0)
                        else:
                            board[row][column].config(text=new_stones)

                    # move to north side
                    if (column == total_columns - 2 and stones > 0):
                        row = 0
                        column = total_columns - 1

                        # deposit one stone in your store if it is second player turn
                        if self.turn == 2:
                            stones = stones - 1
                            board[1][total_columns - 1].config(text=int(board[1][total_columns - 1]['text']) + 1)
                            if stones == 0 and self.is_end_match() == False:
                                changing_turn = False

            if (changing_turn == True):
                self.change_turn()
            return changing_turn
            

    def change_turn(self):
        total_columns = len(self.buttons[0])
        if self.is_end_match():
            if (int(self.buttons[1][0]['text']) >  int(self.buttons[1][total_columns - 1]['text'])):
                tkinter.messagebox.showinfo(title="Game over", message="Player 1 won!!")
            elif (int(self.buttons[1][0]['text']) ==  int(self.buttons[1][total_columns - 1]['text'])):
                tkinter.messagebox.showinfo(title="Game over", message="It's a draw!!")
            else:
                tkinter.messagebox.showinfo(title="Game over", message="Player 2 won!!")
            self.new_game()
            return 
        # change turn
        if self.turn == 2:
            self.turn = 0
            for j in range(1, total_columns-1):
                self.buttons[2][j].config(state= "disabled")

            if self.nr_players == 2:
                for j in range(1, total_columns-1):
                    self.buttons[0][j].config(state= "normal")
            else:
                # AI player
                print ("AI algorithm searches for the best move")

                while True and self.is_end_match() == False:
                    # best_move is the index of the first row between 1 and 6
                    best_move = MiniMax(self.buttons, self.difficulty).best_move
                    print("Best move from MiniMax:")
                    print(best_move)

                    changing_turn = self.move(self.buttons, 0, best_move)
                    if changing_turn == True:
                        self.turn = 2
                        break

        elif self.turn == 0:
            self.turn = 2
            for j in range(1, total_columns-1):
                self.buttons[2][j].config(state= "normal")
                self.buttons[0][j].config(state= "disabled")

    def choose_players(self, option):
        total_rows = len(self.buttons)
        total_columns = len(self.buttons[0])
        pop.destroy()
        
        # reinitiliaze the board with default values
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.buttons[i][j].config(text=self.nr_stones)

        self.buttons[1][0].config(text=0) 
        self.buttons[1][total_columns - 1].config(text=0)

        # choose the number of players
        if option == "1":
            self.nr_players = 1
            self.turn = 2
            for j in range(1, total_columns-1):
                self.buttons[2][j].config(state= "normal")
                self.buttons[0][j].config(state= "disabled")
            self.choose_difficulty()
        else:
            self.nr_players = 2
            self.turn = 0
            for j in range(1, total_columns-1):
                self.buttons[2][j].config(state= "disabled")
                self.buttons[0][j].config(state= "normal")
            self.difficulty = "-    "
            l2 = Label(self.frame, text = "Difficulty: " + self.difficulty)
            l2.grid(row = 7, column = 0, sticky = W, pady = 2)
        
        # this will create a label widget
        l1 = Label(self.frame, text = "Number players: " + str(self.nr_players))
        
        
        # grid method to arrange labels in respective
        # rows and columns as specified
        l1.grid(row = 6, column = 0, sticky = W, pady = 2)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        
        l2 = Label(self.frame, text = "Difficulty: " + self.difficulty)
        l2.grid(row = 7, column = 0, sticky = W, pady = 2)
        pop.destroy()

    def choose_difficulty(self):
        global pop
        pop = Toplevel(self.frame)
        pop.title("Difficulty")
        pop.geometry("300x150")
        pop.config(bg="white")
        
        # Create a Label Text
        label = Label(pop, text="Choose difficulty: ")
        label.pack(pady=20)
        
        # Add a Frame
        frame = Frame(pop)
        frame.pack(pady=10)

        # Add Button for making selection
        button1 = Button(frame, text="Easy", command=lambda: self.set_difficulty("Easy"))
        button1.grid(row=0, column=1)
        button2 = Button(frame, text="Hard", command=lambda: self.set_difficulty("Hard"))
        button2.grid(row=0, column=2)
        
    def new_game(self):
        msg_box = tkinter.messagebox.askquestion('New game', 'Do you want to start a new game?', icon='question')
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
            button1 = Button(frame, text="1 player", command=lambda: self.choose_players("1"))
            button1.grid(row=0, column=1)
            button2 = Button(frame, text="2 players", command=lambda: self.choose_players("2"))
            button2.grid(row=0, column=2)

    def is_end_match(self):
        total_columns = len(self.buttons[0])
        is_end_game = False
        stones0 = 0
        stones2 = 0
        for j in range(1, total_columns-1):
            stones0 = stones0 + int(self.buttons[0][j]['text'])
            stones2 = stones2 + int(self.buttons[2][j]['text'])
        
        # Move all stones into store when all opponent pits are empty
        if (stones0 == 0):
            self.buttons[1][total_columns - 1].config(text = (int(self.buttons[1][total_columns - 1]['text']) + stones2))
            for j in range(1, total_columns-1):
                self.buttons[2][j].config(text=0)
            is_end_game = True

        elif (stones2 == 0):
            self.buttons[1][0].config(text = (int(self.buttons[1][0]['text']) + stones0))
            for j in range(1, total_columns-1):
                self.buttons[0][j].config(text=0)
            is_end_game = True
        else:
            is_end_game = False

        return is_end_game
    