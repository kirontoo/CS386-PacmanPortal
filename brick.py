# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
from pygame.sprite import Sprite


class Brick(Sprite):

    def __init__(self, screen, pos=(0, 0), brick_type="brick"):
        """Initialize the brick and set its starting position"""

        super(Brick, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.type = brick_type

        # Load the brick or gate image and get its rect
        if self.type == "gate":
            self.image = pygame.image.load(os.path.join("assets/sprites", "gate.png")).convert()
        else:
            self.image = pygame.image.load(os.path.join("assets/sprites", "brick2.png")).convert()

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = pos
        self.x, self.y = pos

    def blitme(self):
        """Draw the brick at its location"""
        self.screen.blit(self.image, self.rect)