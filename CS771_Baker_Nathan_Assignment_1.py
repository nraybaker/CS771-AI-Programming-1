"""
Author: Nathan Baker
StudentID: A767P375
Class: CS 771 - Aritficial Intelligence

Programming Assignment #1

In this script we solve an 8-puzzle using the
A* algorithm with f = g + h where g is the number
of steps taken, and h is the heuristic function.
In this case the heuristic function is the 
manhattan distance.

This program will accept input for two grids,
the start state and the goal state. Each grid is
represented by the Puzzle class.

The solution is handled by the Solution class. It
is used to approximate the shortest solution path 
using the A* algorithm.
"""

import math

class Puzzle:
  """ This class forms a representation of the puzzle grid
  Methods:
    __init__: initializes the Puzzle from a given list
    print: print the grid
    search: search for value in grid and return tuple
    switch: switch two digits' places in grid
    get_lst: return a list of the grid elements
    adjacent: checks whether two digits adjacent
    get_adjacent: returns all adjacent digits to blank space
    manhattan_distance: returns manhattan distance between self and 
      another grid
    heuristic: returns sum of manhattan_distance's for all valid
      digits in grid
  Global Variables:
    digits: valid digits in grid
  Local Variables:
    lst: list representation of puzzle
    puzz: dictionary representation of puzzle
      coordinates are the keys, and the values are 
      elements in the grid at the coordinate 
  """
  digits = ['1', '2', '3', '4', '5', '6', '7', '8']
  
  def __init__(self, lst):
    """ Puzzle is structured as dictionary
    with keys being tuples that represent the value
    in that location. The values are the value in that
    location in the grid.
    """
    self.lst = lst
    self.puzz = {}
    k = 0
    for i in range(3):
      for j in range(3):
        self.puzz[(i, j)] = lst[k]
        k += 1
        
  def print(self):
    """ print the Puzzle
    """
    print(self.puzz[(0, 0)], ' ', self.puzz[(0, 1)], ' ', self.puzz[(0, 2)])
    print(self.puzz[(1, 0)], ' ', self.puzz[(1, 1)], ' ', self.puzz[(1, 2)])
    print(self.puzz[(2, 0)], ' ', self.puzz[(2, 1)], ' ', self.puzz[(2, 2)])
    
  def search(self, val):
    """ search for value among the Puzzle and return the tuple
    """
    for i in range(3):
      for j in range(3):
        if self.puzz[(i, j)] == val:
          return (i, j)
          
  def get_lst(self):
    """ returns a list of the Puzzle's elements to be used for
    the creation of successive Puzzles
    """
    return self.lst
    
  def switch(self, d1, d2):
    """ switch two values in the Puzzle
    """
    t1 = self.search(d1)
    t2 = self.search(d2)
    self.puzz[t1] = d2
    self.puzz[t2] = d1
    self.lst = list()
    for i in range(3):
      for j in range(3):
        self.lst.append(self.puzz[(i, j)])
    return self
    
  def adjacent(self, d1, d2):
    """ check if two digits are adjacent
    Two digits are adjacent if manhattan_distance is 1
    """
    t1 = self.search(d1)
    t2 = self.search(d2)
    s = 0
    for i in range(2):
      s += abs(t1[i] - t2[i])
    return s == 1
    
  def get_adjacent(self):
    """ get all digits adjacent to val
    """
    lst = list()
    for d in self.digits:
      if self.adjacent('_', d):
        lst.append(d)
    return lst
    
  def manhattan_distance(self, goal, val):
    """ gets manhattan_distance between the current
    Puzzle and a goal Puzzle
    """
    t1 = self.search(val)
    t2 = goal.search(val)
    s = 0
    for i in range(2):
      s += abs(t1[i] - t2[i])
    return s
    
  def heuristic(self, goal):
    """ calculates the heuristic for the Puzzle
    and a goal Puzzle. The heursitic in this case 
    is the manhattan distance.
    """
    s = 0
    for d in self.digits:
      s += self.manhattan_distance(goal, d)
    return s

