# CS-386 Pacman Portal
# Amy Nguyen-Dang

import pygame
import os
import math
from pygame.sprite import Sprite


class Ghost(Sprite):
    """Create a ghost object"""

    def __init__(self, screen, ghost_type="inky", pos=(0, 0)):
        """Initialize Ghost"""

        super(Ghost, self).__init__()

        self.type = ghost_type
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x, self.y = pos
        self.movement_speed = 0
        self.dir = "assets/sprites/ghost_" + self.type

        # Save original position
        self.original_pos_x = self.x
        self.original_pos_y = self.y

        # Load ghost animations
        self.animated_sprites = []
        self.animated_eyes = []
        self.scared_sprite = None
        self.rect = None
        self.image = None
        self.load()

        # Set movement speed by type
        self.set_speed()

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Set initial ghost state
        self.scared = False
        self.dead = False

        # Set frame counts
        self.frame_count = 0

        # Set Chase, and Scatter mode
        self.chase = False
        self.scatter = False

        self.in_spawn = True

        # Set destination
        self.dest_x = 0
        self.dest_y = 0

    def __str__(self):
        return "Ghost - type: {}, x: {}, y: {}, scared: {}, dead: {}".format(self.type, self.rect.x, self.rect.y, self.scared,self.dead)

    def __adjust_position__(self):
        """Adjust ghost's position to snap to the grid"""

        # Adjust position for x-axis
        r = self.rect.x % 30
        if r != 0:
            if r <= 16:
                x = self.rect.x - r
            else:
                x = self.rect.x + (30 - r)

        else:
            x = self.rect.x

        # Adjust position for y-axis
        r = self.rect.y % 30
        if r != 0:
            if r <= 16:
                y = self.rect.y - r
            else:
                y = self.rect.y + (30 - r)
        else:
            y = self.rect.y

        return x, y

    def __decide_direction__(self, x, y, bricks):
        """Decide which path to take"""

        # Check for walls
        wall_left = self.__is_wall__(bricks, "left")
        wall_right = self.__is_wall__(bricks, "right")
        wall_up = self.__is_wall__(bricks, "up")
        wall_down = self.__is_wall__(bricks, "down")

        if x > y:
            # Move towards destination horizontally
            if self.dest_x < self.rect.x:
                # If possible move left
                if not wall_left:
                    # Move left
                    self.__move_left__()
                else:
                    # Move up or down towards destination instead
                    if self.dest_y > self.rect.y:
                        if not wall_down:
                            self.__move_down__
                    else:
                        if not wall_up:
                            self.__move_up__()
            else:
                # If possible move right
                if not wall_right:
                    self.__move_right__()
                else:
                    # Move up or down towards destination instead
                    if self.dest_y > self.rect.y:
                        if not wall_down:
                            self.__move_down__
                    else:
                        if not wall_up:
                            self.__move_up__()
        else:
            # Move towards destination vertically
            if self.dest_y < self.rect.y:
                # If possible move up
                if not wall_up:
                    self.__move_up__()
                else:
                    # Move left or right towards destination instead
                    if self.dest_x < self.rect.x:
                        if not wall_left:
                            self.__move_left__()
                        else:
                            if not wall_right:
                                self.__move_right__()
            else:
                # If possible move down
                if not wall_down:
                    self.__move_down__()
                else:
                    # Move left or right towards destination instead
                    if self.dest_x < self.rect.x:
                        if not wall_left:
                            self.__move_left__()
                        else:
                            if not wall_right:
                                self.__move_right__()

    def __distance__(self, x, y):
        """Claculate Linear distance"""
        delx = self.__distanceX__(x)
        dely = self.__distanceY__(y)

        return math.sqrt(delx ** 2 + dely ** 2)

    def __distanceX__(self, x):
        """Calculate horizontal distance"""
        return abs(self.rect.x - x)

    def __distanceY__(self, y):
        """Calculate vertical distance"""
        return abs(self.rect.y - y)

    def __is_wall__(self, bricks, dir):
        """Check if there is a wall in front of ghost"""
    
        x, y = self.__adjust_position__()

        for brick in bricks:
            
            a_x = brick.rect.centerx - brick.rect.width // 2
            b_x = brick.rect.centerx + brick.rect.width // 2
            a_y = brick.rect.centery - brick.rect.width // 2
            b_y = brick.rect.centery + brick.rect.width // 2

            # Look for a wall within range of the ghost
            if (self.rect.right >= a_x and self.rect.left <= b_x) and (a_y <= self.rect.centery <= b_y) and brick.type == "brick":

                # Check for wall on the left
                if (brick.rect.right >= self.rect.left) and dir == "left":
                    return True

                # Check for wall on the right
                if brick.rect.left <= self.rect.right and dir == "right":

                    return True

            if (self.rect.bottom >= a_y and self.rect.top <= b_y) and (a_x <= self.rect.centerx <= b_x) and brick.type == "brick":

                # Check for on the top
                if (brick.rect.bottom >= self.rect.top) and dir == "up":

                    return True

                # Check for wall on the bottom
                if (brick.rect.top <= self.rect.bottom) and dir == "down":
                    return True

        return False
    
    def __move_left__(self):
        self.moving_left = True
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def __move_right__(self):
        self.moving_left = False
        self.moving_right = True
        self.moving_up = False
        self.moving_down = False

    def __move_up__(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_up = True
        self.moving_down = False

    def __move_down__(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = True

    def __blinky__(self, pacman, bricks):

        # Find distance between Blinky and Pacman
        x = self.__distanceX__(pacman.rect.x)
        y = self.__distanceY__(pacman.rect.y)

        # Exit Spawn
        if self.in_spawn:
            self.exit_spawn(bricks)
        else: 
            # Set destination
            self.dest_x = pacman.rect.x
            self.dest_y = pacman.rect.y

        # Decide direction to move to
        self.__decide_direction__(x, y, bricks)

    def exit_spawn(self, bricks):
        """Exit from spawn"""

        # Set flag after ghost exits spawn
        if self.rect.x == self.dest_x and self.rect.y == self.dest_y:
            self.in_spawn = False
            return
        
        # Find the gate
        for brick in bricks:
            if brick.type == "gate":
                self.dest_x = brick.rect.x
                self.dest_y = brick.rect.y - brick.rect.height
                break

    def find_path(self, pacman, bricks):
        """Find path to pacman."""
        if self.type == "inky":
            pass
        if self.type == "pinky":
            pass
        if self.type == "blinky":
            self.__blinky__(pacman, bricks)
        if self.type == "clyde":
            pass

    def load(self):
        """Load ghost animation images"""

        # Load ghost by type and eyes sprites
        for i in range(4):
            sprite = "ghost_" + self.type + "_" + str(i) + ".png"
            self.animated_sprites.append(pygame.image.load(os.path.join(self.dir, sprite)))

            eyes_sprite = "ghost_eyes_" + str(i) + ".png"
            eyes_dir = "assets/sprites/ghost_eyes"
            self.animated_eyes.append(pygame.image.load(os.path.join(eyes_dir, eyes_sprite)))

        # Load scared ghost sprite
        scared_ghost_dir = "assets/sprites/ghost_scared"
        self.scared_sprite = pygame.image.load(os.path.join(scared_ghost_dir, "ghost_scared.png"))

        # Initialize position on the screen
        self.image = self.animated_sprites[2]
        self.rect = self.animated_sprites[0].get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def set_speed(self):
        """Set the ghost's movement speed by type of ghost"""
        if self.type == "pinky":
            self.movement_speed = 1
        if self.type == "blinky":
            self.movement_speed = 1.5
        if self.type == "inky":
            self.movement_speed = 1
        if self.type == "clyde":
            self.movement_speed = 1

    def update(self):
        """Update the ghost's position based on movement flag and state."""

        if self.scared and not self.dead:
            self.image = self.scared_sprite
            self.frame_count += 1

            seconds = self.frame_count // 60

            # After 5 seconds, ghost no longer scared
            if seconds >= 5:
                self.scared = False

        if self.dead and not self.scared:
            self.image = self.animated_eyes[0]

        if not self.dead and not self.scared:
            self.frame_count = 0
            self.image = self.animated_sprites[2]

        # Update movement animation and position
        if self.moving_right:
            if self.dead:
                self.image = self.animated_eyes[3]
            elif self.scared:
                self.image = self.scared_sprite
            else:
                self.image = self.animated_sprites[3]
            self.x += self.movement_speed

        if self.moving_left:
            if self.dead:
                self.image = self.animated_eyes[1]
            elif self.scared:
                self.image = self.scared_sprite
            else:
                self.image = self.animated_sprites[1]
            self.x -= self.movement_speed

        if self.moving_up:
            if self.dead:
                self.image = self.animated_eyes[2]
            elif self.scared:
                self.image = self.scared_sprite
            else:
                self.image = self.animated_sprites[2]
            self.y -= self.movement_speed

        if self.moving_down:
            if self.dead:
                self.image = self.animated_eyes[0]
            elif self.scared:
                self.image = self.scared_sprite
            else:
                self.image = self.animated_sprites[0]
            self.y += self.movement_speed

        self.rect.x, self.rect.y = self.x, self.y

    def blitme(self):
        """Draw the ghost at its location"""
        self.screen.blit(self.image, self.rect)
