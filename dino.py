import sys
import os

from random import choice, randint

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Projectiles(pygame.sprite.Group):
    def __init__(self):
        super(Projectiles, self).__init__()


class Foes(pygame.sprite.Group):
    def __init__(self):
        super(Foes, self).__init__()


class FoeProjectile(pygame.sprite.Sprite):
    def __init__(self):
        super(FoeProjectile, self).__init__()
        self.fire_sound = pygame.mixer.Sound('sounds/roar.ogg')
        self.image = pygame.image.load('images/invader_bullet.png')
        self.rect = self.image.get_rect()

    def fire(self, screen, foe_rect):
        self.fire_sound.play()
        self.rect = self.image.get_rect(center=(foe_rect.centerx ,
            foe_rect.bottom + 10))
        screen.blit(self.image, self.rect)

    def move(self, screen):
        new_rect = self.rect.move(0, 2)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect
            screen.blit(self.image, self.rect)
        else:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.fire_sound = pygame.mixer.Sound('sounds/roar.ogg')
        self.image = pygame.image.load('images/burn.png')
        self.rect = self.image.get_rect()

    def fire(self, screen, dino_rect):
        self.fire_sound.play()
        self.rect = self.image.get_rect(center=(dino_rect.centerx - 16, dino_rect.top - 10))
        screen.blit(self.image, self.rect)

    def move(self, screen):
        new_rect = self.rect.move(0, -10)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect
            screen.blit(self.image, self.rect)
        else:
            self.kill()


class Foe(pygame.sprite.Sprite):
    def __init__(self, path=None, center=None, speed=1, direction=1):
        super(Foe, self).__init__()
        if path is None:
            path = os.path.join('images', choice(FOES))
        self.image = pygame.image.load(path).convert_alpha()
        if center is None:
            center = (randint(32, SCREEN_WIDTH - 24), randint(16, SCREEN_HEIGHT - 130))
        else:
            self.rect = self.image.get_rect(center=center)

        self.projectiles = Projectiles()
        self.fire_power = 1
        self.speed = speed
        self.direction = direction

    def move(self, screen):
        new_rect = self.rect.move(self.direction * 5 * self.speed, 0)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect
        else:
            self.direction *= -1
            self.rect = self.rect.move(0, 32)

    def fire(self, screen):
        if randint(1,100) == 100 and len(self.projectiles) < self.fire_power:
            projectile = FoeProjectile()
            projectile.add(self.projectiles)
            projectile.fire(screen, self.rect)


class Level(object):
    def __init__(self, number):
        self.foes = Foes()
        if number == 1:
            x_multiplier = SCREEN_WIDTH / 10
            foe_image_path = 'images/pterodactyl32.png'
            for n in range(1, 10):
                foe = Foe(foe_image_path, (n * x_multiplier, 96), 2)
                foe.add(self.foes)
                foe = Foe(foe_image_path, (n * x_multiplier, 128), 2, -1)
                foe.add(self.foes)
            foe_image_path = 'images/brontosaurus32.png'
            for n in range(1, 10):
                foe = Foe(foe_image_path, (n * x_multiplier, 192), 1)
                foe.add(self.foes)
                foe = Foe(foe_image_path, (n * x_multiplier, 224), 1, -1)
                foe.add(self.foes)

class Game(object):
    def __init__(self):
        self.score = 0
        self.level = Level(1)
        # Load graphics
        self.game_font = pygame.font.Font(os.path.join("fonts",
            "04b_25__.ttf"), 24)
        self.background = pygame.image.load('images/background_rex.png').convert()
        # Load sounds
        self.game_sound = pygame.mixer.Sound('sounds/foresta_nera.ogg')
        self.game_sound.set_volume(0.1)
        self.boom_sound = pygame.mixer.Sound('sounds/boom.ogg')
        self.move_sound = pygame.mixer.Sound('sounds/fiu.ogg')
        # Load "Dino"
        self.dino = Dino()
        self.game_sound.play(loops=-1)

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def shutdown(self, screen):
        screen.blit(self.game_font.render("Shutdown", 0, ((176, 0, 0))),
                (250, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        pygame.time.wait(200)
        sys.exit()

    def draw_score(self, screen):
        screen.blit(self.game_font.render(str(self.score), 0, (255, 255,
            255)), (20, 20))

    def over(self, screen):
        screen.blit(self.game_font.render("Game Over", 0, ((176, 0, 0))),
                (250, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        pygame.time.wait(200)
        sys.exit()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        self.dino = pygame.image.load('images/tyrannosaurus_rex64.png').convert_alpha()
        # Set dino starting position to the center of the bottom of the screen
        self.dino_rect = self.dino.get_rect(center=(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT  - (self.dino.get_height() / 2)))
        self.speed = 2
        self.fire_power = 1
        self.can_fire = True
        self.projectiles = Projectiles()

    def draw_dino(self, screen):
        screen.blit(self.dino, self.dino_rect)

    def move(self, screen, direction):
        if direction == 'left':
            multiplier = -1
        else:
            multiplier = 1
        new_rect = self.dino_rect.move(self.speed * 5 * multiplier, 0)
        # assign new position if dino is still inside the screen after moving
        if screen.get_rect().contains(new_rect):
            self.dino_rect = new_rect

    def fire(self, screen):
        if len(self.projectiles) < self.fire_power:
            projectile = Projectile()
            projectile.add(self.projectiles)
            projectile.fire(screen, self.dino_rect)

    def toggle_lock(self):
        self.can_fire = not self.can_fire


def main_loop():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Dinos")
    pygame.key.set_repeat(20, 30)

    game = Game()

    while True:
        pygame.time.wait(20)
        # Input handlers
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    game.shutdown(screen)
                elif event.key == pygame.K_RIGHT:
                    game.dino.move(screen, 'right')
                elif event.key == pygame.K_LEFT:
                    game.dino.move(screen, 'left')
                elif event.key == pygame.K_SPACE:
                    if game.dino.can_fire:
                        game.dino.fire(screen)
                        game.dino.toggle_lock()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game.dino.toggle_lock()
        # Loop operations
        game.draw_background(screen)
        game.draw_score(screen)
        game.dino.draw_dino(screen)
        for foe in game.level.foes:
            foe.move(screen)
            foe.fire(screen)
            if foe.rect.colliderect(game.dino.dino_rect):
                game.over(screen)
        game.level.foes.draw(screen)
        for projectile in game.dino.projectiles:
            projectile.move(screen)
            for foe in game.level.foes:
                if foe.rect.colliderect(projectile.rect):
                    game.boom_sound.play()
                    game.score += 10
                    foe.kill()
                    projectile.kill()
        for foe in game.level.foes:
            for projectile in foe.projectiles:
                projectile.move(screen)
                shrinked_rect = game.dino.dino_rect.inflate(-40, -40)
                if shrinked_rect.colliderect(projectile.rect):
                    print shrinked_rect
                    print game.dino.dino_rect
                    game.boom_sound.play()
                    projectile.kill()
                    game.over(screen)
                                                                                                    
        pygame.display.update()

if __name__ == '__main__':
    main_loop()
