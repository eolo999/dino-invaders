#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from random import choice, randint

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

FOES = ['brontosaurus32.png',
        'pterodactyl32.png',
        'stegosaurus32.png',
        'triceratops32.png',
        'tyrannosaurus_rex32.png']

NUM_FOES = 32


class Foes(pygame.sprite.Group):
    def __init__(self):
        super(Foes, self).__init__()


class Foe(pygame.sprite.Sprite):
    def __init__(self, path=None, center=None):
        super(Foe, self).__init__()
        if path is None:
            path = os.path.join('images', choice(FOES))
        self.image = pygame.image.load(path).convert_alpha()
        if center is None:
            self.rect = self.image.get_rect(center=(
                randint(32, SCREEN_WIDTH - 24),
                randint(16, SCREEN_HEIGHT - 130)))
        else:
            self.rect = self.image.get_rect(center=center)

        self.direction = 1

    def move(self, screen):
        new_rect = self.rect.move(self.direction * 5, 0)
        if screen.get_rect().contains(new_rect):
            self.rect = new_rect
        else:
            self.direction *= -1
            self.rect = self.rect.move(0, 5)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        super(Projectile, self).__init__()
        self.screen_rect = self.screen.get_rect()
        self.fire_sound = pygame.mixer.Sound('sounds/click.wav')
        self.image = pygame.image.load('images/burn.png')
        self.rect = self.image.get_rect()
        self.firing = False

    def fire(self, dino_rect):
        if not self.firing:
            self.firing = True
            self.fire_sound.play()
            self.rect = self.image.get_rect(center=(dino_rect.centerx - 16, dino_rect.top - 10))
            self.screen.blit(self.image, self.rect)

    def move(self):
        new_rect = self.rect.move(0, -10)
        if self.screen_rect.contains(new_rect):
            self.rect = new_rect
            self.screen.blit(self.image, self.rect)
        else:
            self.firing = False

    def destroy(self):
        self.firing = False


class Dino(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.dino = pygame.image.load('images/tyrannosaurus_rex64.png').convert_alpha()
        # Set dino starting position to the center of the bottom of the screen
        self.dino_rect = self.dino.get_rect(center=(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT  - (self.dino.get_height() / 2)))
        self.projectile = Projectile(screen)

    def draw_dino(self):
        self.screen.blit(self.dino, self.dino_rect)

    def move(self, direction):
        if direction == 'left':
            multiplier = -1
        else:
            multiplier = 1
        new_rect = self.dino_rect.move(10 * multiplier, 0)
        # assign new position if dino is still inside the screen after moving
        if self.screen_rect.contains(new_rect):
            self.dino_rect = new_rect

    def fire(self):
        self.projectile.fire(self.dino_rect)

class Game(object):
    def __init__(self, screen, dino):

        self.screen = screen
        self.score = 0
        self.game_font = pygame.font.Font(os.path.join("fonts",
            "04b_25__.ttf"), 24)
        self.background = pygame.image.load('images/background_rex.png').convert()
        self.dino = dino
        self.game_sound = pygame.mixer.Sound('sounds/intro.wav')
        self.game_sound.set_volume(0.1)
        self.intro_sound = pygame.mixer.Sound('sounds/intro.wav')
        self.boom_sound = pygame.mixer.Sound('sounds/destroyed.wav')
        self.move_sound = pygame.mixer.Sound('sounds/fiu.ogg')

    def intro(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.game_font.render("Loading....", 0, ((176, 0, 0))),
                (270, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        self.intro_sound.play()
        pygame.time.wait(7000)
        self.draw_background()
        pygame.display.update()
        pygame.time.wait(8000)
        self.dino.draw_dino()
        pygame.display.update()
        pygame.time.wait(7000)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def shutdown(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.game_font.render("Shutdown", 0, ((176, 0, 0))),
                (250, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        pygame.time.wait(200)
        sys.exit()

    def draw_score(self):
        self.screen.blit(self.game_font.render(str(self.score), 0, (255, 255,
            255)), (20, 20))

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Dinos")
    pygame.key.set_repeat(20, 20)

    dino = Dino(screen)
    game = Game(screen, dino)
    game.game_sound.play(loops=-1)
    foes = Foes()

    for n in range(NUM_FOES):
        foe = Foe()
        foe.add(foes)

    try:
        if sys.argv[1] == '-i':
            game.intro()
    except IndexError:
        pass
    while len(foes) > 0:
        pygame.time.wait(20)
        # Input handlers
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    game.shutdown()
                elif event.key == pygame.K_RIGHT:
                    dino.move('right')
                elif event.key == pygame.K_LEFT:
                    dino.move('left')
                elif event.key == pygame.K_SPACE:
                    dino.fire()
        # Loop operations
        game.draw_background()
        game.draw_score()
        for foe in foes:
            foe.move(screen)
        foes.draw(screen)
        dino.draw_dino()
        if dino.projectile.firing:
            dino.projectile.move()
        for foe in foes:
            if foe.rect.colliderect(dino.projectile.rect):
                game.boom_sound.play()
                game.score += 10
                foe.kill()
                dino.projectile.destroy()
        pygame.display.update()
    game.shutdown()
