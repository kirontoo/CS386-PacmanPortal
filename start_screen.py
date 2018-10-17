# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
from button import Button


class StartScreen:

    def __init__(self, screen, bg_color, title, subtitle=None, font_size=100):
        """Initialize the start screen"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.title = title
        self.bg_color = bg_color
        self.font_size = font_size

        # Prepare the start screen
        self.title_image = None
        self.title_rect = None
        self.prep_title()

        if subtitle:
            self.subtitle_image = None
            self.subtitle_rect = None
            self.subtitle = subtitle
            self.prep_subtitle()

        # Create all buttons
        self.play_button = None
        self.hs_button = None
        self.prep_buttons()

    def prep_title(self):
        """Prepare the title image"""
        font = pygame.font.SysFont(None, self.font_size)
        text_color = (255, 245, 6)

        # Create and position the title
        self.title_image = font.render(self.title, True, text_color, self.bg_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.x = (self.screen_rect.width // 2) - (self.title_rect.width // 2)
        self.title_rect.y = self.title_rect.height // 2

    def prep_subtitle(self):
        """Prepare the subtitle image"""
        font = pygame.font.SysFont(None, self.font_size)
        text_color = (255, 255, 255)

        # Create and position the subtitle
        self.subtitle_image = font.render(self.subtitle, True, text_color, self.bg_color)
        self.subtitle_rect = self.subtitle_image.get_rect()
        self.subtitle_rect.x = (self.screen_rect.width // 2) - (self.subtitle_rect.width // 2)

        # Align it under the title
        self.subtitle_rect.top = self.title_rect.bottom

    def prep_buttons(self):
        """Prepare all buttons"""

        text_color = (255, 255, 255)

        # Create the play button
        x = self.screen_rect.centerx
        y = self.screen_rect.height - 250
        self.play_button = Button(self.screen, "Play", text_color, (0, 198, 24), (x, y))

        # Create high score button
        y = self.play_button.rect.bottom + 20
        self.hs_button = Button(self.screen, "Highscores", text_color, (255, 120, 0), (x, y))


    def draw(self):
        """Draw the title, subtitle and all buttons"""
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.subtitle_image, self.subtitle_rect)

        self.play_button.draw()
        self.hs_button.draw()
