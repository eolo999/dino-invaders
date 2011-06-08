#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Dino(object):
    def __init__(self, screen):
        self.screen = screen
        self.dino = pygame.image.load('images/tyrannosaurus_rex.png').convert_alpha()
        self.dino_rect = self.dino.get_rect(center=(
                    SCREEN_WIDTH - (self.dino.get_width() / 2),
                    SCREEN_HEIGHT / 2))

    def draw_dino(self):
        self.screen.blit(self.dino, self.dino_rect)
        pygame.display.update()

    def move(self, direction):
        if direction == 'left':
            multiplier = -1
        else:
            multiplier = 1
        new_rect = self.dino_rect.move(0, 10 * multiplier)
        if not (new_rect.collidepoint(SCREEN_WIDTH - 20, -10) or
                new_rect.collidepoint(SCREEN_WIDTH - 20, SCREEN_HEIGHT + 10)):
            self.dino_rect = new_rect
        self.screen.blit(self.dino, self.dino_rect)
        pygame.display.update()

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
        pygame.time.wait(8000)
        self.dino.draw_dino()
        pygame.time.wait(7000)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()


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

    dino = Dino(screen)
    game = Game(screen, dino)

    try:
        if sys.argv[1] == '-i':
            game.intro()
    except IndexError:
        game.draw_background()
        dino.draw_dino()
    while True:
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                game.shutdown()
            elif event.key == pygame.K_DOWN:
                game.move_sound.play()
                game.draw_background()
                dino.move('right')
            elif event.key == pygame.K_UP:
                game.draw_background()
                game.move_sound.play()
                dino.move('left')
            pygame.event.clear()
