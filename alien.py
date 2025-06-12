import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """A class to represent a single alien."""

    def __init__(self, ai_game, x_pos=None, in_formation=False):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        try:
            self.image = pygame.image.load('images/alien.png')
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))
        
        self.rect = self.image.get_rect()

        # Start each new alien at a random position at top of screen
        if x_pos is not None:
            self.rect.x = x_pos
        else:
            self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        
        self.rect.y = -self.rect.height  # Start above screen
        self.y = float(self.rect.y)
        
        # Formation aliens move faster
        self.speed = self.settings.alien_speed * (1.5 if in_formation else 1.0)
        self.health = 1

    def update(self):
        """Move the alien downward."""
        self.y += self.speed
        self.rect.y = self.y
        
        # Remove alien if it goes off bottom of screen
        if self.rect.top > self.screen.get_rect().height:
            self.kill()