import pygame
from .constants import (
    DARK_PINK,
    SQUARE_SIZE,
    CROWN,
)


class Piece:  # the intiailization and the idea to draw anything manually
    # is half inspired from Tech with Tim checkers although it has been
    # enhanced
    """
    the parent class for the checkers game pieces (pawns and kings).
    This handles positioning, movement, and visuals .

    Attributes:
        row (int): Current row position on board
        column (int): Current column position on board
        color (tuple): RGB color value of piece
        king (bool): Whether piece is a king
        points (int): Point value of piece (1 for pawn, 3 for king)
        x (int): X coordinate for drawing
        y (int): Y coordinate for drawing
        direction (int): Movement direction (-1 for pink, 1 for blue)
    """


    def __init__(
        self, row, column, color, points=1
    ):  # pawns are by default 1pt
        """
        Initializes a new piece with properties.

        Args:
            row (int): Starting row position
            column (int): Starting column position
            color (tuple): RGB color value
            points (int, optional): Point value of piece. Defaults to 1 for pawns
        """
        self.row = row
        self.column = column
        self.color = color
        self.king = False # to determine the king
        self.points = points  # to use sorting algorithms
        self.x = self.y = 0
        self.calc_pos() # finds the position on the window(x and y)
        if self.color == DARK_PINK:  # going up or down
            self.direction = -1
        else:
            self.direction = 1

    def draw_base(self, win):
        """
        Draws the base piece with shadow and highlight on it, these are 
        basically the pawns, this creates 3D appearance(at least trying).

        Args:
            win (pygame.Surface): Surface to draw on
        Raises:
            None
        Returns:
            None
        """


        radius = SQUARE_SIZE // 2 - 10

        # shadow: a soft transparent circle under the piece, slightly offset
        shadow_color = (0, 0, 0, 100)  # black with some transparency (0-255)
        shadow_surface = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            shadow_surface, shadow_color, (radius, radius), radius
        )
        shadow_pos = (
            self.x - radius,
            self.y - radius + 5,
        )  # slightly lower for shadow effect
        win.blit(shadow_surface, shadow_pos)

        # Draw the piece circle (main piece)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        # Draw a highlight circle for a subtle 3D effect (lighter color, smaller radius)
        highlight_color = (255, 255, 255, 80)  # white with transparency
        highlight_surface = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            highlight_surface, highlight_color, (radius, radius), radius // 2
        )
        highlight_pos = (self.x - radius, self.y - radius)
        win.blit(highlight_surface, highlight_pos)

    def draw(self, win):
        """
        draws the pawns

        Args:
            win (pygame.Surface): Surface to draw 
        Raises:
            None
        Returns:
            None
        """
        self.draw_base(win)

    
    def draw_small(self, win, x, y):
        """
        Draws smaller version of piece to captured pieces display.

        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X coordinate to draw at
            y (int): Y coordinate to draw at
        Raises:
            None
        Returns:
            None
        """


        radius = SQUARE_SIZE // 4

        # Draw white border behind piece (slightly bigger)
        border_radius = radius + 2
        pygame.draw.circle(win, (255, 255, 255), (x, y), border_radius)

        # Shadow (optional, for consistency)
        shadow_surface = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            shadow_surface, (0, 0, 0, 90), (radius, radius), radius
        )
        win.blit(shadow_surface, (x - radius, y - radius + 3))

        # Main piece
        pygame.draw.circle(win, self.color, (x, y), radius)

        # Highlight (light source reflection)
        highlight_surface = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            highlight_surface,
            (255, 255, 255, 80),
            (radius, radius),
            radius // 2,
        )
        win.blit(highlight_surface, (x - radius, y - radius))

    def move(self, row, column):
        """
        Updates the piece position and recalculates where to draw

        Args:
            row (int): New row 
            column (int): new column 
        Raises:
            None
        Returns:
            None
        """
        self.row = row
        self.column = column
        self.calc_pos()
    @property
    def position(self):  # this is something written for the user to let them
        # know where the piece is
        """
        Gets the poisition on the board
        Args:
            None
        Raises:
            None
        Returns:
            tuple:(row,column) 
        """
        return self.row, self.column

    def calc_pos(self):  # make sure the piece is in the middle of the
        # square it is supposed to be on
        """
        calculates the pixel position in order to draw piece and 
        updates the x and y attributes.
        """
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    # a veneer(yes I know my stuff)
    def become_king(self):
        """
        turns the piece into a king, just a veneer
        """
        self.king = True

    @property
    def is_king(self):
        """
        Mostly useful for debugging and testing, this gives us
        the option to see whether the piece is king or not

        Returns:
            Bool: True and False based on kingness of piece 
        """
        return True if self.king else False

    def __gt__(self, other):
        """
        Operator overloading based of the piece value. Greater than.

        Args:
            other (Piece): this is the other piece self being compared to. 
        Raises: 
            None
        Returns:
            bool: Whether self is greater than other or not 
        """
        return self.points > other.points

    def __lt__(self, other):
        """
        Operator overloading based of the piece value. Less than

        Args:
            other (Piece): this is the other piece self being compared to. 
        Raises: 
            None
        Returns:
            bool: Whether self is less than other or not 
        """
        return (self.points) < (other.points)

    # Mostly used for debugging:
    def __repr__(self):
        """
        String representation of piece showing color, type and position.
        Args:
            None
        Raises:
            None
        Returns:
            str: Piece description
        """
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
    """
    represents a king piece in checkers. Inherits from Piece class.
    kings can move diagonally in any direction and have higher point value(3).

    Attributes:
        Inherits all attributes from Piece class
        points (int): Set to 3 for kings
        king (bool): Always True for kings
    """
    def __init__(self, row, column, color):
        """
        generates a new king piece.

        Args:
            row (int): Starting row position
            column (int): Starting column position
            color (tuple): RGB color value
        """
        super().__init__(row, column, color, points=3)# each king has 3 pts
        self.become_king()

    # TODO: check whether we should draw the simple or complicated version
    # def draw(self, win):
    #     radius = SQUARE_SIZE // 2 - 10
    #     pygame.draw.circle(win, self.color, (self.x, self.y), radius)
    #     CROWN_RECT.center = (self.x, self.y)
    #     # Draw king marker
    #     pygame.draw.circle(win, "gold", (self.x, self.y), radius // 2 + 4)
    #     win.blit(CROWN, CROWN_RECT)
    #

    # METHOD OVERRIDING
    def draw(self, win):
        """
        Draws king piece with crown decoration.
        Overrides parent draw method to add tilted crown image.

        Args:
            win (pygame.Surface): Surface to draw on
        Raises:
            None
        Returns:
            None

        """
        self.draw_base(win)
        # _______THEEEEE CROWN_____
        radius = SQUARE_SIZE // 2 - 10
        crown_size = radius * 1.5
        crown_img_scaled = pygame.transform.smoothscale(
            CROWN, (int(crown_size), int(crown_size))
        )

        # Rotate the crown by about 30 degrees (tilt left)
        rotated_crown = pygame.transform.rotate(crown_img_scaled, 30)

        # Get the rect to help with positioning
        crown_rect = rotated_crown.get_rect()

        # Position it centered horizontally, but raised higher vertically (adjust y more negative)
        crown_pos = (
            self.x - crown_rect.width // 2 - 23,
            self.y - crown_rect.height // 2 - 32,
        )

        win.blit(rotated_crown, crown_pos)

    def draw_small(self, win, x, y):  # hey I'm using polymorphism
        """
        draws smaller version of king for captured pieces display.

        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X coordinate to draw at
            y (int): Y coordinate to draw at
        Raises:
            None
        Returns:
            None
        """

        # base piece draw
        super().draw_small(win, x, y) # inheriting the small pawn

        # Crown drawing
        radius = SQUARE_SIZE // 4
        crown_size = radius * 1.7
        crown_img = pygame.transform.smoothscale(
            CROWN, (int(crown_size), int(crown_size))
        )
        crown_img = pygame.transform.rotate(crown_img, 30)  # stylish angle

        crown_x = x - crown_size // 2 - 22
        crown_y = (
            y - crown_size // 2 - radius * 0.7
        ) - 10  # raised above piece center
        win.blit(crown_img, (crown_x, crown_y))


class Pawn(Piece):
    """
    Represents a pawn piece in checkers. Inherits from Piece class.
    Pawns move diagonally forward based on their color direction.

    Attributes:
        Inherits all attributes from Piece class
        points (int): Set to 1 for pawns
        king (bool): Always False initially for pawns
    """
    def __init__(self, row, column, color):
        """
        Creates a new pawn piece which has most of the 
        same attributes as Piece.

        Args:
            row (_type_): _description_
            column (_type_): _description_
            color (_type_): _description_
        """
        super().__init__(row, column, color, points=1) # the pts of 
        # each pawn is only 1 by default always
