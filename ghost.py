# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os

ghost_types = ["inky", "pinky", "blinky", "clyde"]


class Ghost:
    def __init__(self, screen, type="inky", pos=(0, 0)):
        """Initialize Ghost"""
        self.type = type
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.movement_speed = 0
        self.dir = "assets/sprites/ghost_" + self.type

        # Load ghost animations
        self.animated_sprites = []
        self.animated_eyes = []
        self.scared_sprite = None
        self.rect = None
        self.image = None
        self.load()

        # Set movement speed by type
        self.set_speed()

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Set initial ghost state
        self.scared = False
        self.dead = False

    # TODO: set __str__

    def load(self):
        """Load ghost animation images"""

        # Load ghost by type and eyes sprites
        for i in range(4):
            sprite = "ghost_" + self.type + str(i)
            self.animated_sprites.append(pygame.image.load(os.path.join(self.dir, sprite)))

            eyes_sprite = "ghost_eyes_" + str(i)
            eyes_dir = "assets/sprites/ghost_eyes"
            self.animated_eyes.append(pygame.image.load(os.path.join(eyes_dir, eyes_sprite)))

        # Load scared ghost sprite
        scared_ghost_dir = "assets/sprites/ghost_scared"
        self.scared_sprite = pygame.image.load(os.path.join(scared_ghost_dir, "ghost_scared"))

        # Initialize position on the screen
        self.image = self.animated_sprites[2]
        self.rect = self.animated_sprites[0].get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def set_speed(self):
        """Set the ghost's movement speed by type of ghost"""
        if self.type == "pinky":
            self.movement_speed = 5
        if self.type == "blinky":
            self.movement_speed = 5
        if self.type == "inky":
            self.movement_speed = 5
        if self.type == "clyde":
            self.movement_speed = 5

    def update(self):
        """Update the ghost's position based on movement flag and state."""

        # Update movement animation and position
        if self.scared:
            self.image = self.scared_sprite

        if self.moving_right:
            if self.dead:
                self.image = self.animated_eyes[3]
            else:
                self.image = self.animated_sprites[3]
            self.x += self.movement_speed

        if self.moving_left:
            if self.dead:
                self.image = self.animated_eyes[1]
            else:
                self.image = self.animated_sprites[1]
            self.x -= self.movement_speed

        if self.moving_up:
            if self.dead:
                self.image = self.animated_eyes[2]
            else:
                self.image = self.animated_sprites[2]
            self.y -= self.movement_speed

        if self.moving_down:
            if self.dead:
                self.image = self.animated_eyes[0]
            else:
                self.image = self.animated_sprites[0]
            self.y += self.movement_speed

        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        """Draw the ghost at its location"""
        self.screen.blit(self.image, self.rect)