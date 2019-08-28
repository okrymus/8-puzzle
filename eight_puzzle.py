# https://codereview.stackexchange.com/questions/76906/python-8-puzzle-and-solver
from itertools import chain
from math import sqrt
from random import choice


class Puzzle:
    """
    A class representing an '8-puzzle'.
    - 'init_state' should be a square list of lists with integer entries 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]].
    - 'goal_state' is fixed to be the board with 0 in the upper left corner, followed
       by integers in increasing order.
    """
    HOLE = 0

    def __init__(self, init_state, step_cost=None, test=False):
        # Use a flattened representation of the board (if it isn't already)
        self.init_state = list(chain.from_iterable(init_state)) if hasattr(init_state[0], '__iter__') else init_state
        self.init_hole = self.init_state.index(Puzzle.HOLE)
        self.width = int(sqrt(len(self.init_state)))
        self.goal_state = [Puzzle.HOLE] + list(range(1, self.width * self.width))
        self.test = test
        self.path_string = ''

    def is_goal(self, state):
        """
        Tests whether state is a goal state (i.e. the puzzle is solved).
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        first position on the board.
        """
        cond = state == self.goal_state
        if not cond and self.test:
            self.path_string += 'explored: \n'+self.board_str(state)+'\n'
        return cond
    
    def actions(self, state):
        """
        A generator for the possible moves for the hole, where the
        board is linearized in row-major order.  Possibilities are
        'U' (up), 'D' (down), 'L' (left), 'R' (right).
        """
        hole = state.index(Puzzle.HOLE)
        # Up, down
        for dest in (hole - self.width, hole + self.width):
            if 0 <= dest < len(self.init_state):
                if dest < hole:
                    yield 'U'
                else:
                    yield 'D'
        # Left, right
        for dest in (hole - 1, hole + 1):
            if dest // self.width == hole // self.width:
                if dest < hole:
                    yield 'L'
                else:
                    yield 'R'

    def transitions(self, state, action):
        """
        Returns the new state resulting from applying 'action' ('U','D','L','R')
        to 'state' (list of distinct integers representing board).
        """
        hole = state.index(Puzzle.HOLE)
        if action == 'U':
            new_hole = hole - self.width
        elif action == 'D':
            new_hole = hole + self.width
        elif action == 'L':
            new_hole = hole - 1
        elif action == 'R':
            new_hole = hole + 1
        else:
            raise Error()
        new_state = state[:]
        new_state[hole], new_state[new_hole] = state[new_hole], state[hole]
        if self.test:
            self.path_string += 'generated: \n'+self.board_str(new_state)+'\n'
        return new_state

    def step_cost(self, state, action):
        """
        Returns the cost associated with moving the hole: always 1.
        """
        return 1

    def shuffle(self, moves=1000):
        """
        Returns a new puzzle that has been shuffled with random moves.
        """ 
        def possible_moves(self):
            """
            A generator for the possible moves for the hole, where the
            board is linearized in row-major order.  Possibilities are
            -1 (left), +1 (right), -width (up), or +width (down).
            """
            # Up, down
            for dest in (self.init_hole - self.width, self.init_hole + self.width):
                if 0 <= dest < len(self.init_state):
                    yield dest
            # Left, right
            for dest in (self.init_hole - 1, self.init_hole + 1):
                if dest // self.width == self.init_hole // self.width:
                    yield dest
        def move(self, destination):
            """
            Move the hole to the specified index.
            """
            board = self.init_state[:]
            board[self.init_hole], board[destination] = board[destination], board[self.init_hole]
            return Puzzle(board)

        p = self
        for _ in range(moves):
            p = move(self,choice(list(possible_moves(self))))
        return p
    
    def getBoard(self):
        board = [[0 for i in range(3)] for i in range(3)]
        index = 0
        for row in range(3):
            for col in range(3):
                board[row][col] = self.init_state[index]
                index += 1

        return board

    def board_str(self, state):
        """
        Returns a string representation for the board state for easy printing.
        """
        return "\n".join(str(state[start : start + self.width])
                         for start in range(0, len(state), self.width))
