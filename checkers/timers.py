import pygame


class GameTimer:
    """
    total game time using Pygame's built-in timer.Provides methods
    to get elapsed time in seconds and formatted string plus the overall
    time spend in game. 

    Attributes:
        start_time (int): Initial time in milliseconds timer started
    """
    def __init__(self):
        """
        Starts the timer with current time as starting time and 
        uses pygame.time.get_ticks() in milliseconds to count.
        Args:
            None
        Raises:
            None
        Returns:    
            None
        """
        self.start_time = (
            pygame.time.get_ticks()
        )  # starting the built in timer
        # available in pygame itself, this is just a normal timer that tells the
        # user how much time they have spent in the game

    def get_time(self):
        """
        gets the time in seconds from milliseconds
        Args:
            None
        Raises: 
            None
        Returns:
            int: seconds passed
        """
        # Time in milliseconds since start
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        return elapsed_ms // 1000  # convert to seconds for easier calculations
        # further down the line

    def format_time(self):
        """
        this gets the format of the time to be able to neatly 
        print or render it afterwards
        Args:
            None
        Raises: 
            None
        Returns:
            str: this is a formatted {hrs}:{mins}:{secs} formatted
            string that makes the rendering neat
        """
        total = self.get_time()
        hours = total // 3600  # who plays checkers for hours?
        minutes = total // 60 - hours * 60  # making sure that the minutes is
        # reduced and never exceeds 60 when the value gets more than that

        seconds = total % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"


class PlayerTimer:
    """
    countdown timer for each player's turns which tracks remaining time.
    
    Attributes:
        time_left (float): Remaining time in seconds
        is_active (bool): is timer currently counting down
    """
    def __init__(self, initial_time=300):  # 5 minutes default 300/60 =5 
        """
        Creates new player timer with certain time limit.

        Args:
            initial_time (int, optional): Starting time in seconds. Defaults to 300 (5 minutes)
        Raises:
            None
        Returns:
            None
        """
        self.time_left = initial_time
        self.is_active = False

    # this updates the time by bringing it down 
    # each second that is passed in game
    def update(self, dt):       
        """
        Updates remaining time.
        
        Args:
            dt (float): delta time in seconds to subtract from remaining time
        Raises:
            None
        Returns:
            None
        """
        if self.is_active and self.time_left > 0:
            self.time_left -= dt

    def format_time(self):
        """
        Nicely formats the timer so that it is ready to render.

        Args:
            None
        Raises: 
            None
        Returns:
            str: formats the time to a mins:secs string 
        """
        minutes = int(self.time_left) // 60
        seconds = int(self.time_left) % 60
        return f"{minutes:02}:{seconds:02}"

    def is_expired(self):
        """
        is the time done or the limit for either player exceeded?
        Args:
            None
        Raises:
            None
        Returns:
            bool: whether there's any time left or not, True if 0 or less
            and False if any time left
        """ 
        return self.time_left <= 0