class Solution:
  """ This class handles the solution of a Puzzle from
  start to goal.
  Local Variables:
    start: the initial Puzzle
    goal: the goal state of the Puzzle
    paths: dictionary stores the open paths left to check
      Key = a tuple representing the path
      Value = a tuple of (g, h) that is the number of steps
        for that path and the heuristic for the resulting
        puzzle of that path and the goal state
    solution_path: a tuple of the current min A* function path
      Upon solution completion will contain the solution path
  Methods:
    __init__: initializes the Solution with a given start
      and goal Puzzle
    solve: implementation of the A* algorithm to solve the
      Puzzle from start state to goal state
    print_solution: print the grids along the path of the solution
  """
  def __init__(self, start, goal):
    """ The Solution path contains two Puzzles, a 
    start Puzzle and a goal Puzzle. The paths are all the open
    paths to check. Closed paths are removed not stored. 
    """
    self.start = start
    self.goal = goal
    self.paths = {'_':(0, self.start.heuristic(self.goal))}
    self.solution_path = '_'
    
  def solvable(self):
    """ Checks the board for solvability using information from:
    "https://www.cs.princeton.edu/
      courses/archive/fall12/cos226/assignments/8puzzle.html"
    
    Possible boards are divided into two equivalence classes, those that are
    solvable, and those that aren't.
    
    The equivalence class the board belongs to is given by the number of 
      inversions. An inversion is given by a pair of elements where i < j, but
      j > i in goal grid when the grids are represented in row-major order.
      E.g. 1 2 3 4 5 6 7 8 for a goal grid. Grid is solvable if number of 
      inversions are even, and unsolvable if the number of inversions are odd.
    """
    start_lst = self.start.get_lst()
    goal_lst = self.goal.get_lst()
    start_lst = [x for x in self.start.get_lst() if x != '_']
    goal_lst = [x for x in self.goal.get_lst() if x != '_']
    
    inversions = 0
    for i in range(len(start_lst)):
      for j in range(len(start_lst)):
        if (i < j) and (goal_lst.index(start_lst[j]) < goal_lst.index(start_lst[i])):
          inversions += 1
    return inversions % 2 == 0
    
  def solve(self):
    """ Uses the A* algorithm to solve the Puzzle
    from start state to goal state.
    """
    solved = False
    while not solved:
      """ Create temporary puzzle and choose current
      solution path, then traverse the temporary puzzle 
      along that path.
      """
      temp = Puzzle(self.start.get_lst())
      path = self.solution_path
      val = self.paths[self.solution_path]
      for i in path:
        temp.switch('_', i)
        
      """ Get all possible moves and store
      the new path, the number of moves, and
      their heuristic value.
      """
      new_paths = temp.get_adjacent()
      check_paths = {}
      for i in range(len(new_paths)):
        temp2 = Puzzle(temp.get_lst())
        temp2.switch('_', new_paths[i])
        new_val = (val[0] + 1, temp2.heuristic(self.goal))
        lst = list()
        for j in path:
          lst.append(j)
        lst.append(new_paths[i])
        check_paths[tuple(lst)] = new_val
        
      """ Remove path if it repeats a previous move
      """
      for i in list(check_paths):
        if (i[-1] == i[-2]):
          check_paths.pop(i)
          
      """ Add new possible paths to the path list
      and get the current path with the minimum
      A* function value.
      """
      for i in list(check_paths):
        self.paths[i] = check_paths[i]
      self.paths.pop(path)
      self.solution_path = get_min(self.paths)
      
      """ If the solution path's heuristic value is 0
      the puzzle is solved.
      """
      if self.paths[self.solution_path][1] == 0:
        solved = True
  
  def print_solution(self):
    """ When the puzzle is solved this will print the
    grids from start state to goal state along the 
    solution path.
    """  
    path = self.solution_path
    temp = Puzzle(self.start.get_lst())
    j = 0
    for i in path:
      temp.switch('_', i)
      if j == 0:
        print('\nInitial State: ')
        temp.print()
      else:
        print('\nStep ', j, ' slide ', i, ':')
        temp.print()
      j += 1

def get_min(dic):
  """ Gets the path in the dictionary
  that contians the minimum A* function.
  """
  comp = math.inf
  for i in range(len(dic)):
      if sum(dic[list(dic)[i]]) < comp:
          comp = sum(dic[list(dic)[i]])
          curr_key = list(dic)[i]
  return curr_key

def accept(st):
  """ Accepts the puzzle from the user.
  Will ask if puzzle is correct and accept
  input again if not.
  """
  incorrect = True
  while incorrect:
    puz = list()
    print('\nEnter 9 numbers to be inserted into ', st, ' grid.',
      '\n_ Represents the blank space.\nInsert top to bottom, left to right: ')
    for i in range(9):
      thing = input('Insert: ')
      puz.append(thing)
    puz = Puzzle(puz)
    print('\nIs this correct?')
    puz.print()
    yn = input("(y/n)? ")
    if yn in ['y', 'Y']:
      incorrect = False
  return puz

def main():
  """ Gets input, creates Solution,
  solves, and prints the solution.
  """
  start = accept('START')
  goal = accept('END')
  
  S = Solution(start, goal)
  
  if S.solvable():
    S.solve()
    S.print_solution()
  else:
    print('\nWARNING! Start and Goal puzzle as input is unsolvable!')

if __name__ == '__main__':
  main()
