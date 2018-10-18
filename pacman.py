# CS-386 Pacman Portal
# Amy Nguyen-Dang

import os
import pygame
from pygame.sprite import Sprite
from text_image import TextImage


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
        self.portal1 = None
        self.portal2 = None
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

        self.temp = None

    def __str__(self):
        return "Pacman: x: {} y: {}".format(self.rect.x, self.rect.y)

    def adjust_position(self):
        """Adjust pacman's position to snap to the grid"""
        x = 0
        y = 0

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

        # Save pacman's location
        # find out which direction facing
        # use adjusted position to add size of brick to find nearest brick in grid

        x, y = self.adjust_position()
        print("x {} y {}".format(self.rect.x, self.rect.y))

        found = False

        # Pacman facing right
        if self.image in self.animated_right:
            print("facing right")

            # Find nearest brick on the right
            while x < self.screen_rect.width and not found:
                x += maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:
                        print("found")
                        if portal_type == "1":
                            self.portal1 = TextImage(self.screen, "1", 30, (0, 255, 0), (0, 0,0), (x, y))
                        else:
                            self.portal2 = TextImage(self.screen, "2", 30, (255, 0, 0), (0, 0,0), (x, y))

                        found = True
                        break

        # Pacman facing left
        elif self.image in self.animated_left:
            print("facing left")

            # Find nearest brick on the left
            while x >= 0 and not found:
                x -= maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:
                        print("found")
                        if portal_type == "1":
                            self.portal1 = TextImage(self.screen, "1", 30, (0, 255, 0), (0, 0, 0), (x, y))
                        else:
                            self.portal2 = TextImage(self.screen, "2", 30, (255, 0, 0), (0, 0, 0), (x, y))

                        found = True
                        break

        # Pacman facing up
        elif self.image in self.animated_up:
            print("facing up")

            # Find nearest brick on the above
            while y >= 0 and not found:
                y -= maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:
                        print("found")
                        if portal_type == "1":
                            self.portal1 = TextImage(self.screen, "1", 30, (0, 255, 0), (0, 0, 0), (x, y))
                        else:
                            self.portal2 = TextImage(self.screen, "2", 30, (255, 0, 0), (0, 0, 0), (x, y))

                        found = True
                        break

        # Pacman facing down
        elif self.image in self.animated_down:
            print("facing down")

            # Find nearest brick on the above
            while y <= self.screen_rect.height and not found:
                y += maze.brick_size

                for brick in maze.bricks:
                    if x == brick.rect.x and y == brick.rect.y:
                        print("found")
                        if portal_type == "1":
                            self.portal1 = TextImage(self.screen, "1", 30, (0, 255, 0), (0, 0, 0), (x, y))
                        else:
                            self.portal2 = TextImage(self.screen, "2", 30, (255, 0, 0), (0, 0, 0), (x, y))

                        found = True
                        break

        print(self.portal1)
        print(self.portal2)

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

        if self.portal1:
            self.portal1.draw()

        if self.portal2:
            self.portal2.draw()
