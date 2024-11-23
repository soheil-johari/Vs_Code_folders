import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a single star in the space."""

    def __init__(self, ai_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the star image and set its rect attributes.
        self.image = pygame.image.load("star.png").convert_alpha()
        self.rect = self.image.get_rect()

        # Start each new alien near the top right of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the star's exact horizental position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retirn True if star is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the star to the left."""
        self.x -= (self.settings.star_speed * 
                   self.settings.stars_direction)
        self.rect.x = self.x
