# CS-386 Pacman Portal
# Amy Nguyen-Dang

import os
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from portal import Portal


class Pacman(Sprite):
    """Create a pacman object"""

    dir = "assets/sprites/pacman"

    def __init__(self, screen, speed, pos=(0, 0)):
        """Initialize pacman"""
        super(Pacman, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.movement_speed = speed

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

        # Count ghosts eaten
        self.ghosts_eaten = 0

        # Portals
        self.portals = Group()

    def __str__(self):
        return "Pacman: x: {} y: {}".format(self.rect.x, self.rect.y)

    def add_portal(self, portal_type, direction, pos):
        """Add a portal to the group and destroy the previous version"""
        for portal in self.portals:
            if portal.type == portal_type:
                portal.kill()

        portal = Portal(self.screen, portal_type, direction, pos)
        self.portals.add(portal)

    def adjust_position(self):
        """Adjust pacman's position to snap to the grid"""

        # Adjust position for x-axis
        r = self.rect.x % 30
        if r != 0:
            if r <= 16:
                x = self.rect.x - r
            else:
                x = self.rect.x + (30 - r)

        else:
            x = self.rect.x

        # Adjust position for y-axis
        r = self.rect.y % 30
        if r != 0:
            if r <= 16:
                y = self.rect.y - r
            else:
                y = self.rect.y + (30 - r)
        else:
            y = self.rect.y

        return x, y

    def create_portal(self, maze, portal_type):
        """Create a portal based on the direction pacman is facing"""

        # use adjusted position to add size of brick to find nearest brick in grid
        x, y = self.adjust_position()
        found = False

        # Pacman facing right
        if self.image in self.animated_right:

            # Find nearest brick on the right
            while x < self.screen_rect.width and not found:
                x += maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:

                        # Add a portal
                        self.add_portal(portal_type, "left", (x, y))
                        found = True
                        break

        # Pacman facing left
        elif self.image in self.animated_left:

            # Find nearest brick on the left
            while x >= 0 and not found:
                x -= maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:

                        # Add a portal
                        self.add_portal(portal_type, "right", (x, y))
                        found = True
                        break

        # Pacman facing up
        elif self.image in self.animated_up:

            # Find nearest brick above
            while y >= 0 and not found:
                y -= maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:

                        # Add a portal
                        self.add_portal(portal_type, "down", (x, y))
                        found = True
                        break

        # Pacman facing down
        elif self.image in self.animated_down:

            # Find nearest brick below
            while y <= self.screen_rect.height and not found:
                y += maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:

                        # Add a portal
                        self.add_portal(portal_type, "up", (x, y))
                        found = True
                        break

    def enter_portal(self, portal):
        """Enter a portal and teleport to the other portal."""
        other_portal = None

        # Find the other portal
        for p in self.portals:
            if p.type != portal.type:
                other_portal = p

        if not other_portal:
            return

        if other_portal.direction == "right":
            # Teleport pacman to the right of the portal
            self.x = other_portal.rect.x + other_portal.rect.width
            self.y = other_portal.rect.y

            # Set movement flags
            self.moving_down = False
            self.moving_up = False
            self.moving_left = False
            self.moving_right = True

            self.image = self.animated_right[0]

        elif other_portal.direction == "left":
            # Teleport to the left of the portal
            self.x = other_portal.rect.x - other_portal.rect.width
            self.y = other_portal.rect.y

            # Set movement flags
            self.moving_down = False
            self.moving_up = False
            self.moving_left = True
            self.moving_right = False

            self.image = self.animated_left[0]

        elif other_portal.direction == "up":
            # Teleport to above the portal
            self.x = other_portal.rect.x
            self.y = other_portal.rect.y - other_portal.rect.height

            # Set movement flags
            self.moving_down = False
            self.moving_up = True
            self.moving_left = False
            self.moving_right = False

            self.image = self.animated_up[0]

        elif other_portal.direction == "down":
            # Teleport to below the portal
            self.x = other_portal.rect.x
            self.y = other_portal.rect.y + other_portal.rect.height

            # Set movement flags
            self.moving_down = True
            self.moving_up = False
            self.moving_left = False
            self.moving_right = False

            self.image = self.animated_down[0]

        self.rect.x, self.rect.y = self.x, self.y

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

    def travel(self, portal):
        """Travel through a existing portal."""

        # Check if pacman is facing the portal
        if self.image in self.animated_right and portal.direction == "left":
            self.enter_portal(portal)

        elif self.image in self.animated_left and portal.direction == "right":
            self.enter_portal(portal)

        elif self.image in self.animated_up and portal.direction == "down":
            self.enter_portal(portal)

        elif self.image in self.animated_down and portal.direction == "up":
            self.enter_portal(portal)

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

        for portal in self.portals:
            portal.draw()
