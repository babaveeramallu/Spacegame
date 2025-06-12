import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to manage explosion animations"""
    
    def __init__(self, ai_game, center):
        super().__init__()
        self.screen = ai_game.screen
        
        # Load explosion images (fallback to rectangle if images not found)
        try:
            self.image = pygame.image.load('images/explosion.png')
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # milliseconds between frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame > 8:  # Number of frames to display
                self.kill()