# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import sys
from settings import Settings
from maze import Maze
from pacman import Pacman

# noinspection PyAttributeOutsideInit


class PacmanPortal:

    def __init__(self):
        print("pacman portal init")
        """Initiate Pacman Portal game settings and objects"""
        pygame.init()
        pygame.display.set_caption("Pacman Portal")

        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Create a screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.maze = None

        # Initialzie game_objects
        self.create_game_objects()

    def run_game(self):
        print("run game")
        """Run the game"""
        while True:
            # Limit FPS
            self.clock.tick(60)

            # Check Keyboard and mouse events
            self.check_events()

            # Update all objects
            self.update_objects()

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
        """Respond to key presses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.pacman.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = True
        elif event.key == pygame.K_UP:
            self.pacman.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = True

    def check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.pacman.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = False
        elif event.key == pygame.K_UP:
            self.pacman.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = False

    def create_game_objects(self):
        print("create game objects")
        """Initialize all game objects"""
        self.maze = Maze(self.screen, "maze.txt")
        self.pacman = Pacman(self.screen, 3)

    def update_objects(self):
        self.pacman.update()

    def update_screen(self):
        """Update the screen"""
        self.screen.fill(
            self.settings.screen_bg_color
        )

        self.maze.show_maze()
        self.pacman.blitme()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    game = PacmanPortal()
    game.run_game()
