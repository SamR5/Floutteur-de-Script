#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Same game from Simon Tatham's Portable Puzzle Collection

import random as r
import sys
if sys.version_info.major == 3:
    import tkinter as tk
else:
    import Tkinter as tk

M, N = 10, 10 # size rows*columns
colors = ["gray", "red", "green", "blue"]
cs = 40 # cell size
nei = [(-1, 0), (1, 0), (0, -1), (0, 1)] # neighbors of a cell

class SameGame():
    """"""
    def __init__(self, master, m=M, n=N):
        self.master = master
        self.m, self.n = m, n
        self.grid = [[r.randint(1, len(colors)-1) for j in range(self.n)]
                     for i in range(self.m)]
        self.gui()
        self.reset()

    def reset(self):
        self.grid = [[r.randint(1, len(colors)-1) for j in range(self.n)]
                     for i in range(self.m)]
        self.currM, self.currN = self.m, self.n # when row/col deleted
        self.selected = []
        self.selectedColor = 0
        self.score = 0
        self.update_display()
        self.update_status_bar()

    def gui(self):
        """"""
        self.canvas = tk.Canvas(self.master, width=self.n*cs,
                                height=self.m*cs)
        self.canvas.pack()
        # create the rectangles and center mark first for initialization
        # don't merge the for loops to keep the order of element in the canvas
        for i in range(self.m):
            for j in range(self.n):
                self.canvas.create_rectangle(j*cs, i*cs, (j+1)*cs, (i+1)*cs,
                                             fill=colors[self.grid[i][j]], width=1)
        for i in range(self.m):
            for j in range(self.n):
                self.canvas.create_rectangle((j+0.33)*cs, (i+0.33)*cs,
                                             (j+0.66)*cs, (i+0.66)*cs,
                                             fill="black")
        self.canvas.bind("<Button-1>", self.click_cell)
        self.canvas.bind_all("<KeyPress>", self.key_press)
        # status bar
        self.statusStr = tk.StringVar()
        self.scoreLab = tk.Label(self.master, textvariable=self.statusStr,
                                 anchor="w", relief="sunken")
        self.scoreLab.pack(side="bottom", fill='x')

    def update_status_bar(self):
        if len(self.selected):
            nxtScore = max(0, len(self.selected)-2)**2
            self.statusStr.set("Score: {}  Selected: {} ({})"\
                               .format(self.score, len(self.selected), nxtScore))
        else:
            self.statusStr.set("Score: {}".format(self.score))
        

    def update_display(self):
        for i in range(self.m):
            for j in range(self.n):
                self.canvas.itemconfig(i*self.n+j+1, fill=colors[self.grid[i][j]])
                if (i, j) in self.selected:
                    self.canvas.itemconfig(self.m*self.n+i*self.n+j+1, state="normal")
                else:
                    self.canvas.itemconfig(self.m*self.n+i*self.n+j+1, state="hidden")

    def click_cell(self, event=None):
        row, col = event.y//cs, event.x//cs
        if (row, col) in self.selected and len(self.selected) > 1:
            for i, j in self.selected:
                self.grid[i][j] = 0
            self.score += max(0, len(self.selected)-2)**2
            self.selected.clear()
        elif self.grid[row][col] != 0: # not gray
            self.selectedColor = self.grid[row][col]
            self.selected.clear()
            self.selected.append((row, col))
            self.get_area(row, col)
            if len(self.selected) == 1:
                self.selected.clear()
        self.update_grid_left()
        self.update_grid_down()
        self.update_display()
        self.update_status_bar()

    def key_press(self, event=None):
        if event.keysym in 'nN':
            self.reset()

    def get_area(self, row, col):
        """Update selected cells of the same color"""
        for i, j in nei:
            R, C = row+i, col+j
            # if on grid and not selected and same color
            if 0 <= R < self.m and 0 <= C < self.n and\
               (R, C) not in self.selected and\
               self.grid[R][C] == self.selectedColor:
                self.selected.append((R, C))
                self.get_area(R, C)

    def update_grid_left(self):
        """Push everything Left"""
        # push everything to the left
        for col in range(self.currN):
            allZero = True
            for i in range(self.currM):
                if self.grid[i][col] != 0:
                    allZero = False
                if not allZero:
                    break
            if allZero:
                for i in range(self.currM):
                    del self.grid[i][col]
                    self.grid[i].append(0)
                self.currN -= 1
                self.selected.clear()
                return self.update_grid_left()
    
    def update_grid_down(self):
        """Push everything down"""
        change = False
        for row in range(self.m-1, 0, -1):
            for j in range(self.currN):
                if self.grid[row][j] == 0 and self.grid[row-1][j] != 0:
                    self.grid[row][j] = self.grid[row-1][j]
                    self.grid[row-1][j] = 0
                    change = True
        if change:
            self.update_grid_down()
            self.selected.clear()

def main():
    """"""
    pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Same Game")
    root.resizable(False, False)
    myApp = SameGame(root)
    root.mainloop()
