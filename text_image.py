# CS386 - Pacman Portal
# Amy Nguyen-Dang

import pygame.font


class TextImage:
    """A class to create a text image."""

    def __init__(self, screen, text, size, color, bg_color, pos=(0, 0)):
        """Initialize text image attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text = text
        self.text_size = size
        self.text_color = color
        self.bg_color = bg_color
        self.x, self.y = pos

        self.image = None
        self.rect = None
        self.prep_text()

    def __str__(self):
        return "{} Text Image, x: {} y: {}".format(self.text, self.rect.x, self.rect.y)

    def prep_text(self):
        """Turn the text into a rendered image"""

        font = pygame.font.SysFont(None, self.text_size)
        self.image = font.render(self.text, True, self.text_color, self.bg_color)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.x, self.y

    def draw(self):
        print("draw!")
        self.screen.blit(self.image, self.rect)