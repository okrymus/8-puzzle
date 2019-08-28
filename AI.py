from eight_puzzle import Puzzle
from math import sqrt


################################################################
### Node class and helper functions
################################################################
class Node:
    """
    A class representing a node.
    - 'state' holds the state of the node.
    - 'parent' points to the node's parent.
    - 'action' is the action taken by the parent to produce this node.
    - 'path_cost' is the cost of the path from the root to this node.
    """

    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def gen_child(self, problem, action):
        """
        Returns the child node resulting from applying 'action' to this node.
        """
        return Node(state=problem.transitions(self.state, action),
                    parent=self,
                    action=action,
                    path_cost=self.path_cost + problem.step_cost(self.state, action))

    @property
    def state_hashed(self):
        """
        Produces a hashed representation of the node's state for easy
        lookup in a python 'set'.
        """
        return hash(str(self.state))

def retrieve_solution(node,num_explored,num_generated):
    """
    Returns the list of actions and the list of states on the
    path to the given goal_state node. Also returns the number
    of nodes explored and generated.
    """
    actions = []
    states = []
    while node.parent is not None:
        actions += [node.action]
        states += [node.state]
        node = node.parent
    states += [node.state]
    return actions[::-1], states[::-1], num_explored, num_generated

def print_solution(solution):
    """
    Prints out the path from the initial state to the goal given
    a tuple of (actions,states) corresponding to the solution.
    """
    actions, states, num_explored, num_generated = solution
    print('Start')
    for step in range(len(actions)):
        print(puzzle.board_str(states[step]))
        print()
        print(actions[step])
        print()
    print('Goal')
    print(puzzle.board_str(states[-1]))
    print()
    print('Number of steps: {:d}'.format(len(actions)))
    print('Nodes explored: {:d}'.format(num_explored))
    print('Nodes generated: {:d}'.format(num_generated))

################################################################
### Skeleton code for your Astar implementation
################################################################
class Astar:
    """
    A* search.
    - 'problem' is a Puzzle instance.
    """
    def __init__(self, problem):
        self.problem = problem
        self.init_state = problem.init_state
        self.num_explored = 0
        self.num_generated = 1

    def solve(self, method='man'):
        """
        Perform A* search and return a solution using `retrieve_solution'
        (if a solution exists).
        pass method to the heuristic function h 
        """

        node = Node(state=self.init_state,
                    parent=None,
                    action=None,
                    path_cost=0)
        num_explored = int(0)
        num_generated = int(0)
        puzzle = self.problem
        
        ################################################################
        ### Solve algorithm
        # ###############################################################
        openl = [node]
        closel = []

        while len(openl) > 0:
            node = min(openl,key=lambda p: self.f(p,method))
            num_explored+=1
            if (puzzle.is_goal(node.state)):
                return retrieve_solution(node, num_explored=num_explored, num_generated=num_generated)

            openl.remove(node)
            closel.append(node.state_hashed)

            moves = puzzle.actions(node.state)
            for action in moves:
                succ = node.gen_child(puzzle,action)
                if succ.state_hashed in closel:
                    continue

                if succ not in openl:
                    num_generated+=1
                    openl.append(succ)
        raise ValueError('No Path Found')

    def f(self,node, method):
        '''
        Returns a lower bound estimate on the cost from root through node
        to the goal.
        '''
        return node.path_cost + self.h(node, method)

    def h(self,node, method='man'):
        '''
        Returns a lower bound estimate on the cost from node to the goal
        using the different heuristics. 
        '''

        def getx(value):
            return value//3

        def gety(value):
            return value%3

        if method == 'man':
            sum = 0
            counter = 0
            for value in node.state:
                if value != 0:
                    sum += abs(getx(counter)-getx(value)) + abs(gety(counter)-gety(value))
                    counter = counter+1
                else: counter = counter+1
            return sum # compute manhattan distance
        elif method == 'rowcol':
            sum = 0
            counter = 0
            for value in node.state:
                if value != 0:
                    if getx(counter) != getx(value):
                        sum += 1
                    if gety(counter) != gety(value):
                        sum += 1
                counter += 1
            return sum # compute rowcol heuristic
        elif method == 'misplaced':
            msp = 0
            counter = 0
            for value in node.state:
                if value != 0:
                    if (getx(value) != getx(counter) or gety(value) != gety(counter)):
                        msp = msp+1
                    counter = counter + 1
                else:
                    counter = counter + 1
            return msp  # compute misplaced tiles the number of tiles out of place
        elif method == 'null':
            return 0 # compute null heuristic
        else:
            return 0

    def method_stats(self, board, trials=100, method='man'):
        '''
        Returns an mean and standard deviation of the number of nodes expanded
        '''
        # randomly generate puzzles and
        # compute the mean and standard deviation of the number
        # nodes expanded. You can use np.mean() and np.std()

        expanded_mean = 0.
        expanded_std = 0.
        arr = []
        for t in range(trials):
            puzzle = Puzzle(board).shuffle()
            solver = Astar(puzzle)
            # actions, states, num_explored, num_generated = solver.solve(method=method)
            for r in range(40):
                puzzle = Puzzle(board).shuffle()

            solution = solver.solve(method=method)
            actions, states, num_explored, num_generated = solution
            arr.append(num_generated)
            ############################################################
            ### Compute upper bound for branching factor and update b_hi
            ############################################################


        expanded_mean = mean(arr)
        expanded_std = std(arr)
        return expanded_mean, expanded_std

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    """returns the standard deviation of lst"""
    mn = mean(lst)
    variance = sum([(e-mn)**2 for e in lst]) / len(lst)
    return sqrt(variance)

if __name__ == '__main__':
    # Simple puzzle test

    board = [[3,1,2],
             [4,0,5],
             [6,7,8]]

    puzzle = Puzzle(board)
    solver = Astar(puzzle)
    solution = solver.solve()
    print_solution(solution)

    # Harder puzzle test
    board = [[7,2,4],
             [5,0,6],
             [8,3,1]]

    puzzle = Puzzle(board)
    solver = Astar(puzzle)
    solution = solver.solve()
    print(len(solution[0]))

    board = [[5, 1, 4],
             [2, 0, 3],
             [6, 7, 8]]

    # branching factor test
    method='man'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))

    # branching factor test
    method = 'rowcol'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))

    # branching factor test
    method='misplaced'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))

# branching factor test
    method='null'
    emean, estd = solver.method_stats(board, trials=5, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))
