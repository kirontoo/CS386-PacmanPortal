# CS-386 Pacman Portal
# Amy Nguyen-Dang

import os
from brick import Brick

import pygame


class Maze:

    def __init__(self, screen, file):
        self.maze_file = file
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.bricks = []
        self.maze = None
        self.dir = file

        self.build()
        self.set_screen_size()

    # TODO: set __str__

    def load_maze_file(self):
        """Read a maze file."""

        self.dir = "assets/mazes"
        file = os.path.join(self.dir, self.maze_file)

        with open(file, 'r') as f:
            self.maze = f.read()

    def build(self):
        """Build maze"""
        self.load_maze_file()

        pos_x = 0
        pos_y = 0

        new_brick = Brick(self.screen, (pos_x, pos_y))

        for c in self.maze:
            if c == '\n':
                pos_y += new_brick.rect.height
                pos_x = 0
                continue

            if c == ' ':
                pos_x += new_brick.rect.width
                continue

            # Create a brick
            new_brick = Brick(self.screen, (pos_x, pos_y))
            self.bricks.append(new_brick)
            pos_x += new_brick.rect.width

    def set_screen_size(self):
        """Set dynamic screen size"""
        width = self.get_screen_width()
        height = self.get_screen_height()

        self.screen = pygame.display.set_mode(
            (width, height)
        )

    def get_screen_width(self):
        """Find dynamic screen width"""
        row_of_bricks = 0

        for c in self.maze:
            if c == '\n':
                break

            row_of_bricks += 1

        width = row_of_bricks * self.bricks[0].rect.width
        return width

    def get_screen_height(self):
        """Find dynamic screen height"""
        column_of_bricks = 0
        for c in self.maze:
            if c == '\n':
                column_of_bricks += 1

        height = column_of_bricks * self.bricks[0].rect.height
        return height

    def show_maze(self):
        """Draw the maze"""
        for brick in self.bricks:
            brick.blitme()

