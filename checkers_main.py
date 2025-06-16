"""
Author: Arsam Asefi
Date: June 11th, 2025
"""

import pygame
from checkers.timers import GameTimer
from checkers.constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    WIDTH,
    HEIGHT,
    FONT_NAME,
    BOARD_BORDER,
    FONT_SIZE,
)

from checkers.board import Board
import pygame
import sys
import os

from checkers.utils import get_mouse_square
from checkers.timers import PlayerTimer
from checkers.stats import stats

# Add the parent directory to sys.path to run everything smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Checkers Game")
FPS = 30
FONT = pygame.font.Font(FONT_NAME, FONT_SIZE)
OVERALL_TIMER_EVENT = pygame.event.custom_type()
OVERALL_TIME = pygame.time.set_timer(OVERALL_TIMER_EVENT, 1000)


def main():
    """
        This is the main function which runs all of the components of the game by 
        importing and getting different modules.
        Initializes the game board, timers, and handles all game events including
        mouse clicks for piece movement, keyboard controls for pause/reset, and 
        game state updates.
        Args:
            None

        Raises:
            pygame.error: For any Pygame-related errors during game execution
            SystemExit: When the game is closed

        Returns:
            None
        """
    game_timer = GameTimer()
    running = True
    clock = pygame.time.Clock() # builtin pygame timer helping us
    # to count by milliseconds, this is later used in timers.py
    board = Board(SCREEN)
    win_recorded = False  # a flag to check if the win is already recorded
    # this is to make sure we don't add to the wins every single frame

    while running:
        clock.tick(FPS)

        # UPDATE TIMERS FIRST (before events)
        if not board.paused:
            board.update_timers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(f"Click at: {pos}")

                # Check if click is within the board boundaries because the
                # user must not be able to click on the side panel
                if (
                    BOARD_WIDTH - BOARD_BORDER >= pos[0] > 0 + BOARD_BORDER
                    and BOARD_HEIGHT - BOARD_BORDER
                    >= pos[1]
                    > 0 + BOARD_BORDER
                ):

                    row, col = get_mouse_square(pos)
                    print(f"Board position: row {row}, col {col}")

                    # Handle the click through the board's click handler
                    board.handle_click(row, col)
         

            # add the win whenever someone wins to our database
            if board.status == "game_over" and not win_recorded:
                stats.add_win(board.winner)
                stats.save()  # Make sure to save the stats
                win_recorded = True
                print(f"{board.winner} win recorded!")

            
            if event.type == pygame.KEYDOWN:

                # Escape key for pause
                if event.key == pygame.K_p:  
                    board.toggle_pause()
                # Reset the wins scores by key L, only if in a menu
                if event.key == pygame.K_l and (
                    board.paused == True or board.status == "game_over"
                ):
                    stats.reset()

                # Rest with R key 
                if event.key == pygame.K_r:
                    board = Board(SCREEN)
                    game_timer = GameTimer()
                    win_recorded = False  # Reset flag for new game, making
                    # sure we will record the result for this one

                # going to main menu, only from a menu
                if (
                    event.key == pygame.K_ESCAPE
                    and board.paused
                    or event.key == pygame.K_ESCAPE
                    and board.status == "game_over"
                ):
                    running = False

        # Clear screen and draw everything
        SCREEN.fill((0, 0, 0))  # Black background put to be able to 
        # smoothly erased the last frame

        board.update_timers()  # this checks if any of the times is over

        # Draw the board and pieces
        board.draw_whole(SCREEN)

        # Draw the side panel with timer and game info
        board.draw_side_panel(SCREEN, FONT, game_timer)
        #  if the board is paused draw the menu for it 
        if board.paused:
            board.draw_pause_menu(SCREEN, FONT)

        # Update display
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
