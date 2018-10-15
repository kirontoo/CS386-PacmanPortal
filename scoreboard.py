# CS386 - Pacman Portal
# Amy Nguyen-Dang

import pygame.font
import os
from pygame.sprite import Group
from pacman import Pacman


class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.lives = Group()

        self.prep_score()
        # self.prep_high_score()
        # self.prep_level()
        self.prep_lives()
        # self.load_data()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.current_score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            (0, 0, 0))

        # Display the score ate the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.x = 10
        self.score_rect.y = self.screen_rect.height - 80

    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color,
                                            self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        """Show how many ships are left."""
        self.lives_image = self.font.render("Lives:", True, self.text_color, (0, 0, 0))
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.x = self.screen_rect.centerx
        self.lives_rect.y = self.screen_rect.height - 80

        for life in range(self.stats.current_lives):
            pacman = Pacman(self.screen, 0)
            pacman.rect.y = self.screen_rect.height - 80
            pacman.rect.x = self.lives_rect.right + 15 + life * pacman.rect.width
            self.lives.add(pacman)

    def load_data(self):
        """Load all-time high score"""
        self.dir = os.path.dirname(__file__)
        file = os.path.join(self.dir, self.ai_settings.hs_file)

        # If the file doesn't exist, create one else load highscore
        if os.path.exists(file):

            with open(file, 'r') as f:
                try:
                    highest_score = f.readline()
                    self.stats.high_score = int(highest_score)
                except:
                    self.stats.high_score = 0
        else:
            f = open(file, 'w+')
            f.close()

    def save_data(self):
        """Save new highscore"""
        with open(os.path.join(self.dir, self.ai_settings.hs_file), 'a') as f:
            f.write(str(self.stats.score) + "\n")

        self.sort_highscores()

    def sort_highscores(self):
        """Sort all scores to find the highest score"""
        all_scores = []

        f = open(os.path.join(self.dir, self.ai_settings.hs_file), 'r')
        fl = f.readlines()
        for x in fl:
            all_scores.append(int(x))

        # sort all scores
        w = open(os.path.join(self.dir, self.ai_settings.hs_file), 'w')
        all_scores.sort(reverse=True)

        # write sorted scores to file
        for score in all_scores:
            w.write(str(score) + "\n")

        f.close()
        w.close()

    def draw(self):
        """Draw score and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        # self.screen.blit(self.high_score_image, self.high_score_rect)
        # self.screen.blit(self.level_image, self.level_rect)

        # Draw ships.
        self.screen.blit(self.lives_image, self.lives_rect)
        self.lives.draw(self.screen)
