# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
from pygame.sprite import Group
from brick import Brick
from cherry import Cherry
from pellet import Pellet
from pacman import Pacman
from ghost import Ghost


class Maze:
    """Build a maze level"""

    def __init__(self, screen, file, pacman_speed):
        self.maze_file = file
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.pacman_speed = pacman_speed
        self.pacman_init_pos = None

        self.brick_size = 0
        self.grid = None
        self.dir = file

        # Grid objects
        self.bricks = Group()
        self.fruits = Group()
        self.pellets = Group()
        self.ghosts = Group()
        self.pacman = None

        self.build()
        self.set_screen_size()

    # TODO: set __str__

    def load_maze_file(self):
        print("load maze")
        """Read a maze file."""

        self.dir = "assets/mazes"
        file = os.path.join(self.dir, self.maze_file)

        with open(file, 'r') as f:
            self.grid = f.read()

    def build(self):
        print("build maze")
        """Build maze"""
        self.load_maze_file()

        pos_x = 0
        pos_y = 0

        new_brick = Brick(self.screen, (pos_x, pos_y))
        self.brick_size = new_brick.rect.width

        for c in self.grid:
            if c == '\n':
                pos_y += new_brick.rect.height
                pos_x = 0
                continue

            if c == ' ':
                pos_x += new_brick.rect.width
                continue

            # Build walls
            if c == 'x':
                # Create a brick
                new_brick = Brick(self.screen, (pos_x, pos_y))
                self.bricks.add(new_brick)

            # Build pacman
            if c == '^':
                self.pacman = Pacman(self.screen, self.pacman_speed, (pos_x, pos_y))
                # Save pacman's initial position.
                self.pacman_init_pos = (pos_x, pos_y)

            # Build fruits
            if c == 'f':
                fruit = Cherry(self.screen, (pos_x, pos_y))
                self.fruits.add(fruit)

            # Build pellets
            if c == '.':
                pellet = Pellet(self.screen, (pos_x, pos_y))
                self.pellets.add(pellet)

            if c == "*":
                pwr_pellet = Pellet(self.screen, (pos_x, pos_y), "pwr")
                self.pellets.add(pwr_pellet)

            if c == "b":
                ghost = Ghost(self.screen, "blinky", (pos_x, pos_y))
                self.ghosts.add(ghost)

            if c == "c":
                ghost = Ghost(self.screen, "clyde", (pos_x, pos_y))
                self.ghosts.add(ghost)

            if c == "i":
                ghost = Ghost(self.screen, "inky", (pos_x, pos_y))
                self.ghosts.add(ghost)

            if c == "p":
                ghost = Ghost(self.screen, "pinky", (pos_x, pos_y))
                self.ghosts.add(ghost)

            pos_x += new_brick.rect.width

    def set_screen_size(self):
        """Set dynamic screen size"""
        width = self.get_screen_width()
        height = self.get_screen_height()

        # Add to height for scoreboard
        height += (80 + self.brick_size)

        self.screen = pygame.display.set_mode(
            (width, height)
        )

    def get_screen_width(self):
        """Find dynamic screen width"""
        row_of_bricks = 0

        for c in self.grid:
            if c == '\n':
                break

            row_of_bricks += 1
        width = row_of_bricks * self.brick_size
        return width

    def get_screen_height(self):
        """Find dynamic screen height"""
        column_of_bricks = 0

        for c in self.grid:
            if c == '\n':
                column_of_bricks += 1

        height = column_of_bricks * self.brick_size
        return height

    def show_maze(self):
        """Draw the maze"""
        for brick in self.bricks:
            brick.blitme()

        for pwr_up in self.fruits:
            pwr_up.blitme()

        for pellet in self.pellets:
            if pellet.type == "pwr":
                pellet.update()
            pellet.blitme()
