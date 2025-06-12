import pygame.font
import pygame
 
class Button:
 
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 250, 60
        self.button_color = (0, 100, 200)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Arial', 48)
        
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Add button border
        self.border_rect = pygame.Rect(0, 0, self.width + 10, self.height + 10)
        self.border_rect.center = self.screen_rect.center
        self.border_color = (255, 255, 255)
        
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw button border
        pygame.draw.rect(self.screen, self.border_color, self.border_rect, border_radius=10)
        # Draw button
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=8)
        # Draw text
        self.screen.blit(self.msg_image, self.msg_image_rect)