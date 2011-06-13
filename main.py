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


class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.bullet = pygame.image.load('images/burn.png')

    def fire(self, dino_rect):
        return self.bullet.get_rect(center=(dino_rect.centerx - 16, dino_rect.top - 10))

class Foe(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        path = os.path.join('images', choice(FOES))
        self.foe = pygame.image.load(path).convert_alpha()
        self.foe_rect = self.foe.get_rect(center=(
            randint(16, SCREEN_WIDTH - 8),
            randint(16, SCREEN_HEIGHT - 130)))

    def draw_foe(self):
        self.screen.blit(self.foe, self.foe_rect)


class Dino(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.dino = pygame.image.load('images/tyrannosaurus_rex64.png').convert_alpha()
        # Set dino starting position to the center of the bottom of the screen
        self.dino_rect = self.dino.get_rect(center=(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT  - (self.dino.get_height() / 2)))
        self.state = 'still'
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
        self.state == 'moving'
        self.screen.blit(self.dino, self.dino_rect)

    def fire(self):
        self.screen.blit(self.dino, self.dino_rect)
        self.screen.blit(self.projectile.bullet, self.projectile.fire(self.dino_rect))

class Game(object):
    def __init__(self, screen, dino):

        self.screen = screen
        self.game_font = pygame.font.Font(os.path.join("fonts", "04b_25__.ttf"), 36)
        self.background = pygame.image.load('images/background_rex.png').convert()
        self.dino = dino
        self.intro_sound = pygame.mixer.Sound('sounds/intro.wav')
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

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Dinos")
    pygame.key.set_repeat(20, 100)

    dino = Dino(screen)
    game = Game(screen, dino)
    foes = []

    for n in range(NUM_FOES):
        foe = Foe(screen)
        foes.append(foe)

    try:
        if sys.argv[1] == '-i':
            game.intro()
    except IndexError:
        game.draw_background()
        dino.draw_dino()
        [foe.draw_foe() for foe in foes]
        pygame.display.update()
    while True:
        #pygame.time.delay(20)
        pygame.time.wait(20)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    game.shutdown()
                elif event.key == pygame.K_RIGHT:
                    game.move_sound.play()
                    game.draw_background()
                    [foe.draw_foe() for foe in foes]
                    dino.move('right')
                    pygame.display.update()
                elif event.key == pygame.K_LEFT:
                    game.move_sound.play()
                    game.draw_background()
                    [foe.draw_foe() for foe in foes]
                    dino.move('left')
                    pygame.display.update()
                elif event.key == pygame.K_SPACE:
                    #game.fire_sound.play()
                    game.draw_background()
                    [foe.draw_foe() for foe in foes]
                    dino.fire()
                    pygame.display.update()
            #pygame.event.pump()
        #    pygame.event.clear()
