import pygame
import os

# what is the parent directory? important to be able to access assets
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Themes
TEXT_COLOR = (255, 255, 255)  # White text

# Colors
BLACK = (100, 100, 100)
WHITE = (240, 240, 240)  # White squares
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (150, 220, 220)  # Cyan squares
BLUE = (0, 0, 139)  # Player 1 pieces
DARK_PINK = (231, 84, 128)  # Player 2 pieces
DARK_GREY = (169, 169, 169)
GOLD = (255, 215, 0)  # King pieces highlight (both sides)
SILVER = (192, 192, 192)  # Alternative crown color
COOL_GREY = (60, 74, 80)
SILVER_BLUE = (197, 216, 228)
NEON_BLUE = (0, 30, 255)


# Selection
SELECTED_OUTLINE = (255, 255, 0)  # Yellow outline for selected piece
VALID_MOVE = (200, 160, 255)  # purple dots or markers for valid moves

# FONT PATH
FONT_PATH = os.path.join(
    parent_dir, "fonts", "Orbitron", "static", "Orbitron-SemiBold.ttf"
)


# Text

TEXT_COLOR = WHITE
FONT_NAME = FONT_PATH
FONT_SIZE = 40
BOLD = False

# Screen
WIDTH = 1200
BOARD_WIDTH = WIDTH - 300
HEIGHT = 900
BOARD_HEIGHT = HEIGHT
BOARD_BORDER = 5
BOARD_BORDER_COLOR = COOL_GREY

# PANEL
PANEL_WIDTH = 200
PANEL_HEIGHT = 900
PANEL_COLOR = COOL_GREY
PANEL_OVERALL_TIMER_WIDTH = 238
PANEL_OVERALL_TIMER_HEIGHT = 130
PANEL_OVERALL_TIMER_X = (
    BOARD_WIDTH + ((WIDTH - BOARD_WIDTH) - PANEL_OVERALL_TIMER_WIDTH) // 2
)
PANEL_OVERALL_TIMER_Y = (HEIGHT - PANEL_OVERALL_TIMER_HEIGHT) // 2
PANEL_OVERALL_TIMER_TEXT_CENTRE = (
    PANEL_OVERALL_TIMER_X + PANEL_OVERALL_TIMER_WIDTH // 2,
    PANEL_OVERALL_TIMER_Y + PANEL_OVERALL_TIMER_HEIGHT // 2,
)
PANEL_OVERALL_TIMER_TEXT_TITLE_CENTRE = (
    PANEL_OVERALL_TIMER_X + PANEL_OVERALL_TIMER_WIDTH // 2,
    (PANEL_OVERALL_TIMER_Y + PANEL_OVERALL_TIMER_HEIGHT // 2) - 84,
)
# values taken from the rectangles(boxes)
PANEL_SCORE_UP_CENTRE = (910 + 90 // 2, 30 + 80 // 2)
PANEL_SCORE_DOWN_CENTRE = (910 + 90 // 2, 790 + 80 // 2)

PANEL_TIMER_UP_TEXT_CENTRE = (1010 + 180 // 2, 30 + 80 // 2)
PANEL_TIMER_DOWN_TEXT_CENTRE = (1010 + 180 // 2, 790 + 80 // 2)

# PANEL:RECTS
PANEL_RECT = pygame.Rect(899.9, 0, 900, 900)
PANEL_TIMER_UP = pygame.Rect(1010, 30, 180, 80)  # higher time rectangle
PANEL_TIMER_DOWN = pygame.Rect(1010, 790, 180, 80)  # low time rectangle
PANEL_SCORE_TIMER_DOWN = pygame.Rect(910, 30, 90, 80)  # top score rectangle
PANEL_SCORE_TIMER_UP = pygame.Rect(910, 790, 90, 80)
PANEL_OVERALL_TIMER_RECT = pygame.Rect(
    PANEL_OVERALL_TIMER_X,
    PANEL_OVERALL_TIMER_Y,
    PANEL_OVERALL_TIMER_WIDTH,
    PANEL_OVERALL_TIMER_HEIGHT,
)


PANEL_TIME_RADIUS = 16  # for rounded corners
PANEL_TIME_BG_COLOR = (197, 216, 228)
PANEL_TIME_BORDER_COLOR = (255, 255, 255)  # White
PANEL_TIME_TEXT_COLOR = (255, 255, 255)
PANEL_OVERALL_TIMER_COLOR = (40, 40, 50, 250)  # DARK GREY
PANEL_OVERALL_TIMER_TEXT_COLOR = (245, 222, 179)  # Warm Beige
# Board
COLUMNS = 8
ROWS = 8
SQUARE_SIZE = HEIGHT // ROWS
BOARD_RECT = pygame.Rect(0.5, 0, 899, 900)

# Images
# Get parent directory (culminating) path
crown_path = os.path.join(parent_dir, "imgs", "crown.png")

# Crown of the kings whenever a piece becomes a king
CROWN = pygame.image.load(crown_path)
CROWN = pygame.transform.scale(CROWN, (70, 65))
CROWN_RECT = CROWN.get_rect()
