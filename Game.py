import tkinter as tk
import Sudoku_solver as sd
import copy
import random
import time
import threading
from tkinter import messagebox

dict = {}


class Game:

# --- functions ---
    def __init__(self, dim):
        
        self.board = [[]]
        self.dim = dim
        self.root = tk.Tk()
        self.root.title("Sudoku by eDenT")
        self.root.geometry("580x600")
        self.root.resizable(width=False, height=False)
        self.difficulty = {
            "Easy": 1,
            "Medium": 40,
            "Hard": 60
        }
        self.entries = self.grid_layout()
        self.solved = False
        self.grid_menu()
        self.errors = 0
        self.right = 0
        

    def grid_layout(self):
        entries = []
        self.vars = []
            
        for i in range(self.dim*self.dim):
            row = i // self.dim
            col = i % self.dim
            var = tk.StringVar()
            # var.trace_add('write', callback)
            self.vars.append(var)
            entries.append(tk.Entry(self.root, width=3, highlightthickness=3, highlightbackground='#000000', justify='center', bg="blue", font =('Arial', 16, 'bold'), textvariable = var))
            padx = (10, 0) if col in (3, 6) else None
            pady = (10, 0) if row in (3, 6) else None
            entries[i].grid(row=row, column=col, padx=padx, pady=pady, ipadx=5, ipady=5)
            entries[i].config(selectbackground='yellow', foreground='yellow',bg = "green")        
            dict.update({entries[i]: (row,col)})
         
                       
        return entries
    

       
        
    def grid_menu(self):
        color2 = '#05d7ff'
        color3 = '#65e7ff'
        color4 = 'BLACK'
        self.start_btn = tk.Button(self.root, text="Start",
                                   background=color2,
                                   foreground=color4,
                                   activebackground= color3,
                                   activeforeground= color4,
                                   highlightbackground= color2,
                                   highlightthickness=2,
                                   width=4,
                                   height= 1,
                                   border = 0,
                                   font =('Arial', 16, 'bold'),
                                   command=self.start_game)
        
        self.drop_value = tk.StringVar(self.root)
  
        # Set the default value of the variable
        self.drop_value.set("Select Difficulty")
        self.start_btn.grid(row=self.dim * self.dim + 10, column=0, padx=0, pady=5) 
        options_list = ["Easy", "Medium", "Hard"]
        self.difficulty_dropdown = tk.OptionMenu(self.root, self.drop_value, *options_list)
        self.timer_txt = tk.StringVar()                            
        self.difficulty_dropdown.grid(row=self.dim * self.dim + 10, column=2, padx=0, pady=5, columnspan=3) 
        self.timer_txt.set("0")
        label = tk.Label( self.root, textvariable=self.timer_txt, relief= 'raised',font =('Arial', 16, 'bold'))  
        label.grid(row=self.dim * self.dim + 10, column=8)
                    
            
    def loop(self):
        self.root.mainloop() 
          
    def start_game(self):
        self.errors = 0
        self.entries = self.grid_layout()
        self.create_board(difficulty=self.drop_value.get())
        for i in range(self.dim*self.dim):
            row = i // self.dim
            col = i % self.dim
            if self.board[row][col] != 0:
                #self.entries[i].insert(0, str(self.board[row][col]))       
                self.vars[i].set(str(self.board[row][col]))
                self.entries[i].config(state='disabled', disabledforeground="BLACK", disabledbackground="#05d7ff")
            else:
                self.entries[i].bind("<KeyRelease>", self.callback) #keyup
        timer = threading.Thread(target=self.create_timer) 
        timer.start()
        
                            
    def create_board(self, difficulty):
        
        self.board = [[0 for i in range(self.dim)] for i in range(self.dim)]
        print(self.board)
        has_solution = False
        while not has_solution:
            has_solution = sd.make_solution(board = self.board, row= 0, col= 0)         
        self.solution_board = copy.deepcopy(self.board)
        
        count = 0        
        while count < self.difficulty[difficulty]:
            row, col = self.rand_cell()
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count = count + 1 

            
    def callback(self, event):
        
        row,col = dict[event.widget]
        if event.char == str(self.solution_board[row][col]):
            event.widget.config(state='disabled', disabledforeground="BLACK", disabledbackground="#05d7ff")
            self.right = self.right + 1
            print(self.right + self.difficulty[self.drop_value.get()])
            if self.right == self.difficulty[self.drop_value.get()]:
                messagebox.showinfo("You won!", "You won!")
                self.start_game()
        else:
            self.errors = self.errors + 1  
            time.sleep(1)
            self.vars[row * self.dim + col].set("")
            if self.errors == 3:
                messagebox.showerror(title="You Lost", message="You Lost") 
                self.start_game()
     
                
    def rand_cell(self):
        return random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)
                
    def create_timer(self):
        self.timer_txt.set("0")
        while not self.solved:
            time.sleep(1)
            self.timer_txt.set(str(int(self.timer_txt.get()) + 1))   
              

    # --- main ---
    
    
def main():
    game = Game(dim=9)  
    game.loop()
    

if __name__ == "__main__":
    main()    
