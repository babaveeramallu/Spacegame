import pygame
import random
from datetime import datetime, timedelta

class AlienTimer:
    """A class to manage random alien generation timing"""
    
    def __init__(self):
        self.last_alien_time = datetime.now()
        self.next_alien_delay = random.randint(2000, 4000)  # milliseconds between 1-3 seconds
        
    def should_create_alien(self):
        """Check if it's time to create a new alien"""
        current_time = datetime.now()
        time_since_last = current_time - self.last_alien_time
        if time_since_last > timedelta(milliseconds=self.next_alien_delay):
            self.last_alien_time = current_time
            self.next_alien_delay = random.randint(1000, 3000)  # new random delay
            return True
        return False