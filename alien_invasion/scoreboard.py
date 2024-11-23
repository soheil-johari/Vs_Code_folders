import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (130, 130, 30)
        self.symbol_color = (50, 145, 78)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendred image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        symbol = "Score" f"  {score_str}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color)
        self.score_symbol = self.font.render(symbol, True,
                                             self.symbol_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

        # Display score symbol
        self.score_symbol_rect = self.score_symbol.get_rect()
        self.score_symbol_rect.right = self.score_rect.right
        self.score_symbol_rect.top = self.score_rect.top

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        high_score_symbol = "Top Score"  f"  {high_score_str}"

        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color)
        self.high_score_symbol = self.font.render(high_score_symbol, True,
                                                  self.symbol_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

        # Center the high score symbol at the centery of the high score number
        self.high_score_symbol_rect = self.high_score_symbol.get_rect()
        self.high_score_symbol_rect.right = self.high_score_rect.right
        self.high_score_symbol_rect.top = self.high_score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color)
        level_symbol = "Level"
        self.level_symbol = self.font.render(level_symbol, True,
                                             self.symbol_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

        # Position the level symbol righ the level number.
        self.level_symbol_rect = self.level_symbol.get_rect()
        self.level_symbol_rect.right = self.level_rect.right - 30
        self.level_symbol_rect.top = self.level_symbol_rect.bottom + 30

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw scores, level, and ships to the sceen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.score_symbol, self.score_symbol_rect)
        self.screen.blit(self.high_score_symbol, self.high_score_symbol_rect)
        self.screen.blit(self.level_symbol, self.level_symbol_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
