# CS386 - Pacman Portal
# Amy Nguyen-Dang

import pygame.font
import os
from pygame.sprite import Group
from pacman import Pacman


# noinspection PyAttributeOutsideInit
class Scoreboard:
    """A class to report scoring information."""

    file = "highscores.txt"

    def __init__(self, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_lives()
        self.load_data()

    def prep_score(self):
        """Turn the score into a rendered image."""
        self.score_image = self.font.render("Score:", True, self.text_color, (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.x = 10
        self.score_rect.y = self.screen_rect.height - 80

        rounded_score = int(round(self.stats.current_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.total_score_image = self.font.render(score_str, True, self.text_color,
                                                  (0, 0, 0))

        # Display the score at the bottom of the screen.
        self.total_score_rect = self.total_score_image.get_rect()
        self.total_score_rect.x = self.score_rect.width + 15
        self.total_score_rect.y = self.score_rect.y

    def prep_lives(self):
        """Show how many lives are left."""
        self.lives_image = self.font.render("Lives:", True, self.text_color, (0, 0, 0))
        self.lives_rect = self.lives_image.get_rect()

        # Position it at the bottom of the screen
        self.lives_rect.x = self.screen_rect.centerx
        self.lives_rect.y = self.screen_rect.height - 80

        self.lives = Group()

        # Create sprites to indicate number of lives
        for life in range(self.stats.current_lives):
            pacman = Pacman(self.screen, 0)
            pacman.rect.y = self.screen_rect.height - 80
            pacman.rect.x = self.lives_rect.right + 15 + life * pacman.rect.width
            self.lives.add(pacman)

    def load_data(self):
        """Load all-time high score"""
        self.dir = os.path.dirname(__file__)
        file = os.path.join(self.dir, self.file)

        # If the file doesn't exist, create one
        if not os.path.exists(file):

            f = open(file, 'w+')
            f.close()

    def save_data(self):
        """Save new highscore"""
        with open(os.path.join(self.dir, self.file), 'a') as f:
            f.write(str(self.stats.current_score) + "\n")

        self.sort_highscores()

    def sort_highscores(self):
        """Sort all scores to find the highest score"""
        all_scores = []

        f = open(os.path.join(self.dir, self.file), 'r')
        fl = f.readlines()
        for x in fl:
            all_scores.append(int(x))

        # sort all scores
        w = open(os.path.join(self.dir, self.file), 'w')
        all_scores.sort(reverse=True)

        # write sorted scores to file
        for score in all_scores:
            w.write(str(score) + "\n")

        f.close()
        w.close()

    def draw(self):
        """Draw the scoreboard to the screen."""
        self.screen.blit(self.total_score_image, self.total_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        # self.screen.blit(self.high_score_image, self.high_score_rect)
        # self.screen.blit(self.level_image, self.level_rect)

        # Draw lives.
        self.screen.blit(self.lives_image, self.lives_rect)
        self.lives.draw(self.screen)
