# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
from pygame.sprite import Sprite


class Pellet(Sprite):
    """Create pellets and power pellets"""

    def __init__(self, screen, pos=(0, 0), type="pellet"):
        """Initialize a pellet by type"""
        super(Pellet, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.type = type

        self.x, self.y = pos
        self.dir = "assets/sprites/pellets"

        self.rect = None
        self.image = None

        # Load sprites according to type
        if self.type == "pwr":
            self.animated = []
            self.fps_counter = 0
            self.load_pwr_pellet()
        else:
            self.load_pellet()

    def load_pwr_pellet(self):
        """Load power pellet animation"""

        for i in range(6):
            sprite = "pwr_pellet_" + str(i) + ".png"
            self.animated.append(pygame.image.load(os.path.join(self.dir, sprite)))

        self.image = self.animated[0]
        self.rect = self.animated[0].get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def load_pellet(self):
        self.image = pygame.image.load(os.path.join(self.dir, "pellet.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def update(self):
        """Update power pellet sprite"""
        if self.fps_counter + 1 >= 60:
            self.fps_counter = 0

        self.fps_counter += 1
        self.image = self.animated[self.fps_counter // 10]

    def blitme(self):
        self.screen.blit(self.image, self.rect)
