from tkinter import *
import tkinter
from tkinter import messagebox
class Table:
   
   # column = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1] 
   # row =    [1, 2, 2, 2, 2, 1, 0, 0, 0, 0]
    def __init__(self,root):
        self.frame=Frame(root)
        self.frame.grid(row=1,column=1)

        self.action_button = [[0 for x in range(total_columns)] for x in range(total_rows)]

        # house of the first player on the board
        self.e = Entry(self.frame, width=5, fg='blue', font=('Arial',16,'bold'))
        self.e.grid(row=1, column=0)
        self.action_button[1][0] = tkinter.Button(self.frame, text=0, state= "disabled", command= lambda x1=1, y1=0: self.move(x1, y1))
        self.action_button[1][0].grid(row=1, column=0, sticky="ew")
        
        # house of the second player on the board
        self.e = Entry(self.frame, width=5, fg='blue', font=('Arial',16,'bold'))
        self.e.grid(row=1, column=5)
        self.action_button[1][5] = tkinter.Button(self.frame, text=0, state= "disabled", command = lambda x1=1, y1=5: self.move(x1, y1))
        self.action_button[1][5].grid(row=1, column=5, sticky="ew")

        # creating buttons
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.e = Entry(self.frame, width=5, fg='blue',
                               font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
                self.action_button[i][j] = tkinter.Button(self.frame, text=lst[i][j], command = lambda x1=i, y1=j: self.move(x1, y1))
                self.action_button[i][j].grid(row=i, column=j, sticky="ew")
        
        # button for a new game
        new_game_button=tkinter.Button(root, text="New game", command=self.new_game)
        new_game_button.grid(row=5,column=0)
        
    
    def move(self, row, column):
        # get the stones number of current pit
        stones = int(self.action_button[row][column]['text'])
        self.action_button[row][column].config(text=0)

        # split the stones to the next pits (anti-clockwise)
        while (stones > 0):
            if row == 0:
                while (column > 1 and stones > 0):
                    column = column - 1
                    newStones = int(self.action_button[row][column]['text']) + 1
                    self.action_button[row][column].config(text=newStones)
                    stones = stones - 1
                
                if (column == 1  and stones > 0): 
                    newStones = int(self.action_button[1][0]['text']) + 1
                    self.action_button[1][0].config(text=newStones)
                    row = 2
                    column = 0
            else:
                while (column < total_columns - 2 and stones > 0):
                    column = column + 1
                    newStones = int(self.action_button[row][column]['text']) + 1
                    self.action_button[row][column].config(text=newStones)
                    stones = stones - 1
                
                if (column == total_columns - 2 and stones > 0): 
                    newStones = int(self.action_button[1][5]['text']) + 1
                    self.action_button[1][5].config(text=newStones)
                    row = 0
                    column = total_columns - 1

            stones = stones - 1
    
    def choice(self, option):
        pop.destroy()
        # reinitiliaze the board with the default values
        for i in range(0, total_rows,2):
            for j in range(1, total_columns-1):
                self.action_button[i][j].config(text=4)

        self.action_button[1][0].config(text=0) 
        self.action_button[1][5].config(text=0)

        # choose the number of players
        if option == "1":
            print ("Some code here...")
        else:
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

# take the data
lst = [(0, 4, 4 ,4, 4, 0),
       (0, 0, 0, 0, 0, 0),
       (0, 4, 4 ,4, 4, 0)]
  
# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])