import sys
from time import sleep


import pygame

from alien1 import Settings, Space_image
from game_state import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from Alien_fleet import Alien, HalfAlien
from stars import Star


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height
        ))

        pygame.display.set_caption("Soheil alien")

        # Create an instance to store game statistics,
        #  and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.space = Space_image(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.h_aliens = pygame.sprite.Group()
        self._create_fleet()
        self._create_half_fleet()
        self._create_star()

        # Make the play button.
        self.play_button = Button(self, "Play bitch")

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_half_aliens()
                self._update_stars()
            self._update_screen()

    def _check_events(self):
        """Responding to keypresses and mouse events."""
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _start_game(self):
        """start a new game."""
        # Reset the game statisticks.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaing aliens and bullets.
        self.aliens.empty()
        self.h_aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self._create_half_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet =  Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disapoeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        collisions1 = pygame.sprite.groupcollide(
            self.bullets, self.h_aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if collisions1:
            for aliens in collisions1.values():
                self.stats.score += self.settings.half_alien_point * \
                    len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.h_aliens:
         # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_half_fleet()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()            
            

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:

            # Decrement ships_left, and update scoreboard.
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.h_aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_half_fleet()
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaliable_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height -
                             (2 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _create_half_fleet(self):
        """Create the fleet of half aliens."""
        half_alien = HalfAlien(self)
        h_alien_width, h_alien_height = half_alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * h_alien_width)
        number_aliens_x = avaliable_space_x // (2 * h_alien_width)

        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height -
                             (2 * 75) - ship_height)
        number_rows = avaliable_space_y // (2 * 75)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_half_alien(alien_number, row_number)

    def _create_half_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        h_alien = HalfAlien(self)
        h_alien_width, h_alien_height = h_alien.rect.size
        h_alien.x = h_alien_width + 2 * h_alien_width * alien_number
        h_alien.rect.x = h_alien.x
        h_alien.y = 115 + 2 * 75 * row_number
        h_alien.rect.y = h_alien.y
        self.h_aliens.add(h_alien)

    def _create_star(self):
        """Create the star of space."""
        star = Star(self)
        star_width, star_height = star.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * star_width)
        number_stars_x = avaliable_space_x // (3 * star_width)

        # Determine the number of rows of star that fit on the screen.
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height -
                             (4 * star_height) - ship_height)
        number_rows = avaliable_space_y // (2 * star_height)

        # Create the full space of star.
        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_space_star(star_number, row_number)

    def _create_space_star(self, star_number, row_number):
        """Create an star and place it in the row."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 3 * star_width * star_number
        star.rect.x = star.x
        star.y = star.rect.height + 2 * star.rect.height * row_number
        star.rect.y = star.y
        self.stars.add(star)

    def _check_half_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.h_aliens:
            if alien.check_edges():
                self._change_half_fleet_direction()
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _change_half_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.h_aliens.sprites():
            alien.rect.y += self.settings.half_fleet_drop_speed
        self.settings.half_fleet_direction *= -1

    def _check_star_edges(self):
        """Respond appropriately if any stars have reached an edge."""
        for star in self.stars.sprites():
            if star.check_edges():
                self._change_star_direction()
                break

    def _change_star_direction(self):
        """Drop the entire star and change the star's direction."""
        for star in self.stars.sprites():
            star.rect.y += self.settings.stars_drop_speed
        self.settings.stars_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.space.draw_bg()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.stars.draw(self.screen)
        self.aliens.draw(self.screen)
        self.h_aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()
        self.ship.blitme()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _update_aliens(self):
        """
        check if the fleet is at an edge,
          then update the position of all aliens in the fleet.
        """
        self.aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_half_aliens(self):
        """
        check if the fleet is at an edge,
          then update the position of all aliens in the fleet.
        """
        self._check_half_fleet_edges()
        self.h_aliens.update()

        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.h_aliens):
            print("Ship hit!!!")
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_stars(self):
        """
        chack if the stars is at an edge,
          then update the position of all stars in the space.
        """
        self._check_star_edges()
        self.stars.update()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    print("Running the game...")
    ai = AlienInvasion()
    #sleep(3)
    ai.run_game()
