import pygame
from .constants import DARK_PINK, SQUARE_SIZE, WHITE, CROWN_RECT, CROWN


class Piece:
    def __init__(
        self, row, column, color, points=1
    ):  # pawns are by default 1pt
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.points = points  # to use sorting algorithms
        self.x = self.y = 0
        self.get_position()
        if self.color == DARK_PINK:  # going up or down
            self.direction = -1
        else:
            self.direction = 1

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            CROWN_RECT.center = (self.x, self.y)
            # Draw king marker
            pygame.draw.circle(win, "gold", (self.x, self.y), radius // 2 + 4)

            win.blit(CROWN, CROWN_RECT)

    @property
    def position(self):  # this is something written for the user to let them
        # know where the piece is
        return self.row, self.column

    def get_position(self):  # make sure the piece is in the middle of the
        # square it is supposed to be on
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def become_king(self):
        self.king = True

    @property
    def is_king(self):
        True if self.king else False

    def __lt__(self, other):
        return (self.points) < (other.points)

    def __repr__(self):
        if self.king:
            return (
                f"{self.color} king, at row and column numbers"
                f"{self.position}"
            )
        else:
            return (
                f"{self.color} pawn, at row and column numbers"
                f"{self.position}"
            )


class King(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color, points=3)
        self.become_king()


class Pawn(Piece):
    def __init__(self, row, column, color):
        super().__init__(row, column, color, points=1)