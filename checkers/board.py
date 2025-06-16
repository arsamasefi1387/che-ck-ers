import pygame
from .constants import (
    COLUMNS,
    COOL_GREY,
    NEON_BLUE,
    ROWS,
    CYAN,
    GOLD,
    SQUARE_SIZE,
    WHITE,
    WIDTH,
    HEIGHT,
    BLUE,
    BOARD_BORDER_COLOR,
    BOARD_RECT,
    BOARD_BORDER,
    PANEL_COLOR,
    PANEL_RECT,
    PANEL_TIME_BG_COLOR,
    PANEL_TIMER_UP,
    PANEL_TIMER_DOWN,
    PANEL_TIME_RADIUS,
    PANEL_SCORE_TIMER_UP,
    PANEL_SCORE_TIMER_DOWN,
    PANEL_OVERALL_TIMER_COLOR,
    PANEL_OVERALL_TIMER_TEXT_COLOR,
    PANEL_OVERALL_TIMER_RECT,
    PANEL_OVERALL_TIMER_TEXT_CENTRE,
    PANEL_OVERALL_TIMER_TEXT_TITLE_CENTRE,
    SELECTED_OUTLINE,
    VALID_MOVE,
    PANEL_TIMER_UP_TEXT_CENTRE,
    PANEL_TIMER_DOWN_TEXT_CENTRE,
    PANEL_SCORE_DOWN_CENTRE,
    PANEL_SCORE_UP_CENTRE,
)
from .timers import GameTimer, PlayerTimer
from .pieces import DARK_PINK, Pawn, King
from .utils import mergeSort
from .stats import stats


