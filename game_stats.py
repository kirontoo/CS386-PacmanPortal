# CS386 - Pacman Portal
# Amy Nguyen-Dang

class GameStats:
    """Track statistics for the game."""

    def __init__(self, max_lives=0):
        """Initialize statistics"""

        # Set the max lives possible
        self.max_lives = max_lives

        self.reset()

        # Start game in a inactive state.
        self.game_active = False

        self.hs_active = False
        self.game_over = False

        # Start Highscore screen in inactive state.
        self.hs_active = False

    def reset(self):
        """Reset all statistics that can change during the game"""
        self.current_lives = self.max_lives
        self.current_score = 0
