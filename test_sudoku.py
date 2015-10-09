import unittest
from numpy import matrix, vectorize
'''
Created on Oct 7, 2015

@author: templetonc
'''
from components import Board, Location, Solver

class BoardTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board(9)
        self.puzzle = '0 9 4 0 0 0 1 3 0; 0 0 0 0 0 0 0 0 0; 0 0 0 0 7 6 0 0 2; 0 8 0 0 1 0 0 0 0; 0 3 2 0 0 0 0 0 0; 0 0 0 2 0 0 0 6 0; 0 0 0 0 5 0 4 0 0; 0 0 0 0 0 8 0 0 7; 0 0 6 3 0 4 0 0 8' 
        self.board.set_puzzle(self.puzzle)
        
    def test_set_puzzle(self):
        self.board.set_puzzle(self.puzzle)
        assert self.board.puzzle == self.puzzle
        assert self.board.empty_locations == 60
    
    def test_set_matrix(self):
        self.board.set_matrix(self.puzzle)
    
    def test_get_number(self):
        test_location = Location(0,1)
        assert self.board.get_number(test_location) == 9
        
    def test_set_number(self):
        test_location = Location(0,4)
        assert self.board.empty_locations == 60, "self.board.empty_locations == %s" % self.board.empty_locations
        self.board.set_number(test_location, 5)
        assert self.board.m.item(test_location) == 5
        assert self.board.empty_locations == 59
        self.board.set_number(test_location, 4)
        assert self.board.empty_locations == 59
        test_location = Location(0,1)
        self.board.set_number(test_location, 0)
        assert self.board.empty_locations == 60
        self.board.set_number(test_location, 0)
        assert self.board.empty_locations == 60
      
    def test_get_row(self):
        test_location = Location(2,4)
        row = self.board.get_row(test_location)
        test_row = matrix([0,0,0,0,7,6,0,0,2])
        assert (row==test_row).all(), "row = %s, test_row = %s" % (row, test_row)
        
    def test_get_column(self):
        test_location = Location(2,4)
        column = self.board.get_column(test_location)
        test_column = matrix([[0], [0], [7], [1], [0], [0], [5], [0], [0]])
        assert (column==test_column).all(), "column = %s, test_column = %s" % (column, test_column)
        
    def test_get_sector(self):
        test_location = Location(2,4)
        sector = self.board.get_sector(test_location)
        assert sector.shape == (3,3), "sector.shape = %s" % sector.shape
        test_sector = matrix([[0, 0, 0],[0, 0, 0],[0, 7, 6]])
        assert (sector==test_sector).all(), "sector = %s, test_sector = %s" % (sector, test_sector)
        
    def test_is_in_row(self):
        test_location = Location(2,4)
        expected_results = [False, True, False, False, False, True, True, False, False]
        f = vectorize(self.board.is_in_row, excluded = [1])
        results = f(range(1, self.board.dimension + 1), test_location)
        assert len(results) == len(expected_results)
        assert (results == expected_results).all()
        #for x in range (self.board.dimension):
        #    assert self.board.is_in_row(x + 1, test_location) == expected_results[x]

    def test_is_in_column(self):
        test_location = Location(2,4)
        expected_results = [True, False, False, False, True, False, True, False, False]
        f = vectorize(self.board.is_in_column, excluded = [1])
        results = f(range(1, self.board.dimension + 1), test_location)
        assert len(results) == len(expected_results)
        assert (results == expected_results).all()
        
    def test_is_in_sector(self):
        test_location = Location(2,4)
        expected_results = [False, False, False, False, False, True, True, False, False]
        f = vectorize(self.board.is_in_sector, excluded = [1])
        results = f(range(1, self.board.dimension + 1), test_location)
        assert len(results) == len(expected_results)
        assert (results == expected_results).all()
        
        #for x in range(self.board.dimension):
        #    test = self.board.is_in_sector(x + 1, test_location) == expected_results[x]
        #    assert test, "x = %s, expected_results[%s] = %s, board.is_in_sector(%s, %s) = %s" % (x, x, expected_results[x], x, test_location, test )
        
    def test_is_legal(self):
        test_location = Location(2,4)
        expected_results = [False, False, True, True, False, False, False, True, True]
        for x in range(self.board.dimension):
            assert self.board.is_legal(x + 1, test_location) == expected_results[x]

class SolverTestCase(unittest.TestCase):
    def setUp(self):
        self.solver = Solver(9)
        self.puzzle = '0 9 4 0 0 0 1 3 0; 0 0 0 0 0 0 0 0 0; 0 0 0 0 7 6 0 0 2; 0 8 0 0 1 0 0 0 0; 0 3 2 0 0 0 0 0 0; 0 0 0 2 0 0 0 6 0; 0 0 0 0 5 0 4 0 0; 0 0 0 0 0 8 0 0 7; 0 0 6 3 0 4 0 0 8' 
        self.solver.board.set_puzzle(self.puzzle)
    
    def test_is_solution(self):# fix this test
        self.solver.board.empty_locations = 0
        assert self.solver.is_solution() == True
        self.solver.board.empty_locations = 1
        assert self.solver.is_solution() == False
        
    def test_local_count(self):
        test_location = (Location(2, 4))
        test_local_count = self.solver.local_count(test_location)
        assert test_local_count == 4, "local_count(%s) = %s" % (test_location, test_local_count)
        
    def test_next_location(self):
        next_location = self.solver.next_location()
        expected_location = Location(0, 3)
        assert expected_location == next_location

    def test_possible_numbers(self):
        test_location = Location(2,2)
        expected_possible_numbers = [1,3,5,8]
        possible_numbers = self.solver.possible_numbers(test_location)
        assert possible_numbers == expected_possible_numbers, "possible_numbers = %s" % possible_numbers
        
    def test_make_move(self):
        location = Location(2,2)
        number = 3
        self.solver.make_move(location, number)
        assert len(self.solver.moves) == 1
        assert self.solver.board.get_number(location) == number
        
    def test_solve(self):
        test_solution = matrix("7 9 4 5 8 2 1 3 6; 2 6 8 9 3 1 7 4 5; 3 1 5 4 7 6 9 8 2; 6 8 9 7 1 5 3 2 4; 4 3 2 8 6 9 5 7 1; 1 5 7 2 4 3 8 6 9; 8 2 1 6 5 7 4 9 3; 9 4 3 1 2 8 6 5 7; 5 7 6 3 9 4 2 1 8")
        self.solver.solve()
        (self.solver.solution == test_solution).all()
        
        
        
        
    
    

        
