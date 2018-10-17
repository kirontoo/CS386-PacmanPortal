# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import sys
from pygame.sprite import Group
from pacman import Pacman
from settings import Settings
from maze import Maze
from game_stats import GameStats
from start_screen import StartScreen
from scoreboard import Scoreboard
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
        self.ghosts = Group()
        self.mixer = Sounds()

        # Initialize game_objects
        self.create_game_objects()

        # Update screen width and height
        self.settings.screen_width = self.maze.screen_rect.width
        self.settings.screen_height = self.maze.screen_rect.height

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

                # Check all collisions
                self.check_collisions()

            # Update the screen
            self.update_screen()

    def check_collisions(self):
        """Check collisions for all game objects"""

        # Check for pacman munching on pellets collisions
        pellet_collisions = pygame.sprite.spritecollide(self.pacman, self.maze.pellets, True)

        if pellet_collisions:
            # Play munching sound
            self.mixer.play_sound(self.mixer.pacman_chomp, 0)

            for pellet in pellet_collisions:
                if pellet.type == "pwr":
                    print("ghosts scared")
                    self.mixer.play_sound(self.mixer.ghost_scared, 0)
                    self.stats.current_score += self.settings.pwr_pellet_points

                    # Make all ghosts scared
                    for ghost in self.ghosts:
                        ghost.scared = True
                else:
                    self.stats.current_score += self.settings.pellet_points

                self.scoreboard.prep_score()

        # Check for pacman munching on power up cherry collisions
        cherry_collisions = pygame.sprite.spritecollide(self.pacman, self.maze.fruits, True)
        if cherry_collisions:
            for fruit in cherry_collisions:
                self.mixer.play_sound(self.mixer.fruit_eaten, 0)
                self.stats.current_score += fruit.points
                self.scoreboard.prep_score()

        # Check for pacman collisions with ghosts
        ghost_collisions = pygame.sprite.spritecollide(self.pacman, self.ghosts, False)

        if ghost_collisions:
            print("ghosts!! Oh no!")

            for ghost in ghost_collisions:
                if not ghost.scared and not ghost.dead and self.stats.current_lives > 0:
                    # If ghost is not scared, pacman dies and reset to original position

                    self.mixer.play_sound(self.mixer.life_lost, 0)

                    # Reset pacman
                    self.pacman = Pacman(self.screen, self.settings.pacman_speed, self.maze.pacman_init_pos)

                    # subtract lives
                    self.stats.current_lives -= 1

                    # redraw game stats
                    self.scoreboard.prep_lives()
                    self.scoreboard.prep_score()

                elif ghost.scared:
                    # Ghosts are scared, pacman can eat them. Ghosts run back and respawn.
                    self.mixer.play_sound(self.mixer.ghost_eaten, 0)
                    ghost.scared = False
                    ghost.dead = True

                else:
                    # Game over
                    print("game over")

                    # Play game over music
                    pygame.time.wait(5000)

                    # Go back to start screen
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)

                    # Reset game
                    self.stats.reset()
                    self.maze = self.maze = Maze(self.screen, "maze.txt", self.settings.pacman_speed)
                    self.pacman = self.maze.pacman
                    self.ghosts = self.maze.ghosts

                    self.pacman.moving_left = False
                    self.pacman.moving_right = False
                    self.pacman.moving_up = False
                    self.pacman.moving_down = False

                    self.scoreboard.prep_score()
                    self.scoreboard.prep_lives()

        # Check collisions with walls.
        for brick in self.maze.bricks:

            a_x = brick.rect.centerx - brick.rect.width // 2
            b_x = brick.rect.centerx + brick.rect.width // 2
            a_y = brick.rect.centery - brick.rect.width // 2
            b_y = brick.rect.centery + brick.rect.width // 2

            if (self.pacman.rect.right >= a_x and self.pacman.rect.left <= b_x) and \
                    (self.pacman.rect.centery >= a_y and self.pacman.rect.centery <= b_y):
                self.pacman.moving_left = False
                self.pacman.moving_right = False

                # Realign Pacman to the grid
                if self.pacman.rect.centerx % 15 != 0:

                    r = self.pacman.rect.centerx % 15
                    if r < 10:
                        self.pacman.rect.x -= r

            if (self.pacman.rect.bottom >= a_y and self.pacman.rect.top <= b_y) and \
                    (self.pacman.rect.centerx >= a_x and self.pacman.rect.centerx <= b_x):
                self.pacman.moving_up = False
                self.pacman.moving_down = False

                # Realign Pacman to the grid
                if self.pacman.rect.centery % 15 != 0:

                    r = self.pacman.rect.centery % 15
                    if r < 10:
                        self.pacman.rect.y += r

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

            print("x {} y {}".format(self.pacman.rect.centerx, self.pacman.rect.centery))

        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = True

            # Set all other pacman movement flags to false
            self.pacman.moving_up = False
            self.pacman.moving_down = False
            self.pacman.moving_right = False

            print("x {} y {}".format(self.pacman.rect.centerx, self.pacman.rect.centery))

        elif event.key == pygame.K_UP:
            self.pacman.moving_up = True

            # Set all other pacman movement flags to false
            self.pacman.moving_left = False
            self.pacman.moving_down = False
            self.pacman.moving_right = False

            print("x {} y {}".format(self.pacman.rect.centerx, self.pacman.rect.centery))

        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = True

            # Set all other pacman movement flags to false
            self.pacman.moving_up = False
            self.pacman.moving_left = False
            self.pacman.moving_right = False

            print("x {} y {}".format(self.pacman.rect.centerx, self.pacman.rect.centery))

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
        self.maze = Maze(self.screen, "maze.txt", self.settings.pacman_speed)

        # Create the start screen
        self.start_screen = StartScreen(self.screen, self.settings.screen_bg_color,
                                        "Pacman", "Portal")

        # Create scoreboard
        self.scoreboard = Scoreboard(self.screen, self.stats)

        # Create pacman
        self.pacman = self.maze.pacman

        # Create ghosts
        self.ghosts = self.maze.ghosts

    # #     TESTING STUFF
    #     for ghost in self.ghosts:
    #         ghost.scared = True

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
        for ghost in self.ghosts:
            ghost.update()

    def update_screen(self):
        """Update the screen"""
        self.screen.fill(
            self.settings.screen_bg_color
        )

        # While the game is active, show all game objects
        if self.stats.game_active:
            # Disable the mouse
            pygame.mouse.set_visible(False)

            self.scoreboard.draw()
            self.maze.show_maze()
            self.pacman.blitme()

            for ghost in self.ghosts:
                ghost.blitme()
        else:
            # Show the start screen when game is inactive
            self.start_screen.draw()

        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    game = PacmanPortal()
    game.run_game()
