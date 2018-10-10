# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import sys
from settings import Settings
from maze import Maze


# noinspection PyAttributeOutsideInit
class PacmanPortal:
    def __init__(self):
        """Initiate pong game settings and objects"""
        pygame.init()
        pygame.display.set_caption("Pong")

        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Create a screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.maze = Maze(self.screen, "maze.txt")

    def run_game(self):
        """Run the game"""
        while True:
            # Limit FPS
            self.clock.tick(30)

            # Check Keyboard and mouse events
            self.check_events()

            # Update the screen
            self.update_screen()

    def check_events(self):
        """Check for any keyboard events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self, event):
        """Check all keydown events"""
        if event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        """Check all key up events"""
        if event.key == pygame.K_RIGHT:
            self.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.moving_left = False
        elif event.key == pygame.K_UP:
            self.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.moving_down = False

    def update_screen(self):
        """Update the screen"""
        self.screen.fill(
            self.settings.screen_bg_color
        )

        self.maze.show_maze()

        # Make the most recently drawn screen visible
        pygame.display.flip()


game = PacmanPortal()
game.run_game()