# NOTE: dc is direction of column(going up or down) and dr is left or right
class Board:
    """
    Checkers game board with game logic, piece management, and 
    display the scores,time,etc.
    
    The board manages the game logic including piece positions, captured 
    pieces,turn management, timers, and win conditions. It handles all 
    game logic including valid moves, piece captures, and king promotions.

    Attributes:
        SCREEN (pygame.Surface): The game display surface
        status (str): Current game status ("playing" or "game_over")
        board (list): 2D list representing the game board
        captured (list): List of captured pieces
        pink_pawns (int): Count of pink pawns
        cyan_pawns (int): Count of blue pawns
        selected (Piece): Currently selected piece
        pink_kings (int): Count of pink kings
        cyan_kings (int): Count of blue kings
        turn (tuple): Current player's turn (BLUE or DARK_PINK)
        valid_moves (dict): Dictionary of valid moves for selected piece
        winner (str): Winner of the game (None if game ongoing)
        paused (bool): Game pause status
        blue_timer (PlayerTimer): Timer for blue player
        pink_timer (PlayerTimer): Timer for pink player
        
    Raises:
        pygame.error: If game display fails or any unexpected errors

    """
    def __init__(self, win):
        """
        Initializes a new game board with starting piece positions
        and starts the main logic of the game.

        Args:
            win (pygame.Surface): The game window to draw on.

        Raises:
            None

        Returns:
            None
        """
        self.SCREEN = win
        self.status = "playing"
        self.board = []
        self.captured = []
        self.pink_pawns = self.cyan_pawns = 12
        self.selected = None
        self.pink_kings = self.cyan_kings = 0
        self.turn = BLUE  # Blue starts first
        self.valid_moves = {}
        self.winner = None
        self.make_board()
        self.paused = False  # pause functionality
        self.blue_timer = PlayerTimer()  # initialize the blue timer
        self.pink_timer = PlayerTimer()  # initialize the pink timer
        self.last_update = pygame.time.get_ticks()  # update the timer
        self.blue_timer.is_active = True  #  blue starts first

    def make_board(self):
        """
        Creates the initial board setup with pieces in starting positions.
        Places 12 pieces for each player in alternating squares on first 3 rows.
        Note that this is not the visual, but is the 2D table representation 
        and only representation of pieces to help with smooth logic.

        Args:
            None
        Raises:
            None

        Returns:
            list: 2D list representing board with pieces
        """

        for row in range(ROWS):
            self.board.append([])
            for columns in range(COLUMNS):
                if (columns % 2 == 0 and row % 2 == 1) or (
                    columns % 2 == 1 and row % 2 == 0
                ):  # this is to be able to create the famous
                    # checkers and chess structure using row numbers
                    # and columns, if one even and the other odd, we
                    # draw the squares, otherwise, just 0 to represent
                    # the empty squares(all created in the 2D list)

                    if row < 3:  # if top of the board
                        self.board[row].append(Pawn(row, columns, DARK_PINK))
                    elif row > 4:  # bottom of the board
                        self.board[row].append(Pawn(row, columns, BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def toggle_pause(self):
        """
        pauses the game and switches the mode between paused and unpaused.
        This eventually Affects timer counting and piece movement since 
        all of them must be frozen except overall timer.

        Args:
            None
        Raises:
            None        
        Returns:
            bool: New pause state
        """
        self.paused = not self.paused
        # Stop all timers(except the overall timer) when paused
        # the reason why we don't stop the overall timer is that it kills the
        # purpose of overall timer which is supposed to show how much time has
        # been spent in the game
        if self.paused:
            self.blue_timer.is_active = False
            self.pink_timer.is_active = False
        else:
            # resime the timers
            if self.turn == BLUE:
                self.blue_timer.is_active = True
            else:
                self.pink_timer.is_active = True

    def draw_pause_menu(self, screen, font):
        # the very clean menu that we have been using
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # pause message, telling the user that the game is paused
        pause_text = font.render("GAME PAUSED", True, (255, 215, 0))
        text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

        screen.blit(pause_text, text_rect)

        # pause message instructions
        subtext = font.render(
            "Press P to resume or ESC to quit to Main Menu",
            True,
            (200, 200, 200),
        )
        subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(subtext, subtext_rect)

        # reset scores(that are being saved for each color) instruction
        reset_text = font.render("Press L to reset scores", True, WHITE)
        reset_rect = reset_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 100)
        )
        screen.blit(reset_text, reset_rect)

    def get_piece(
        self, row, column
    ):  # double checking if the click is correct
        if 0 <= row < ROWS and 0 <= column < COLUMNS:
            return self.board[row][column]
        return None  # if the piece is not in the range don't return anythign

    def get_valid_moves(self, piece):
        """
        Gets valid moves for a given piece including regular & capture moves.
        This function adds all of the possibilities together to pass to other 
        methods
        
        Args:
            piece (Piece): The piece to get valid moves for
        Raises:
            None 
        Returns:
            dict: Dictionary with valid move positions as keys and captured pieces as values
        """
        # first check for capture moves, whether the piece could capture and
        # where it could
        capture_moves = self.get_capture_moves(piece)
        regular_moves = self.get_regular_moves(piece)

        # Combine them into a single dictionary
        all_moves = {
            **regular_moves,
            **capture_moves,
        }  # since the game written
        # does not restrict user's choice, but for further consideration the
        # system is designed to be able to have a forcing captures mode as well

        return all_moves

    def get_regular_moves(self, piece):
        """
        gets non-capture moves for a given piece based on type and color.

        Args:
            piece (Piece): The piece to get moves for
        Raises: 
            None
        Returns:
            dict: dictionary with valid move positions as keys and empty lists as values
        """


        moves = {}
        if piece.king:  # when the piece becomes a king we need to change
            # the directions that the king moves in because it is different
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # the king could
            # go to every single diagonal
        else:
            if piece.color == BLUE:  # if the pieces are blue and not kings
                # they could only move up
                directions = [(-1, -1), (-1, 1)]  # move up, -1 is up and
                # second -1 is left, due to the index of the board
            else:
                directions = [(1, -1), (1, 1)]  # move down

        for dirrow, dircol in directions:
            new_row, new_col = (
                piece.row + dirrow,
                piece.column + dircol,
            )  # calculate
            # the new possible rows and columns that could be gone to using the
            # directions that we have set before,

            if (
                0 <= new_row < ROWS
                and 0 <= new_col < COLUMNS
                and self.board[new_row][new_col] == 0
            ):  # if the new row and column are within the board and are empty
                moves[(new_row, new_col)] = []  # we add the moves to the moves
                # dictionary and associate no values to it since it does not
                # involve any capturing (I almost crashed out twice to figure
                # this out)
        return moves

    def get_capture_moves(self, piece):
        """
        gets the captures that are possible for the pieces 
        and for that color of the pieces. 

        Args:
            piece (Piece): this is the piece that we get the 
            squares they could capture 

        Returns:
            dictionary : returns a dictionary of capture moves valid move as key and value
            as the captured

        """
        # no commnets for this function since it's essentially the same as the
        # get_regular_moves except the last section
        moves = {}

        if piece.king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # these
            # directions are about the index and not the actual direction adn
            # this means that they are actually reveresed, -1 is up and left
            # (first index up, second left) and so on
        else:
            if piece.color == BLUE:
                directions = [(-1, -1), (-1, 1)]
            else:
                directions = [(1, -1), (1, 1)]

        for (
            dr,
            dc,
        ) in directions:  # then we call the find_captures since it's a
            # recursive algorithm(which I wish it wasn't)
            self.find_captures(
                piece.row, piece.column, dr, dc, piece.color, moves, piece.king
            )

        return moves

    # Researched and got inspiration from the internet
    # and the idea of using recurion here is by ChatGPT: (I know it's not that
    # difficult)
    def find_captures(
        self, row, col, dr, dc, color, moves, is_king, captured=None
    ):  # a recursive algorithm that checks for the captures that a piece could
        # do and eventually appends them into the captured list
        """
        By far the most complicated function which involves recursion.
        Recursively finds all possible capture sequences for a piece.

        Args:
            row (int): Current row position
            col (int): Current column position 
            dr (int): Row direction
            dc (int): Column direction (-1 or 1)
            color (tuple): Piece color
            moves (dict): Dictionary to store valid moves
            is_king (bool): Whether piece is a king
            captured (list, optional): List of pieces captured in sequence
        Raises:
            None
        Returns:
            None: Updates moves dictionary in place
        """
        if captured is None:
            captured = []  # to make sure that the list doesn't reset everytime
            # the function is recursively called

        # check for enemy piece
        enemy_row, enemy_col = row + dr, col + dc  # checking the higher or
        # lower direcitons and saving them into temp values

        if not (
            0 <= enemy_row < ROWS and 0 <= enemy_col < COLUMNS
        ):  # if we're
            # out of range just return and stop checking)
            return

        enemy_piece = self.board[enemy_row][enemy_col]  # saving temporarily
        # where the enemy pieces are

        if (
            enemy_piece != 0
            and enemy_piece.color != color
            and enemy_piece not in captured
        ):  # if the square above or below is not captured or same color or none
            # Found enemy, check landing square
            land_row, land_col = (
                enemy_row + dr,
                enemy_col + dc,
            )  # this is where
            # we are going to land in

            if (
                0 <= land_row < ROWS
                and 0 <= land_col < COLUMNS
                and self.board[land_row][land_col] == 0
            ):  # now check if the landing is inside the board and if it's empty

                new_captured = captured + [enemy_piece]  # more than 1 captures
                moves[(land_row, land_col)] = new_captured  # add them to the
                # moves

                # look for additional captures from landing position
                if is_king:
                    # kings can capture in all directions
                    for new_dr, new_dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        self.find_captures(
                            land_row,
                            land_col,
                            new_dr,
                            new_dc,
                            color,
                            moves,
                            is_king,
                            new_captured,
                        )
                else:
                    # REgular pieces continue in their allowed directions
                    if color == BLUE:
                        next_directions = [(-1, -1), (-1, 1)]
                    else:
                        next_directions = [(1, -1), (1, 1)]

                    for new_dr, new_dc in next_directions:
                        self.find_captures(
                            land_row,
                            land_col,
                            new_dr,
                            new_dc,
                            color,
                            moves,
                            is_king,
                            new_captured,
                        )  # recursively do until hitting base

    def get_all_pieces(self, color):  # gets the pieces that are on the board
        """
        This gets all of the pieces from the color that are on the board.

        Args:
            color (Piece.color): this is the color of the piece

        Returns:
            list: list of all of the pieces with that color
        """
        pieces = []  # the pieces on the board
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def select_piece(self, row, col):
        """
        selects a piece at given position if valid. then checks if 
        it's for current player.

        Args:
            row (int): Row of piece to select
            col (int): Column of piece to select

        Returns:
            bool: True if piece was selected, False if invalid selection
        """
        piece = self.get_piece(row, col)

        if piece == 0 or piece.color != self.turn:  # is the piece's turn or is
            # there a piece at all?
            return False

        self.selected = piece
        self.valid_moves = self.get_valid_moves(piece)

        return True

    def move(self, row, col):
        """
        Moves piece to whatever position given as the arg position.
        Then it handles captures, king promotions, and turn changes
        using other methods available in this class.

        Args:
            row (int): row the piece is going to 
            col (int): column the piece is going to 

        Raises:
            None
        Returns:
            boolean: True if move successful, False if invalid
        """
        if not self.selected or (row, col) not in self.valid_moves:  # if the
            # piece is not selected or the squares are not in the valid moves list
            return False

        # get the captures for this move
        captures = self.valid_moves[(row, col)]

        # remove captured pieces from the board since if they are still there
        # the 2D borad is not accurate
        for captured_piece in captures:
            self.board[captured_piece.row][captured_piece.column] = 0  # turn
            # captured pieces to zeros in the board
            self.captured.append(captured_piece)  # add them to captures

            # now let's update each color's pieces
            if captured_piece.color == BLUE:
                if captured_piece.king:  # if king reduce from kings
                    self.cyan_kings -= 1
                else:  # if not then it's a pawn
                    self.cyan_pawns -= 1
            else:
                if captured_piece.king:
                    self.pink_kings -= 1
                else:
                    self.pink_pawns -= 1

        # now we move the piece
        old_row, old_col = self.selected.row, self.selected.column
        self.board[old_row][old_col] = 0
        self.board[row][col] = self.selected
        self.selected.move(row, col)

        # check for king promotion
        if not self.selected.king:  # only if already not a king, not necessary
            # but better to have it just to make sure
            if (self.selected.color == BLUE and row == 0) or (
                self.selected.color == DARK_PINK and row == ROWS - 1
            ):  # cheking for the last and first row

                # Replace the pawn with a king ( this could be done by just
                # changing the status of self.king,but for drawing them we
                # would face some complications)
                old_piece = self.selected
                new_king = King(row, col, old_piece.color)
                self.board[row][col] = new_king
                self.selected = new_king

                if self.selected.color == BLUE:  #  we add
                    # to kings poplultion and reduce from pawns
                    self.cyan_kings += 1
                    self.cyan_pawns -= 1
                else:
                    self.pink_kings += 1
                    self.pink_pawns -= 1

        # check for additional captures after this move
        if captures:
            additional_moves = self.get_valid_moves(self.selected)  # function
            # explained before

            capture_moves = {}
            for pos, caps in additional_moves.items():
                if caps:  # only keep moves that have captured pieces
                    capture_moves[pos] = caps

            if capture_moves:
                self.valid_moves = capture_moves
                return True  # Keep the same piece selected for multi-jump

        # End turn, next player please
        self.selected = None
        self.valid_moves = {}  # empty the valid moves
        self.change_turn()
        return True

    def change_turn(self):
        """
        Turn manager: Changes turn to other player and updates timers.
        Then stops current player's timer and starts other player's timer.
        It also checks for winner after turn change.

        Args:
            None
        Raises:
            None
        Returns:
            None
        """
        # stop current player's timer, start other player's timer when the
        # player makes a move( which is the same as them changing turns)
        if self.turn == BLUE:
            self.blue_timer.is_active = False
            self.pink_timer.is_active = True
        else:
            self.pink_timer.is_active = False
            self.blue_timer.is_active = True

        self.turn = DARK_PINK if self.turn == BLUE else BLUE
        self.check_winner()

    def update_timers(self):
        """ 
        updates game timers and checks for expired timers, if any, they lose.
        also converts milliseconds to seconds and updates both player timers.

        Args:
            None
        Raises:
            None
        Returns:
            None
        """
        current_time = pygame.time.get_ticks()  # time is ticking
        dt = (current_time - self.last_update) / 1000.0  # now we convert ms to
        # seconds, dt is delta time
        self.last_update = current_time
        self.blue_timer.update(dt)
        self.pink_timer.update(dt)

        # check for time already being expired and they're out of time
        # (or already done (the game))
        if self.blue_timer.is_expired():  # if blue's time is over pink wins
            self.winner = "Pink"
            self.status = "game_over"

        elif self.pink_timer.is_expired():  # opposite of last statement
            self.winner = "Blue"
            self.status = "game_over"

    # Clear winning and losing conditions:
    def check_winner(self):
        """
        Checks if game has a winner based on: whether there is pieces remaining
        or whether there is No valid moves left for either player
        Timer expired for either of the players which makes them lose.
        Updates winner attribute and game status if winner found.

        Args:
            None
        Raises:
            None
        Returns:
            None
        """
        blue_pieces = self.get_all_pieces(BLUE)
        pink_pieces = self.get_all_pieces(DARK_PINK)

        # check if a player has no pieces left:

        if not blue_pieces:
            self.winner = "Pink"
            self.status = "game_over"

        elif not pink_pieces:
            self.winner = "Blue"
            self.status = "game_over"

        else:
            # see if current player has no valid moves
            current_pieces = blue_pieces if self.turn == BLUE else pink_pieces
            has_moves = False

            for piece in current_pieces:
                if self.get_valid_moves(piece):
                    has_moves = True
                    break

            if not has_moves:  # no no moves left they should loose
                self.winner = "Pink" if self.turn == BLUE else "Blue"
                self.status = "game_over"

    def handle_click(self, row, col):
        """
        checks the mouse clicks for piece selection and movement.
        checks piece selection, movement , and turn so that it won't 
        cause certain problems for the other methods available. 
        As an example, the user should not be able to click on pieces
        that are not in the game.

        Args:
            row (int): Clicked board row
            col (int): Clicked board column
        Raises:
            None
        Returns:
            None
        """


        if self.status != "playing" or self.paused:  # if the game is over
            # don't check (or if the game is paused)
            return

        if (
            self.selected
        ):  # if it's already selected(maybe another square) then
            # try to move to clicked position
            if not self.move(row, col):
                # If move failed, try to select a new piece
                if not self.select_piece(row, col):
                    self.selected = None
                    self.valid_moves = {}
        else:
            # Select a piece
            self.select_piece(row, col)

    def draw_valid_moves(self, win):  # drawing the valid moves
        """
        draws the valid move positions for a piece.
        Displays circles indicating where selected piece can move.

        Args:
            win (pygame.Surface): Surface to draw on

        Returns:
            None
        """
        for row, col in self.valid_moves:
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(win, VALID_MOVE, (x, y), 29)

    def draw_selected(self, win):
        """
        highlights the currently selected piece with a yellow outline.

        Args:
            win (pygame.Surface): the window to draw on
        Raises: 
            None
        Returns:
            None
        """


        if self.selected: # if the piece is selected and of course it is their 
            # turn,
            x = self.selected.column * SQUARE_SIZE
            y = self.selected.row * SQUARE_SIZE
            pygame.draw.rect(
                win, SELECTED_OUTLINE, (x, y, SQUARE_SIZE, SQUARE_SIZE), 5
            ) # the outline is gold so that it's visible

    def draw_side_panel(self, win, font, game_timer):
        """
        Draws game information and timer panel which includes player timers, 
        piece and point counters, overall score counters in the history by each 
        piece, and the overall timer which shows the overall time spent by 
        both players.

        Args:
            win (pygame.Surface): Surface to draw on
            font (pygame.font.Font): Font for text
            game_timer (GameTimer): Overall game timer
        """
        SCREEN = win
        self.font = font

        pygame.draw.rect(SCREEN, BOARD_BORDER_COLOR, BOARD_RECT, BOARD_BORDER)
        pygame.draw.rect(SCREEN, PANEL_COLOR, PANEL_RECT)

        pygame.draw.rect(  # the pink timer
            SCREEN,
            PANEL_TIME_BG_COLOR,
            PANEL_TIMER_UP,
            border_radius=PANEL_TIME_RADIUS,
        )
        pygame.draw.rect(  # the blue timer
            SCREEN,
            PANEL_TIME_BG_COLOR,
            PANEL_TIMER_DOWN,
            border_radius=PANEL_TIME_RADIUS,
        )

        self.draw_scoreboard(SCREEN, font)
        # Title
        timer_text_title = font.render("Time", True, GOLD)
        text_title_rect = timer_text_title.get_rect(
            center=PANEL_OVERALL_TIMER_TEXT_TITLE_CENTRE
        )
        SCREEN.blit(timer_text_title, text_title_rect)

        # Overall timer
        pygame.draw.rect(
            SCREEN,
            PANEL_OVERALL_TIMER_COLOR,
            PANEL_OVERALL_TIMER_RECT,
            border_radius=PANEL_TIME_RADIUS,
        )
        # Overall timer text
        overall_timer_text = font.render(
            f"{game_timer.format_time()}", True, PANEL_OVERALL_TIMER_TEXT_COLOR
        )
        text_rect = overall_timer_text.get_rect(
            center=PANEL_OVERALL_TIMER_TEXT_CENTRE
        )
        SCREEN.blit(overall_timer_text, text_rect)

        # Current turn indicator
        (
            pygame.draw.rect(SCREEN, BLUE, BOARD_RECT, BOARD_BORDER)
            if self.turn == BLUE
            else pygame.draw.rect(SCREEN, DARK_PINK, BOARD_RECT, BOARD_BORDER)
        )
        turn_text = font.render(
            "Blue's Turn" if self.turn == BLUE else "Pink's Turn",
            True,
            BLUE if self.turn == BLUE else DARK_PINK,
        )
        SCREEN.blit(turn_text, (920, 120))

        # Scores
        blue_score = (
            len([p for p in self.get_all_pieces(BLUE)]) + self.cyan_kings * 2
        )

        pink_score = (
            len([p for p in self.get_all_pieces(DARK_PINK)])
            + self.pink_kings * 2
        )
        score_text = font.render(f"Blue: {blue_score}", True, WHITE)
        SCREEN.blit(score_text, (920, 900 - 180))

        score_text = font.render(f"Pink: {pink_score}", True, WHITE)
        SCREEN.blit(score_text, (920, 180))
        self.draw_captured_pieces(SCREEN)

        # Render and center the blue timer text
        blue_timer_text = font.render(
            f"{self.blue_timer.format_time()}", True, BLUE
        )
        blue_timer_rect = blue_timer_text.get_rect(
            center=PANEL_TIMER_DOWN.center
        )
        SCREEN.blit(blue_timer_text, blue_timer_rect)

        # Render and center the pink timer text
        pink_timer_text = font.render(
            f"{self.pink_timer.format_time()}", True, DARK_PINK
        )
        pink_timer_rect = pink_timer_text.get_rect(
            center=PANEL_TIMER_UP.center
        )
        SCREEN.blit(pink_timer_text, pink_timer_rect)
        # Winner display
        if self.winner:
            self.draw_winner(SCREEN, self.font)

    def draw_scoreboard(self, screen, font):
        """
        draws score panels showing win counts for both players and 
        shows total wins for blue and pink in their box that they 
        each have.

        Args:
            screen (pygame.Surface): surface draw on
            font (pygame.font.Font): Font to render text
        Raises:
            None
        Returns:
            None
        """
        # Draw the panel rectangles
        pygame.draw.rect(  # the pink scoreboard (upper panel)
            screen,
            PANEL_TIME_BG_COLOR,
            PANEL_SCORE_TIMER_UP,
            border_radius=PANEL_TIME_RADIUS,
        )
        pygame.draw.rect(  # the blue scoreboard (lower panel)
            screen,
            PANEL_TIME_BG_COLOR,
            PANEL_SCORE_TIMER_DOWN,
            border_radius=PANEL_TIME_RADIUS,
        )

        # Get stats data
        game_stats = stats.get()
        blue_wins = game_stats["Blue"]
        pink_wins = game_stats["Pink"]

        # Render the score texts
        blue_wins_text = font.render(f"{blue_wins}", True, BLUE)
        pink_wins_text = font.render(f"{pink_wins}", True, DARK_PINK)

        # Get text rectangles centered on the panel centers
        blue_rect = blue_wins_text.get_rect(center=PANEL_SCORE_DOWN_CENTRE)
        pink_rect = pink_wins_text.get_rect(center=PANEL_SCORE_UP_CENTRE)

        # Draw the texts
        screen.blit(blue_wins_text, blue_rect)
        screen.blit(pink_wins_text, pink_rect)

    #
    # def draw_total_games(self,screen,font):
    #
    #     # Total games
    #     total_text = font.render(f"Total Games: {total_games}", True, WHITE)
    #     total_rect = total_text.get_rect(
    #         center=(scoreboard_x + scoreboard_width // 2, scoreboard_y + 160)
    #     )
    #     screen.blit(total_text, total_rect)

    def get_sorted_captured(self, pieces):
        """
        sorts the list of the captured pieces by their values.
        Kings are 3 and pawns 1(why? because I want to).

        Args:
            pieces (list): The list of pieces captured 
        Raises:
            None
        Returns:
            list: returns the sorted version of the list 
        """
        # Sort kings first, then by row (optional)
        sorted_list = pieces.copy()
        mergeSort(sorted_list)  # sorts from highest to lowest
        return sorted_list

    def draw_captured_pieces(self, win):
        """
        shows the captured pieces in the side panel. these are
        small versions of captured pieces organized by color and type.

        Args:
            win (pygame.Surface): Surface to draw on
        Raises:
            None
        Returns:
            None
        """
        # Constants
        start_x = 930
        blue_start_y = HEIGHT - 310  # Captured pink pieces (by blue)
        pink_start_y = 264  # Captured blue pieces (by pink)
        spacing = 44
        pieces_per_row = 6
        captured_by_blue = self.get_sorted_captured(
            [piece for piece in self.captured if piece.color == DARK_PINK]
        )
        captured_by_pink = self.get_sorted_captured(
            [piece for piece in self.captured if piece.color == BLUE]
        )

        for idx, piece in enumerate(
            captured_by_blue
        ):  # go through the list of
            # pieces and draw the small version of them according to the
            # panel's position and their own radius and dimensions
            piece_x = start_x + (idx % pieces_per_row) * spacing
            piece_y = blue_start_y + (idx // pieces_per_row) * spacing
            piece.draw_small(win, piece_x, piece_y)

        for idx, piece in enumerate(captured_by_pink):  # same but for blue
            # pieces(captured by pink)
            piece_x = start_x + (idx % pieces_per_row) * spacing
            piece_y = pink_start_y + (idx // pieces_per_row) * spacing
            piece.draw_small(win, piece_x, piece_y)

    # inspired from this YT video showing python transparency:
    # https://www.youtube.com/watch?v=8_HVdxBqJmE
    def draw_winner(self, screen, font):
        """
        winner screen with semi-transparent overlay which shows winner
        message and game control options such as how to quit to main
        menu or how to reset the scores or restart the game.

        Args:
            screen (pygame.Surface): Surface to draw on

            font (pygame.font.Font): Font for text rendering

        Raises:
            None

        Returns:
            None
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Winner message
        win_text = f"{self.winner.upper()} WINS!"  # type:ignore
        # (this is to tell nvim to ignore this error by pyright I was
        # getting in nvim)

        text = font.render(win_text, True, (255, 215, 0))  # Gold
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, text_rect)

        subtext = font.render(
            "Press R to restart or ESC to quit to Main Menu",
            True,
            (200, 200, 200),
        )
        subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(subtext, subtext_rect)  # just draw the two text and the
        # background

        # Reset scores instruction
        reset_text = font.render("Press L to reset scores", True, WHITE)
        reset_rect = reset_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 100)
        )
        screen.blit(reset_text, reset_rect)

    def squares(self, win):
        """
        Draws the checkerboard pattern and tile of alternating colored squares.
        this leads to the classic checkers board this time cyan and white.
        this is a visual representation. 

        Args:
            win (pygame.Surface): Surface to draw the board on
        Raises: 
            None 
        Returns:
            None
        """
        win.fill(CYAN)
        for row in range(ROWS):
            if row % 2 == 1:  # start drawing from second square if row is odd
                # number
                for column in range(1, COLUMNS, 2):
                    pygame.draw.rect(
                        win,
                        WHITE,
                        (
                            row * SQUARE_SIZE,
                            column * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),  # makes sure we have enough squares correct color
                    )
            else:  # draw from the first square, every second squares if row is
                # even
                for column in range(0, COLUMNS, 2):
                    pygame.draw.rect(
                        win,
                        WHITE,
                        (
                            row * SQUARE_SIZE,
                            column * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )
            # puts squares once in two squares, we always start
            # drawing from top left corner, so when we start drawing,
            # we're at point 00

    def draw_whole(self, win):
        """
        draws the complete game including board, pieces, selected squares,
        and valid moves, this might not be initiated directly here but this 
        function is the one that creates the chain of reaction of creating 
        everything at the end of the main game loop .

        Args:
            win (pygame.Surface): Surface to draw on
        Raises:
            None
        Returns:
            None
        """


        self.squares(win)  # to draw the squares and the pieces at the same
        # time, here we just check if the square is a piece we draw one and if
        # not we don't

        # Draw pieces
        for row in range(ROWS):
            for columns in range(COLUMNS):
                piece = self.get_piece(row, columns)  # get the square
                if piece != 0:  # if there's no pieces in that square
                    piece.draw(win)  # type:ignore   hey Ms.Su, there was an
                    # annoying but from the nvim LSP I am using whihc was saying
                    # that there was a bug in this line becuase the piece is
                    # not always necessarily a Piece type, so please ignore
                    # this "type:ignore"

        # Draw selection and valid moves
        self.draw_selected(win)
        self.draw_valid_moves(win)  # this also makes sure that we check the
        # winner and the looser of the game since it contais it inside(if we go
        # further down into the functions
