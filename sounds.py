# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os


class Sounds:
    """Play music, and sound effects"""
    dir = "assets/sounds/"

    def __init__(self):
        """Initialize sound mixer"""
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10)
        self.load_sounds()

    def load_sounds(self):
        """Load all sound files"""
        self.pacman_chomp = pygame.mixer.Sound(os.path.join(self.dir, "pacman_chomp.wav"))
        self.fruit_eaten = pygame.mixer.Sound(os.path.join(self.dir, "fruit_eaten.wav"))

    def play_sound(self, sound, loop):
        """Play a sound effect"""
        channel = pygame.mixer.find_channel()
        if channel:
            channel.play(sound, loop)
