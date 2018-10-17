# CS-386 Pacman Portal
# # Amy Nguyen-Dang

import pygame.font


# noinspection PyAttributeOutsideInit
class Button:

    def __init__(self, screen, msg, txt_color, btn_color, pos=(0, 0)):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.msg = msg

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = btn_color
        self.text_color = txt_color
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.x
        self.rect.y = self.y

        # The button message needs to be prepped only once.
        self.prep_msg()

    def __str__(self):
        return "{} Button, x: {} y: {}".format(self.msg, self.rect.x, self.rect.y)

    def prep_msg(self):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw the button on the screen."""
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
