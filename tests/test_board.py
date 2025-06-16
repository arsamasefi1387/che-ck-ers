import unittest
from unittest import mock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checkers.board import Board
from checkers.pieces import Pawn, King
from checkers.constants import BLUE, DARK_PINK, ROWS, COLUMNS


class TestBoard(unittest.TestCase):
    
    def setUp(self): # this is a smart way to intialize the pygame, learned from 
        # python unittest documentation itself

        with mock.patch('pygame.display.set_mode'), \
             mock.patch('pygame.time.get_ticks', return_value=0):
            self.board = Board(None)  # Pass None for win since we're mocking
    # if the board is correctly initialized with pieces in starting positions.
    def test_01_make_board_initial_setup(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 1: Initial board setup')
        
        # Count pieces in starting positions
        blue_pieces = 0
        pink_pieces = 0
        empty_squares = 0
        
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board.board[row][col]
                if piece == 0:
                    empty_squares += 1
                elif piece.color == BLUE:
                    blue_pieces += 1
                elif piece.color == DARK_PINK:
                    pink_pieces += 1
        expected_blue = 12
        expected_pink = 12
        expected_empty = 40  # 64 - 24 pieces
        print(f'Blue pieces found: {blue_pieces}')
        print(f'Pink pieces found: {pink_pieces}')
        print(f'Empty squares: {empty_squares}')
        print(f'Expected: Blue={expected_blue}, Pink={expected_pink}, Empty={expected_empty}')
        
        try:
            self.assertEqual(blue_pieces, expected_blue)
            self.assertEqual(pink_pieces, expected_pink)
            self.assertEqual(empty_squares, expected_empty)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   #  getting a piece from a valid board position.
    def test_02_get_piece_valid_position(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 2: Get piece from valid position (0, 1)')
        piece = self.board.get_piece(0, 1)
        expected_color = DARK_PINK
        
        print(f'Piece at (0,1): {piece}')
        print(f'Piece color: {piece.color if piece != 0 else "None"}')
        print(f'Expected color: {expected_color}')
        
        try:
            self.assertNotEqual(piece, 0)
            self.assertEqual(piece.color, expected_color)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   #  testing getting a piece from an invalid board position.
    def test_03_get_piece_invalid_position(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 3: Get piece from invalid position (-1, 10)')
        piece = self.board.get_piece(-1, 10)
        expected_result = None
        print(f'Piece at (-1, 10): {piece}')
        print(f'Expected result: {expected_result}')
        
        try:
            self.assertEqual(piece, expected_result)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   #  Test getting all blue pieces from the board.
    def test_04_get_all_pieces_blue(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 4: Get all blue pieces')
        
        blue_pieces = self.board.get_all_pieces(BLUE)
        expected_count = 12
        
        print(f'Number of blue pieces found: {len(blue_pieces)}')
        print(f'Expected count: {expected_count}')
        
        try:
            self.assertEqual(len(blue_pieces), expected_count)
            # Verify all pieces are actually blue
            for piece in blue_pieces:
                self.assertEqual(piece.color, BLUE)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    #  Test getting all pink pieces from the board.
    def test_05_get_all_pieces_pink(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 5: Get all pink pieces')
        pink_pieces = self.board.get_all_pieces(DARK_PINK)
        expected_count = 12
        
        print(f'Number of pink pieces found: {len(pink_pieces)}')
        print(f'Expected count: {expected_count}')
        try:
            self.assertEqual(len(pink_pieces), expected_count)
            # Verify all pieces are actually pink
            for piece in pink_pieces:
                self.assertEqual(piece.color, DARK_PINK)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   #  Test selecting a piece when it's that player's turn.
    def test_06_select_piece_valid_turn(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 6: Select blue piece when it\'s blue\'s turn')
        
        # Blue starts first, so selecting blue piece should work
        result = self.board.select_piece(5, 0)  # Blue piece position
        
        print(f'Selection result: {result}')
        print(f'Selected piece: {self.board.selected}')
        print(f'Current turn: {self.board.turn}')
        print(f'Expected result: True')
        try:
            self.assertTrue(result)
            self.assertIsNotNone(self.board.selected)
            self.assertEqual(self.board.selected.color, BLUE)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    #  Test selecting a piece when it's not that player's turn.
    def test_07_select_piece_wrong_turn(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 7: Select pink piece when it\'s blue\'s turn')
        
        # Blue starts first, so selecting pink piece should fail
        result = self.board.select_piece(0, 1)  # Pink piece position
        
        print(f'Selection result: {result}')
        print(f'Selected piece: {self.board.selected}')
        print(f'Current turn: {self.board.turn}')
        print(f'Expected result: False')
        try:
            self.assertFalse(result)
            self.assertIsNone(self.board.selected)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # Test that turn changes correctly.
    def test_08_change_turn(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 8: Change turn from blue to pink')
        
        initial_turn = self.board.turn
        self.board.change_turn()
        new_turn = self.board.turn
        
        print(f'Initial turn: {initial_turn}')
        print(f'New turn: {new_turn}')
        print(f'Expected new turn: {DARK_PINK}')
        try:
            self.assertEqual(initial_turn, BLUE)
            self.assertEqual(new_turn, DARK_PINK)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   #  Test getting regular moves for a blue pawn.
    def test_09_get_regular_moves_blue_pawn(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 9: Get regular moves for blue pawn')
        
        # Get a blue pawn that can move
        piece = self.board.get_piece(5, 0)
        moves = self.board.get_regular_moves(piece)
        
        print(f'Piece at (5,0): {piece}')
        print(f'Available moves: {list(moves.keys())}')
        print(f'Number of moves: {len(moves)}')
        try:
            self.assertIsInstance(moves, dict)
            # Blue pawn should be able to move up-left to (4,1)
            self.assertIn((4, 1), moves)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   # tests if the regular moves are correct for pink pawns 
    def test_10_get_regular_moves_pink_pawn(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 10: Get regular moves for pink pawn')
        # Get a pink pawn that can move
        piece = self.board.get_piece(2, 1)
        moves = self.board.get_regular_moves(piece)
        print(f'Piece at (2,1): {piece}')
        print(f'Available moves: {list(moves.keys())}')
        print(f'Number of moves: {len(moves)}')
        try:
            self.assertIsInstance(moves, dict)
            # Pink pawn should be able to move down-left to (3,0) and down-right to (3,2)
            self.assertIn((3, 0), moves)
            self.assertIn((3, 2), moves)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
   # how many pieces do we have initially  
    def test_11_initial_piece_counts(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 11: Initial piece counts')
        
        expected_blue_pawns = 12
        expected_pink_pawns = 12
        expected_blue_kings = 0
        expected_pink_kings = 0
        print(f'Blue pawns: {self.board.cyan_pawns}')
        print(f'Pink pawns: {self.board.pink_pawns}')
        print(f'Blue kings: {self.board.cyan_kings}')
        print(f'Pink kings: {self.board.pink_kings}')
        print(f'Expected: Blue pawns={expected_blue_pawns}, Pink pawns={expected_pink_pawns}')
        print(f'Expected: Blue kings={expected_blue_kings}, Pink kings={expected_pink_kings}')
        try:
            self.assertEqual(self.board.cyan_pawns, expected_blue_pawns)
            self.assertEqual(self.board.pink_pawns, expected_pink_pawns)
            self.assertEqual(self.board.cyan_kings, expected_blue_kings)
            self.assertEqual(self.board.pink_kings, expected_pink_kings)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # pause  functionality
    def test_12_toggle_pause(self): 
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 12: Toggle pause functionality')
        
        initial_paused = self.board.paused
        self.board.toggle_pause()
        after_toggle = self.board.paused
        
        print(f'Initial paused state: {initial_paused}')
        print(f'After toggle: {after_toggle}')
        print(f'Expected after toggle: {not initial_paused}')
        
        try:
            self.assertEqual(initial_paused, False)
            self.assertEqual(after_toggle, True)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')


if __name__ == '__main__':
    unittest.main()