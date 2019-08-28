#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import numpy as np
import AI
import time
import random

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QRect,QAbstractAnimation, QSequentialAnimationGroup
from eight_puzzle import Puzzle
from dialog import Ui_Dialog

FRAME_SIZE = 240
TILE_SIZE = FRAME_SIZE/3
X = 0
Y = 1

class Tile:
    def __init__(self, label, value, pos):
        # QLabel
        self.label = label
        # QLabbel's text
        self.value = value
        # position (x, y)
        self.pos = pos
        
class MyApp(QMainWindow):
    def __init__(self, board=None, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.Tiles = []
        self.hole = ()
   
        if board is None:
            board = [[0,1,2],
                     [3,4,5],
                     [6,7,8]]
        
        self.board = board
        self.setBoardGUI(board)
        self.puzzle = Puzzle(self.board)

        # handle events
        self.ui.pushButton.clicked.connect(self.solve_GUI)
        self.ui.pushButton_2.clicked.connect(self.shuffle)
        self.ui.label_1.mousePressEvent = self.move_label_1
        self.ui.label_2.mousePressEvent = self.move_label_2
        self.ui.label_3.mousePressEvent = self.move_label_3
        self.ui.label_4.mousePressEvent = self.move_label_4
        self.ui.label_5.mousePressEvent = self.move_label_5
        self.ui.label_6.mousePressEvent = self.move_label_6
        self.ui.label_7.mousePressEvent = self.move_label_7
        self.ui.label_8.mousePressEvent = self.move_label_8


    def action(self, tile):
        """
        return possible move (action) for the tile
        """
        if tile.pos[X] == self.hole[X]:
            if tile.pos[Y] == self.hole[Y]-1:
                return 'U'
            elif tile.pos[Y] == self.hole[Y]+1:
                return 'D'
        if tile.pos[Y] == self.hole[Y]:
            if tile.pos[X] == self.hole[X]+1:
                return 'R'
            elif tile.pos[X] == self.hole[X]-1:
                return 'L'
        return None
    
    def shuffle(self):
        # random move 10 times
        for _ in range(10):
            self.puzzle = Puzzle(self.board).shuffle()
            self.board = self.puzzle.getBoard()
            self.setBoardGUI(self.board)
        
    def move_helper(self,tile):
        act = self.action(tile)
        
        if act == 'U':
            moveTile = (self.hole[0], self.hole[1]-1)
        elif act == 'D':
            moveTile = (self.hole[0], self.hole[1]+1)
        elif act == 'L':
            moveTile = (self.hole[0]-1, self.hole[1]) 
        elif act == 'R':
            moveTile = (self.hole[0]+1, self.hole[1])
        else:
            print("cannot move") 
        
        if act is not None:
            tile.pos = self.hole
            self.anim = self.doMove(tile,moveTile)
            self.hole = moveTile
            self.anim.start()
            self.puzzle = Puzzle(self.get_board())
            self.board = self.puzzle.getBoard()

    def move_label_1(self,event):
        tile = self.Tiles[0]
        self.move_helper(tile)
    
    def move_label_2(self,event):
        tile = self.Tiles[1]
        self.move_helper(tile)
        
    def move_label_3(self,event):
        tile = self.Tiles[2]
        self.move_helper(tile)
    
    def move_label_4(self,event):
        tile = self.Tiles[3]
        self.move_helper(tile)
    
    def move_label_5(self,event):
        tile = self.Tiles[4]
        self.move_helper(tile)
    
    def move_label_6(self,event):
        tile = self.Tiles[5]
        self.move_helper(tile)
        
    def move_label_7(self,event):
        tile = self.Tiles[6]
        self.move_helper(tile)
    
    def move_label_8(self,event):
        tile = self.Tiles[7]
        self.move_helper(tile)

    """
    fills tiles on the board from a board's string
    """
    def setBoardGUI(self, board):
        num = 1
        self.Tiles = []
        
        for row in range(3):
            for col in range(3):
                value = self.board[row][col]
                if value is 0:
                    self.hole = (col, row)
                else:
                    label = getattr(self.ui, 'label_{}'.format(num))
                    label.setText(str(value))
                    tile = Tile(label,value, (col, row))
                    tile.label.setGeometry(QRect(tile.pos[0]*TILE_SIZE, tile.pos[1]*TILE_SIZE, 80, 80))
                    self.Tiles.append(tile)
                    num += 1
        
    
    def get_board(self):
        """
        return list of a board
        """
        board = [[0 for i in range(3)] for i in range(3)]
        for tile in self.Tiles:
            board[tile.pos[Y]][tile.pos[X]] = tile.value
            
        return board
            
    
    def solve_GUI(self):
        """
        animation for solving the puzzle
        """
        def findTile(moveTile):
            for tile in self.Tiles:
                if tile.pos == moveTile:
                    return tile

        solver = AI.Astar(self.puzzle)
        solution = solver.solve()
        actions, states, num_explored, num_generated = solution
        self.group = QSequentialAnimationGroup()
  
        for action in actions:
#             print(action)

            if action == 'U':
                moveTile = (self.hole[0], self.hole[1]-1)
            elif action == 'D':
                moveTile = (self.hole[0], self.hole[1]+1)
            elif action == 'L':
                moveTile = (self.hole[0]-1, self.hole[1]) 
            elif action == 'R':
                moveTile = (self.hole[0]+1, self.hole[1])
            else:
                raise Error()
            
            tile = findTile(moveTile)
            tile.pos = self.hole
            anim = self.doMove(tile,moveTile)
            self.group.addAnimation(anim);
            self.hole = moveTile

        self.group.start();   
        self.puzzle = Puzzle(self.get_board())
   

    def doMove(self, tile, moveTile):
        """
        action move a tile to position (moveTile) 
        """
        label = tile.label
        
        anim = QPropertyAnimation(label, b"geometry")
        anim.setDuration(500)
        anim.setStartValue(QRect(moveTile[0]*TILE_SIZE, moveTile[1]*TILE_SIZE,  label.width(), label.height()))
        anim.setEndValue(QRect(tile.pos[0]*TILE_SIZE, tile.pos[1]*TILE_SIZE,  label.width(), label.height()))
        
        return anim
        
def random_puzzle():
    init_state = random.sample(range(9), 9)
    board = [[0 for i in range(3)] for i in range(3)]
    index = 0
    for row in range(3):
        for col in range(3):
            board[row][col] = init_state[index]
            index += 1

    return board
if __name__ == '__main__':
    app = QApplication(sys.argv)
#     board = [[3,0,2],
#              [4,1,5],
#              [6,7,8]]
#     Harder puzzle test
#     board = [[7,2,4],
#              [0,5,6],
#              [8,3,1]]
    board = random_puzzle()
    myapp = MyApp(board)
    myapp.show()
    sys.exit(app.exec_())
    
 





