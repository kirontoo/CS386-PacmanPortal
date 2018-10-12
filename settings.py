# CS-386 Pacman Portal
# Amy Nguyen-Dang


# noinspection PyAttributeOutsideInit
class Settings:

    def __init__(self):

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_midX = self.screen_width // 2
        self.screen_bg_color = (42, 78, 110)
        self.screen_padding = 30
        self.FPS = 30

        # Scoreboard settings
        self.scoreboard_text_color = (243, 248, 254)
        self.scoreboard_border_color = (255, 89, 0)
        self.scoreboard_font_size = 70

        # Pacman settings
        self.pacman_lives = 3