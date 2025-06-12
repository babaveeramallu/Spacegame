import pygame
import os

class GameSounds:
    """A class to manage all game sounds"""
    
    def __init__(self):
        """Initialize sound objects with error handling"""
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
        
        # Initialize with silent sounds if files are missing
        silent_sound = pygame.mixer.Sound(buffer=bytearray(44))
        
        # Laser sound
        try:
            self.laser = pygame.mixer.Sound('sounds/laser.wav')
            self.laser.set_volume(0.3)
        except:
            self.laser = silent_sound
            print("Note: laser.wav not found - using silent sound")
        
        # Explosion sound
        try:
            self.explosion = pygame.mixer.Sound('sounds/explosion.wav')
            self.explosion.set_volume(0.4)
        except:
            self.explosion = silent_sound
            print("Note: explosion.wav not found - using silent sound")
        
        # Game over sound
        try:
            self.game_over = pygame.mixer.Sound('sounds/game_over.wav')
            self.game_over.set_volume(0.5)
        except:
            self.game_over = silent_sound
            print("Note: game_over.wav not found - using silent sound")
        
        # Reload sound
        try:
            self.reload = pygame.mixer.Sound('sounds/reload.wav')
            self.reload.set_volume(0.3)
        except:
            self.reload = silent_sound
            print("Note: reload.wav not found - using silent sound")
        
        # Level up sound
        try:
            self.level_up = pygame.mixer.Sound('sounds/level_up.wav')
            self.level_up.set_volume(0.4)
        except:
            self.level_up = silent_sound
            print("Note: level_up.wav not found - using silent sound")
        
        # Background music
        try:
            pygame.mixer.music.load('sounds/background.mp3')
            pygame.mixer.music.set_volume(0.2)
        except:
            print("Note: background.mp3 not found - no background music")
    
    def play_background(self):
        """Play background music in loop if available"""
        if pygame.mixer.music.get_busy():
            return
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
    
    def stop_background(self):
        """Stop background music"""
        pygame.mixer.music.stop()