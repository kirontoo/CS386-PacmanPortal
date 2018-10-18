# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
from pygame.sprite import Sprite


class Portal(Sprite):
    """Create a portal"""

    dir = "assets/sprites/portals"

    def __init__(self, screen, portal_type, direction=None, pos=(0, 0)):
        """Initialize a portal"""

        super(Portal, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.direction = direction
        self.x, self.y = pos
        self.type = portal_type

        self.image = None
        self.rect = None
        self.build()

    def __str__(self):
        return "Portal - x: {}, y: {}, direction: {}, type: {}".format(self.x, self.y, self.direction, self.type)

    def build(self):
        """Build the portal"""

        sprite = "portal_" + str(self.type-1) + ".png"
        self.image = pygame.image.load(os.path.join(self.dir, sprite))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def draw(self):
        """Draw the portal"""
        self.screen.blit(self.image, self.rect)
