import os


class Stats:
    """
    This is our data manager:
    Handles reading/writing win counts to a file and provides
    methods to update and retrieve stats.

    Attributes:
        file (str): Path to stats file
        blue_wins (int): blue player wins
        pink_wins (int): pink player wins
    """
    def __init__(self):
        """
        Creates the Stats with file path and loads existing data.
        """
        self.file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "database", "stats.txt"
        )  # this makes sure we
        # could find our .txt file which is inside parent directory and in our
        # database directory

        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        self.load_data()  # loads the data from the file

    def load_data(self):
        """
        Reads win counts from stats file. Then creates new file with 
        absolutely zero counts if file doesn't exist 
        otherwise it can't be read.
        Args:
            None
        Raises:
            None: Handles all exceptions internally
        Returns:
            None
        """
        try:
            with open(self.file, "r") as f:
                blue, pink = f.read().strip().split(",") # reads after 
                # splitting by commas
                self.blue_wins = int(blue)
                self.pink_wins = int(pink)
        except:
            self.blue_wins = self.pink_wins = 0 # if not successful then all 0
            self.save()

    def save(self):
        """
        Saves current win counts to stats.txt.

        Raises:
            IOError: If unable to write to file
        """
        with open(self.file, "w") as f: # writing the wins by seperating by 
            # columns
            f.write(f"{self.blue_wins},{self.pink_wins}")

    def add_win(self, color):
        """
        It adds the win number for each color that has won by one. 

        Args:
            color (string): this is the color that has won the game. 
        Raises:
            None
        Returns:   
            None
        """
        if color == "Blue":
            self.blue_wins += 1
        elif color == "Pink":
            self.pink_wins += 1

    def get(self):
        """
        Returns current win counts for both players.
        Args:
            None
        Raises: 
            None
        Returns:
            dict: Dictionary with "Blue" and "Pink" keys mapping to win counts

        """


        return {"Blue": self.blue_wins, "Pink": self.pink_wins}

    def reset(self):
        """
        Resets all win counters to zero and saves to file.

        Args:
            None
        Raises:
            None
        Returns:
            None
        """
        self.blue_wins = self.pink_wins = 0
        self.save()

    def get_text(self):
        """
        Gets win count string to be able to display it later
        Args:
            None
        Raises:
            None
        Returns:
            tuple: Two strings (bluewins,pinkwins)

        """
        return f"W: {self.blue_wins}", f"W: {self.pink_wins}"


# Quick access
stats = Stats()
