import sys
from time import time
import pygame
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from alien_timer_functions import AlienTimer
from sounds import GameSounds

class Star:
    """A class to represent a star in the background."""

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.x = random.randint(0, settings.screen_width)
        self.y = random.randint(0, settings.screen_height)
        self.speed = random.uniform(0.5, 1.5)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > self.settings.screen_height:
            self.y = 0
            self.x = random.randint(0, self.settings.screen_width)

    def draw(self):
        pygame.draw.circle(self.screen, (199, 177, 109), (int(self.x), int(self.y)), self.size)

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion Extreme")

        # Create dynamic stars
        self.stars = [Star(self.screen, self.settings) for _ in range(100)]

        # Create game components
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sounds = GameSounds()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.alien_timer = AlienTimer()
        self.play_button = Button(self, "Play")

        # Game state variables  
        self.bullets_fired = 0
        self.reloading = False
        self.reload_start = 0
        self.formation_active = False
        self.formation_time = 0
        self.alien_breach_time = None
        self.breach_timeout = 3

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._create_aliens()
                self._update_explosions()

            self._update_screen()

    def _check_events(self):
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
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        self.explosions.empty()
        self.bullets_fired = 0
        self.reloading = False
        self.formation_active = False
        self.alien_breach_time = None
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
        self.sounds.play_background()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if self.reloading:
            return

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.laser.play()
            self.bullets_fired += 1

            if self.bullets_fired >= self.settings.bullets_allowed:
                self._start_reload()

    def _start_reload(self):
        self.reloading = True
        self.reload_start = time()
        self.sounds.reload.play()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)

        if collisions:
            for aliens_hit in collisions.values():
                for alien in aliens_hit:
                    alien.health -= 1
                    if alien.health <= 0:
                        self._create_explosion(alien)
                        alien.kill()
                        self.stats.score += self.settings.alien_points

            self.sb.prep_score()
            self.sb.check_high_score()

            if not self.aliens and not self.formation_active:
                self._start_new_level()

        if self.reloading and time() - self.reload_start >= self.settings.reload_time:
            self.reloading = False
            self.bullets_fired = 0

    def _create_explosion(self, alien):
        explosion = Explosion(self, alien.rect.center)
        self.explosions.add(explosion)
        self.sounds.explosion.set_volume(1.0)
        self.sounds.explosion.play()

    def _update_aliens(self):
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

        if self.alien_breach_time:
            if not self.aliens:
                self.alien_breach_time = None
            elif time() - self.alien_breach_time >= self.breach_timeout:
                self._ship_hit()
                self.alien_breach_time = None

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.explosions.empty()
            self.ship.center_ship()
            pygame.time.delay(500)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sounds.stop_background()
            self.sounds.game_over.play()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                if self.alien_breach_time is None:
                    self.alien_breach_time = time()

    def _create_aliens(self):
        current_time = time()
        if (not self.formation_active and random.random() < self.settings.formation_chance):
            self._create_formation()
            self.formation_active = True
            self.formation_time = current_time
        elif self.alien_timer.should_create_alien() and not self.formation_active:
            self.aliens.add(Alien(self))

        if self.formation_active and current_time - self.formation_time > 5:
            self.formation_active = False

    def _create_formation(self):
        num_aliens = random.randint(self.settings.formation_size_min, self.settings.formation_size_max)
        spacing = self.settings.screen_width // (num_aliens + 1)

        for i in range(1, num_aliens + 1):
            self.aliens.add(Alien(self, i * spacing, True))

    def _start_new_level(self):
        self.stats.level += 1
        self.sb.prep_level()
        self.settings.increase_speed()
        self.sounds.level_up.play()

    def _update_explosions(self):
        self.explosions.update()

    def _update_screen(self):
        self.screen.fill((0, 0, 30))

        for star in self.stars:
            star.update()
            star.draw()

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        self.sb.show_score()

        if self.reloading:
            reload_progress = (time() - self.reload_start) / self.settings.reload_time
            bar_width = 200
            pygame.draw.rect(self.screen, (255, 0, 0),
                (self.settings.screen_width//2 - bar_width//2, 10,
                 bar_width * reload_progress, 20))

        bullets_left = self.settings.bullets_allowed - self.bullets_fired
        font = pygame.font.SysFont(None, 36)
        bullet_text = font.render(f"Bullets: {bullets_left}", True, (255, 255, 255))
        self.screen.blit(bullet_text, (10, 10))

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()