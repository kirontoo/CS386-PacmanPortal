import os
import pygame


class Pacman:

    def __init__(self, screen, speed, pos=(0, 0)):
        """Initialize pacman"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.movement_speed = speed

        self.dir = "images/pacman"

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
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def load(self):
        """Load pacman animation images"""
        for i in range(8):
            image = "pacman_" + str(i) + ".png"

            if i in range(2):
                self.animated_right.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(2,4):
                self.animated_up.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(4,6):
                self.animated_left.append(pygame.image.load(os.path.join(self.dir, image)))
            if i in range(6,8):
                self.animated_down.append(pygame.image.load(os.path.join(self.dir, image)))

        self.rect = self.animated_right[0].get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.image = self.animated_right[0]

    def update(self):
        """Update pacman's position based on movement flag."""
        if self.fps_counter + 1 >= 60:
            self.fps_counter = 0

        self.fps_counter += 1

        if self.moving_right:
            self.image = self.animated_right[self.fps_counter // 30]
            self.rect.x += self.movement_speed

        if self.moving_left:
            self.image = self.animated_left[self.fps_counter // 30]
            self.rect.x -= self.movement_speed

        if self.moving_up:
            self.image = self.animated_up[self.fps_counter // 30]
            self.rect.y -= self.movement_speed

        if self.moving_down:
            self.image = self.animated_down[self.fps_counter // 30]
            self.rect.y += self.movement_speed

        self.x, self.y = self.rect.x, self.rect.y

    def blitme(self):
        """Draw pacman at its location"""
        self.screen.blit(self.image, self.rect)

