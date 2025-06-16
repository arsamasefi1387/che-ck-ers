import unittest
from unittest import mock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkers.pieces import Pawn, King
from checkers.constants import BLUE, DARK_PINK


class TestPieces(unittest.TestCase):
    
    def test_01_pawn_initialization(self): # checks whether the pawns are correctly 
        # initialized or nto
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 1: Pawn initialization')
        # expected:
        pawn = Pawn(2, 3, BLUE)
        expected_row = 2 
        expected_col = 3
        expected_color = BLUE
        expected_king = False
        expected_points = 1
        # print the actual and expected
        print(f'Pawn row: {pawn.row}')
        print(f'Pawn column: {pawn.column}')
        print(f'Pawn color: {pawn.color}')
        print(f'Pawn is king: {pawn.king}')
        print(f'Pawn points: {pawn.points}')
        print(f'Expected: row={expected_row}, col={expected_col}, color={expected_color}')
        print(f'Expected: king={expected_king}, points={expected_points}')
        
        try: # checking if they actaually are equal
            self.assertEqual(pawn.row, expected_row)
            self.assertEqual(pawn.column, expected_col)
            self.assertEqual(pawn.color, expected_color)
            self.assertEqual(pawn.king, expected_king)
            self.assertEqual(pawn.points, expected_points)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

   # tests if the king is correctly initialized(and if it is a king actually!) 
    def test_02_king_initialization(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 2: King initialization')
        
        king = King(5, 7, DARK_PINK)
        expected_row = 5 # where is it supposed to be in rows
        expected_col = 7 # how about its column
        expected_color = DARK_PINK # and color
        expected_king = True # is it a king?
        expected_points = 3 # how much points does it have, important in sorting
       # print statements 
        print(f'King row: {king.row}')
        print(f'King column: {king.column}')
        print(f'King color: {king.color}')
        print(f'King is king: {king.king}')
        print(f'King points: {king.points}')
        print(f'Expected: row={expected_row}, col={expected_col}, color={expected_color}')
        print(f'Expected: king={expected_king}, points={expected_points}')
        try: # checking
            self.assertEqual(king.row, expected_row)
            self.assertEqual(king.column, expected_col)
            self.assertEqual(king.color, expected_color)
            self.assertEqual(king.king, expected_king)
            self.assertEqual(king.points, expected_points)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # checking if the blue pieces are in correct direction, REALLY ESSENTIAL because
    # this is in the main logic of the game and if it is ever lacking it will cause
    # a lot of problems for other logics of the game such as the score or the board 
    # itself
    def test_03_piece_direction_blue(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 3: Blue piece direction')
        
        blue_pawn = Pawn(5, 3, BLUE)
        direction = blue_pawn.direction
        expected_direction = 1 # the direction of blue pieces must be positive 
        # since they are going from down to up
        print(f'Blue pawn direction: {direction}')
        print(f'Expected direction: {expected_direction}')
        try:
            self.assertEqual(direction, expected_direction)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   # now for the pink pieces checkign their direction 
    def test_04_piece_direction_pink(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 4: Pink piece direction')
        
        pink_pawn = Pawn(2, 1, DARK_PINK)
        direction = pink_pawn.direction
        expected_direction = -1 # since they are at the top and are coming down the 
        # direction MUST BE negative which is towards buttom
        print(f'Pink pawn direction: {direction}')
        print(f'Expected direction: {expected_direction}')
        try:
            self.assertEqual(direction, expected_direction)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # OPERATOR OVERLOADING TESTING
    # this is one of the requirements and we need to check to see if it is accurately 
    # implemented or not since it is essential for sorting too
    def test_05_piece_comparison_greater_than(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 5: Piece comparison (greater than)')
        
        pawn = Pawn(0, 0, BLUE)
        king = King(7, 7, DARK_PINK)
        
        comparison_result = king > pawn # comparing them to one another
        pawn_points = pawn.points
        king_points = king.points
        
        print(f'Pawn points: {pawn_points}')
        print(f'King points: {king_points}')
        print(f'King > Pawn: {comparison_result}')
        print(f'Expected: True')
        
        try:
            self.assertTrue(comparison_result)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # testing for piece comparison less than overloading 
    def test_06_piece_comparison_less_than(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 6: Piece comparison (less than)')
        
        pawn = Pawn(0, 0, BLUE)
        king = King(7, 7, DARK_PINK)
        
        comparison_result = pawn < king
        pawn_points = pawn.points
        king_points = king.points
        
        print(f'Pawn points: {pawn_points}')
        print(f'King points: {king_points}')
        print(f'Pawn < King: {comparison_result}')
        print(f'Expected: True')
        
        try:
            self.assertTrue(comparison_result)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
     



if __name__ == '__main__':
    unittest.main()