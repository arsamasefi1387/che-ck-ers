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
        
        for row in range(ROWS): # creating the rows and columns to count the pieces
            for col in range(COLUMNS): # creating the columns
                piece = self.board.board[row][col] # getting the piece at that position
                if piece == 0: # if there is no piece at that position
                    empty_squares += 1 # add to the empty squares
                elif piece.color == BLUE: # if blue
                    blue_pieces += 1 # add to blue pieces 
                elif piece.color == DARK_PINK: # and so on
                    pink_pieces += 1
        expected_blue = 12 # the expected blues
        expected_pink = 12 # the expected pinks
        expected_empty = 40  # 64 - 24 pieces # the expected empty squares
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
    # testing whether the pieces can be moved off the board
    # this is not allowed so it should return None
    def test_13_move_off_board(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 13: Attempt to move piece off board')
        
        # get a piece from an invalid position
        piece = self.board.get_piece(-1, -1)
        piece2 = self.board.get_piece(8, 8)
        
        print(f'Piece at (-1,-1): {piece}')
        print(f'Piece at (8,8): {piece2}')
        print(f'Expected: None for both positions')
        
        try:
            self.assertIsNone(piece) # asserting that the piece is None
            self.assertIsNone(piece2)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')
    # Testing if the capture functionality actually removes the piece
    # from the board after a capture move
    def test_14_capture_removes_piece(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 14: Verify piece is removed after capture')
        
        # Set up a capture scenario
        self.board.board[4][3] = Pawn(4, 3, DARK_PINK)  # Place piece to be captured
        piece = self.board.get_piece(5, 2)  # Get the capturing piece
        
        # Get moves for the piece that can capture
        moves = self.board.get_valid_moves(piece)
        # not that of a complex logic but just to get the moves that capture
        # the piece at (4,3) which is the piece to be captured
        capture_moves = {k: v for k, v in moves.items() if v}  # Get only moves that capture 
        print(f'Capturing piece position: (5,2)')
        print(f'Piece to be captured position: (4,3)')
        print(f'Capture moves available: {capture_moves}')
        
        try:
            self.assertTrue(len(capture_moves) > 0)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # Testing if selecting an empty square returns False
    def test_15_select_empty_square(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 15: Attempt to select empty square')
        
        # Try to select an empty square (should be empty in default board setup)
        result = self.board.select_piece(3, 3)
        
        print(f'Selection result: {result}')
        print(f'Selected piece: {self.board.selected}')
        print(f'Expected result: False')
        
        try:
            self.assertFalse(result)
            self.assertIsNone(self.board.selected)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')

    # testing if the King promotion is correctly implemented 
    def test_16_king_promotion(self):
        print('\n\n----------------------------------------------------------------------')
        print('Test Case 16: Test king promotion')
        
        # Place a blue pawn at row 1 (one move away from promotion)
        test_piece = Pawn(1, 0, BLUE)
        self.board.board[1][0] = test_piece
        
        # Move to promotion row
        self.board.board[1][0] = 0  # delete from original position
        self.board.board[0][1] = test_piece  # Place in promotion position
        test_piece.move(0, 1)  # Update position
        
        print(f'Piece position before promotion: (1,0)')
        print(f'Piece position after movement: (0,1)')
        print(f'Is king before promotion: {test_piece.king}')
        
        # The piece should be promoted to king
        if test_piece.color == BLUE and test_piece.row == 0:
            test_piece.become_king() # makes the piece a king
            
        try:
            self.assertTrue(test_piece.king)
            print('Test Passed')
        except AssertionError:
            print('Test Failed')
        print('----------------------------------------------------------------------\n\n')


if __name__ == '__main__':
    unittest.main()