import pygame


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        self.ship_limit = 3
        # Bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (100, 240, 40)
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 6
        self.half_fleet_drop_speed = 6

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Star settings
        self.star_speed = 0.2
        self.stars_drop_speed = 6
        # stars_drop_speed of 1 represents right; -1 represent left.
        self.stars_direction = 1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 0.7
        self.bullet_speed = 1.0
        self.alien_speed = 0.6

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.half_fleet_direction = 1

        # Scoring
        self.alien_points = 50
        self.half_alien_point = 25

    def increase_speed(self):
        """Initialize speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        self.half_alien_point = int(self.half_alien_point * self.score_scale)


class Space_image:
    """filling the background by image"""

    def __init__(self, ai_game):
        """Initialize the game image background."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load("space_image.jpg")
        self.rect = self.image.get_rect()

    def draw_bg(self):
        """Initialize background"""
        self.screen.blit(self.image, self.rect)
