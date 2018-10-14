# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
from pygame.sprite import Sprite

class Cherry(Sprite):
    """Create a power up cherry object."""

    def __init__(self, screen, pos=(0,0)):
        """Initialize Cherry Power up"""

        super(Cherry, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.dir = "assets/sprites/power_ups"

        # Load cherry sprite
        self.image = pygame.image.load(os.path.join(self.dir, "power_up_cherry.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        """Draw the cherry at its location"""
        self.screen.blit(self.image, self.rect)