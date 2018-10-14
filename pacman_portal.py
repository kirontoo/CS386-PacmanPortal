# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import sys
from settings import Settings
from maze import Maze
from pacman import Pacman
from ghost import Ghost
from game_stats import GameStats
from start_screen import StartScreen
from sounds import Sounds

# noinspection PyAttributeOutsideInit


class PacmanPortal:

    def __init__(self):
        print("pacman portal init")
        """Initiate Pacman Portal game settings and objects"""
        pygame.init()
        pygame.display.set_caption("Pacman Portal")

        self.settings = Settings()
        self.stats = GameStats(self.settings.pacman_lives)
        self.clock = pygame.time.Clock()

        # Create a screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.maze = None
        self.mixer = Sounds()
        self.start_screen = StartScreen(self.screen, self.settings.screen_bg_color,
                                        "Pacman", "Portal")
        # Initialize game_objects
        self.create_game_objects()

    def run_game(self):
        print("run game")
        """Run the game"""
        while True:
            # Limit FPS
            self.clock.tick(60)

            # Check Keyboard and mouse events
            self.check_events()

            if self.stats.game_active:
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
                # Check for button clicks
                self.on_button_clicked(self.start_screen.play_button, (mouse_x, mouse_y))
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            # elif event.type == pygame.KEYUP:
            #     self.check_keyup_events(event)

    def check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.pacman.moving_right = True

            # Set all other pacman movement flags to false
            self.pacman.moving_up = False
            self.pacman.moving_down = False
            self.pacman.moving_left = False

        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = True

            # Set all other pacman movement flags to false
            self.pacman.moving_up = False
            self.pacman.moving_down = False
            self.pacman.moving_right = False

        elif event.key == pygame.K_UP:
            self.pacman.moving_up = True

            # Set all other pacman movement flags to false
            self.pacman.moving_left = False
            self.pacman.moving_down = False
            self.pacman.moving_right = False

        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = True

            # Set all other pacman movement flags to false
            self.pacman.moving_up = False
            self.pacman.moving_left = False
            self.pacman.moving_right = False

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

        # Create a maze
        self.maze = Maze(self.screen, "maze.txt")

        # Create pacman
        self.pacman = Pacman(self.screen, self.settings.pacman_speed)

        # Create ghosts
        self.blinky = Ghost(self.screen, "blinky", (500,500))
        self.clyde = Ghost(self.screen, "clyde", (600,500))
        self.inky = Ghost(self.screen, "inky", (700,500))
        self.pinky = Ghost(self.screen, "pinky", (800,500))

    def on_button_clicked(self, btn, pos):
        """Check if the button has been pressed."""
        m_x, m_y = pos
        btn_clicked = btn.rect.collidepoint(m_x, m_y)

        if btn_clicked and not self.stats.game_active:
            # Reset all settings
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            self.stats.reset()
            self.stats.game_active = True

    def update_objects(self):
        """Update all game objects"""
        self.pacman.update()
        self.blinky.update()
        self.inky.update()
        self.pinky.update()
        self.clyde.update()

    def update_screen(self):
        """Update the screen"""
        self.screen.fill(
            self.settings.screen_bg_color
        )

        # While the game is active, show all game objects
        if self.stats.game_active:
            self.maze.show_maze()
            self.pacman.blitme()
            self.blinky.blitme()
            self.inky.blitme()
            self.pinky.blitme()
            self.clyde.blitme()
        else:
            # Show the start screen when game is inactive
            self.start_screen.draw()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    game = PacmanPortal()
    game.run_game()
