import tkinter as tk
import random
import sys
import time
#import numpy as np
from square import Square
from itertools import product, starmap
from functools import partial
from tkinter import messagebox

userMode = input("Input a number...\n(8 for Beginner)\n(16 for Intermediate)\n(Or a custom number for a custom game)\n")
mode = int(userMode) 
#print(type(userMode))

class Application(tk.Frame):

  def __init__(self, master=None, height=64, width=64):
    super().__init__(master)
    self.master = master
    self.grid()
    self.create_widgets()

  def create_widgets(self):
    print("hello!")
    self.passed = 0
    self.clockStarted = 0
    if mode == 16:
        self.flagCount = 40 
        self.initialBombCount = 40
    elif mode == 8:
        self.flagCount = 10
        self.initialBombCount = 10
    else:
        self.flagCount = mode*2
        self.initialBombCount = mode*2
    self.squaresCleared = 0
    self.blankTile = tk.PhotoImage(file="blankTile.gif")
    self.blankTile = self.blankTile.subsample(27,27)
    self.smileyFace = tk.PhotoImage(file="smileyFace.gif")
    self.smileyFace = self.smileyFace.subsample(5,5)
    self.frownFace = tk.PhotoImage(file="frownFace.gif")
    self.frownFace = self.frownFace.subsample(7,7)
    self.winFace = tk.PhotoImage(file="winFace.gif")
    self.winFace = self.winFace.subsample(10,10)
    self.bombPic = tk.PhotoImage(file="bomb.gif")
    self.bombPic = self.bombPic.subsample(30,30) 
    self.redBombPic = tk.PhotoImage(file="redBomb.gif")
    self.redBombPic = self.redBombPic.subsample(16,16) 
    self.flagPic = tk.PhotoImage(file="flag.gif") 
    self.flagPic = self.flagPic.subsample(150,150) 
    self.quit = tk.Button(self, text="QUIT", fg="red",
			  command=self.master.destroy)
    self.quit.grid(row=int(mode+1), column=int(mode/4), columnspan=int(mode/2))
    self.resetter = tk.Button(self) 
    self.resetter["image"] = self.smileyFace
    self.resetter["command"] = self.reset
    self.resetter.grid(row=0,column=int(mode/4),columnspan=int(mode/2))
    self.clock = tk.Label("",font=("Courier",24))
    #self.clock = self.clock.zoom(3,3)
    self.clock.configure(text=self.passed)
    self.clock.grid(row=0,column=0,sticky='E'+'N')
    self.create_squares()
    self.flagNumber = tk.Label("",font=("Courier",24))
    self.flagNumber.configure(text=self.flagCount)
    self.flagNumber.grid(row=0,column=0,columnspan=2,sticky='W'+'N')

  def reset(self):
    children = self.winfo_children()
    for item in children:
        item.destroy()
    self.clock.destroy()
    self.flagNumber.destroy()
    self.clk = False
    self.clockStarted = 0
    self.create_widgets()

  def start_clock(self):
    self.clk = True
    self.clockStarted = 1
    self.update_clock()

  def stop_clock(self):
    self.clk = False

  def update_clock(self):
    if not self.clk:
        return
    self.passed += 1
    self.clock.configure(text=self.passed)
    self.after(1000,self.update_clock)

  def create_squares(self):
    self.create_bombs()
    self.create_numbers()
    self.create_buttons()

  def create_bombs(self):
    #bombSquares = np.zeros((mode,mode))
    bombSquares = [[0 for col in range(mode)] for row in range(mode)]
    bombValues = random.sample(range(mode*mode), self.initialBombCount)
    self.squares = [[Square(False,0,False) for j in range(mode)] for i in range(mode)]
    for x in range(mode):
        for y in range(mode):
            for z in range(self.flagCount):
                if x == int(bombValues[z]/mode):
                    if y == bombValues[z]%mode:
                        bombSquares[x][y] = 1
                        self.squares[x][y] = Square(True,0,False)

  def create_numbers(self):
    for i in range(0, mode):
        for j in range(0, mode):
            self.determine_number(i,j)

  def determine_number(self,i,j):
    num = 0
    cells = list(starmap(lambda a,b: (i+a, j+b), product((0,-1,+1), (0,-1,+1))))
    adjacents = cells[1:]  
    for x in adjacents:
        if x[0] >= 0 and x[1] >= 0:
            if x[0] < mode and x[1] < mode:
                if self.squares[x[0]][x[1]].bomb == True:
                    num += 1
    self.squares[i][j].number = num

  def create_buttons(self):
    self.gameButton =[[tk.Button(self) for j in range(mode)] for i in range(mode)]
    for i in range(0, mode):
        for j in range(0, mode):
            self.gameButton[i][j].grid(row = i+1, column = j)
            #self.gameButton[i][j]["text"] = "x"
            self.gameButton[i][j].configure(image=self.blankTile)
            self.gameButton[i][j].bind('<Button-1>', partial(self.change_text,i,j,0)) 
            self.gameButton[i][j].bind('<Button-2>', partial(self.set_flag,i,j))
  
  def set_flag(self, i, j, event):
    #if self.squares[i][j].flag == False:
    if self.gameButton[i][j]["image"] == str(self.blankTile):
        self.squares[i][j].flag = True
        #self.gameButton[i][j]["text"] = "F"
        #self.gameButton[i][j].config(fg='red')
        self.gameButton[i][j]["image"] = self.flagPic
        self.flagCount -= 1
        self.flagNumber.configure(text=self.flagCount)
    elif self.gameButton[i][j]["image"] == str(self.flagPic):
        self.squares[i][j].flag = False
        #self.gameButton[i][j]["text"] = "x"
        #self.gameButton[i][j].config(fg='black')
        self.gameButton[i][j]["image"] = self.blankTile
        self.flagCount += 1
        self.flagNumber.configure(text=self.flagCount)

  def change_text(self, i, j, recursed, *event):
    if self.clockStarted == 0:
        self.start_clock()
    if self.gameButton[i][j]["image"] == str(self.blankTile):
    #if self.gameButton[i][j]["text"] == "x":
        cells = list(starmap(lambda a,b: (i+a, j+b), product((0,-1,+1), (0,-1,+1))))
        adjacents = cells[1:]
        if self.squares[i][j].bomb == False:
            #self.gameButton[i][j]["image"] = self.bombPic
            self.gameButton[i][j]["image"] = ''
            self.gameButton[i][j]["text"] = self.squares[i][j].number
            self.gameButton[i][j].configure(fg="green")
            self.squaresCleared += 1
            if self.squaresCleared == (mode*mode - self.initialBombCount):
                self.resetter["image"] = self.winFace
                win = "Congragulations!! You won.\nYou're time was: %s seconds." % self.passed
                messagebox.showinfo("Game Over", win)
                self.stop_clock()
            if self.squares[i][j].number == 0:
                self.gameButton[i][j]["text"] = " "
                recursed += 1
                for x in adjacents:
                    if x[0] >= 0 and x[1] >= 0:
                        if x[0] < mode and x[1] < mode:
                            self.change_text(x[0],x[1],recursed)
        else:
            #self.gameButton[i][j]["text"] = "B"
            self.gameButton[i][j]["image"] = self.redBombPic
            self.show_bombs()
            self.resetter["image"] = self.frownFace
            messagebox.showinfo("Game Over", "Sorry, you hit a bomb")
            self.stop_clock()
    elif self.squares[i][j].flag == True:
        pass
    else:
        if recursed == 0:
            self.flag_click(i,j)

  def flag_click(self, i, j):
    cells = list(starmap(lambda a,b: (i+a, j+b), product((0,-1,+1), (0,-1,+1))))
    adjacents = cells[1:]
    adjacentFlags = 0
    for x in adjacents:
        if x[0] >= 0 and x[1] >= 0:
            if x[0] < mode and x[1] < mode:
                if self.squares[x[0]][x[1]].flag == True:
                    adjacentFlags += 1
    if adjacentFlags == self.squares[i][j].number:
        for x in adjacents:
            if x[0] >= 0 and x[1] >= 0:
                if x[0] < mode and x[1] < mode:
                    self.change_text(x[0],x[1],1)
    
  def show_bombs(self):
    for i in range(mode):
        for j in range(mode):
            if self.gameButton[i][j]["image"] == str(self.blankTile):
                if self.squares[i][j].bomb == True:
                    self.gameButton[i][j]["image"] = self.bombPic

root = tk.Tk()
dice = Application(master=root)
dice.mainloop()
