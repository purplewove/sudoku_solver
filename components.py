from numpy import matrix, concatenate 
from collections import namedtuple
from math import sqrt
from copy import deepcopy
'''
Created on Oct 7, 2015

@author: templetonc
'''

Location = namedtuple('Location', ['x', 'y'])

class Board():
    def __init__(self, dimension):
        assert sqrt(dimension) % 1 == 0
        self.dimension = dimension
        self.num_locations = dimension**2
        self.puzzle = None
        self.m = None
        self.locations = [Location(x,y) for x in range(self.dimension) for y in range(self.dimension)]
        self.number_range = range(1, dimension + 1)
        self.empty_locations = self.num_locations
        
    def set_puzzle(self, puzzle):
        self.puzzle = puzzle
        self.set_matrix(puzzle)
        self.empty_locations = puzzle.count("0")       
    
    #private
    def set_matrix(self, puzzle):
        self.m = matrix(self.puzzle)
        
    def set_number(self, location, number):
        assert isinstance(location, Location), "location parameter must be a valid Location instance"
        if self.get_number(location) == 0:
            if number != 0:
                self.empty_locations -= 1
        elif number == 0:
            self.empty_locations += 1
        self.m.itemset((location.x, location.y), number)
    
    def get_number(self, location):
        assert isinstance (location, Location), "location parameter must be a valid Location instance"
        return self.m.item(location.x, location.y)

    def is_legal(self, number, location):
        assert isinstance(number, int)
        assert isinstance(location, Location)
        assert number in self.number_range
        if not self.is_in_row(number, location) and not self.is_in_column(number, location) and not self.is_in_sector(number, location):
            return True
        else:
            return False
        
    def get_row(self, location):
        assert isinstance(location, Location)
        return self.m[location.x]
        
    def get_column(self, location):
        assert isinstance(location, Location)
        return self.m[:, location.y]
        
    def get_sector(self, location):
        assert isinstance(location, Location)
        assert sqrt(self.dimension) % 1 == 0
        self.sector_side_length = int(sqrt(self.dimension))
        assert isinstance(self.sector_side_length, int)
        xmin = location.x/self.sector_side_length * self.sector_side_length
        xbound = (location.x/self.sector_side_length + 1) * self.sector_side_length
        ymin = location.y/self.sector_side_length * self.sector_side_length
        ybound = (location.y/self.sector_side_length + 1) * self.sector_side_length
        assert (xmin + xbound + ymin + ybound) % self.sector_side_length == 0, "xmin = %s, xbound = %s, ymin = %s, ybound = %s" % (xmin, xbound, ymin, ybound)
        return self.m[xmin:xbound, ymin:ybound]
    
    def is_in_row(self, number, location):
        assert isinstance(number, int)
        assert isinstance(location, Location)
        if number in self.get_row(location):
            return True
        return False
        
    def is_in_column(self, number, location):
        assert isinstance(number, int)
        assert isinstance(location, Location), "%s" % location
        if number in self.get_column(location):
            return True
        return False
        
    def is_in_sector(self, number, location):
        assert isinstance(number, int)
        assert isinstance(location, Location)
        if number in self.get_sector(location):
            return True
        return False
    
    def print_board(self):
        #print ("this method should print the board")
        print (self.m)

class Solver():
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = Board(dimension)
        self.moves = []
        self.finished = False
        self.partial_iterations = 0
        self.iterations = 0
        self.solution = None
        
    def set_puzzle(self, puzzle):
        self.finished = False
        self.board.set_puzzle(puzzle)
    
    def solve(self):
        self.partial_iterations += 1
        if self.is_solution():
            self.process_solution()
        else:
            location = self.next_location()
            candidates = self.possible_numbers(location)
            for c in candidates:
                if self.finished == False:
                    self.make_move(location, c)
                    self.solve()
                    self.unmake_move()
        self.iterations += 1
        self.partial_iterations -= 1
    
    def next_location(self):
        best_open_location = None
        best_num_candidates = self.board.dimension
        for location in self.board.locations:
            if self.board.get_number(location) == 0:
                num_candidates = self.local_count(location)
                if num_candidates < best_num_candidates:
                    best_open_location = location
                    best_num_candidates = num_candidates
        return best_open_location
        
    def local_count(self, location):
        assert isinstance(location, Location)
        c = 0
        for number in self.board.number_range:
            if self.board.is_legal(number, location):
                c += 1
        return c
                
    def possible_numbers(self, location):
        assert isinstance(location, Location)
        c = []
        for number in self.board.number_range:
            if self.board.is_legal(number, location):
                c.append(number)
        return c
    
    def make_move(self, location, c):
        assert len(self.moves) < self.board.num_locations
        self.moves.append(location)
        self.board.set_number(location, c)
        
    def unmake_move(self):
        assert len(self.moves) > 0
        location = self.moves.pop()
        self.board.set_number(location, 0)
        
    def is_solution(self):
        if self.board.empty_locations == 0:
            return True
        else:
            return False
    
    def process_solution(self):
        self.solution = deepcopy(self.board)
        self.finished = True
        
    def print_board(self):
        if self.iterations == 0:
            print "Puzzle:"
        else: 
            print "Board after %d iterations and %d partial iterations: " % (self.iterations, self.partial_iterations)
        self.board.print_board()
       
    
    def print_solution(self):
        print ("Solution: ")
        self.solution.print_board()
        
    
        
if __name__ == "__main__":
    solver = Solver(9)
    solver.set_puzzle('0 9 4 0 0 0 1 3 0; 0 0 0 0 0 0 0 0 0; 0 0 0 0 7 6 0 0 2; 0 8 0 0 1 0 0 0 0; 0 3 2 0 0 0 0 0 0; 0 0 0 2 0 0 0 6 0; 0 0 0 0 5 0 4 0 0; 0 0 0 0 0 8 0 0 7; 0 0 6 3 0 4 0 0 8')
    solver.print_board()
    solver.solve()    
    solver.print_solution()   
        
        
        
        
        