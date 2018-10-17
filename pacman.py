# CS-386 Pacman Portal
# Amy Nguyen-Dang

import os
import pygame
from pygame.sprite import Sprite


class Pacman(Sprite):
    """Create a pacman object"""

    def __init__(self, screen, speed, pos=(0, 0)):
        """Initialize pacman"""
        super(Pacman, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.movement_speed = speed

        self.dir = "assets/sprites/pacman"

        # Load pacman animation
        self.animated_left = []
        self.animated_right = []
        self.animated_up = []
        self.animated_down = []

        self.rect = None
        self.image = None
        self.load()

        # For animation
        self.fps_counter = 0

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def __str__(self):
        return "Pacman: x: {} y: {}".format(self.rect.x, self.rect.y)

    def load(self):
        """Load pacman animation images"""
        for i in range(8):
            image = "pacman_" + str(i) + ".png"

            if i in range(2):
                self.animated_right.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(2, 4):
                self.animated_up.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(4, 6):
                self.animated_left.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(6, 8):
                self.animated_down.append(pygame.image.load(os.path.join(self.dir, image)))

        # Initialize position on the screen
        self.rect = self.animated_right[0].get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.image = self.animated_right[0]

    def adjust_position(self):
        """Adjust pacman's position to snap to the grid"""
        if self.rect.x % 30 != 0:
            self.rect.x -= (self.rect.x % 30)

        if self.rect.y % 30 != 0:
            self.rect.y -= (self.rect.y % 30)

    def update(self):
        """Update pacman's position based on movement flag."""

        # Track FPS count
        if self.fps_counter + 1 >= 60:
            self.fps_counter = 0

        self.fps_counter += 1

        # Update movement animation and position
        if self.moving_right:
            self.image = self.animated_right[self.fps_counter // 30]
            self.x += self.movement_speed

        if self.moving_left:
            self.image = self.animated_left[self.fps_counter // 30]
            self.x -= self.movement_speed

        if self.moving_up:
            self.image = self.animated_up[self.fps_counter // 30]
            self.y -= self.movement_speed

        if self.moving_down:
            self.image = self.animated_down[self.fps_counter // 30]
            self.y += self.movement_speed

        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        """Draw pacman at its location"""
        self.screen.blit(self.image, self.rect)
