# CS-386 Pacman Portal
# Amy Nguyen-Dang


# noinspection PyAttributeOutsideInit
class Settings:

    def __init__(self):

        # Screen settings
        self.screen_bg_color = (0, 0, 0)
        self.screen_padding = 30
        self.FPS = 30

        # Scoreboard settings
        self.scoreboard_text_color = (243, 248, 254)
        self.scoreboard_border_color = (255, 89, 0)
        self.scoreboard_font_size = 70

        # Pacman settings
        self.pacman_lives = 3
        self.pacman_speed = 1

        # Pellet settings
        self.pellet_points = 10
        self.pwr_pellet_points = 50

        # Ghost settings
        self.ghost_points = 100

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.screen_width = 1200
        self.screen_height = 800
