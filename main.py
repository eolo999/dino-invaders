#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import pygame
from pygame.locals import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("Dinos")
        #self.clock = pygame.time.Clock()

        self.game_font = pygame.font.Font(os.path.join("fonts", "04b_25__.ttf"), 36)
        self.background = pygame.image.load('images/background_rex.png').convert()
        self.intro_sound = pygame.mixer.Sound('sounds/intro.wav')
        self.move_sound = pygame.mixer.Sound('sounds/fiu.ogg')
        self.dino = pygame.image.load('images/tyrannosaurus_rex.png').convert_alpha()

        self.dino_rect = self.dino.get_rect(
                center=(
                    SCREEN_WIDTH - (self.dino.get_width() / 2),
                    SCREEN_HEIGHT / 2))

    def intro(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.game_font.render("Loading....", 0, ((176, 0, 0))),
                (270, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        self.intro_sound.play()
        pygame.time.wait(7000)
        self.start_background()
        pygame.time.wait(8000)
        self.start_dino()
        pygame.time.wait(7000)

    def start_background(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()

    def start_dino(self):
        self.screen.blit(self.dino, self.dino_rect)
        pygame.display.update()


    def move(self, direction, surface):
        if direction == 'left':
            multiplier = -1
        else:
            multiplier = 1
        self.dino_rect = self.dino_rect.move(0, 20 * multiplier)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.dino, self.dino_rect)
        pygame.display.update()

    def shutdown(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.game_font.render("Shutdown", 0, ((176, 0, 0))),
                (250, SCREEN_HEIGHT / 2 - 36))
        pygame.display.flip()
        pygame.time.wait(200)
        sys.exit()

if __name__ == '__main__':

    game = Game()
    if sys.argv[1] == '-i':
        game.intro()
    else:
        game.start_background()
        game.start_dino()
    while True:
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                game.shutdown()
            elif event.key == pygame.K_DOWN:
                game.move_sound.play()
                game.move('right', game.dino)
            elif event.key == pygame.K_UP:
                game.move_sound.play()
                game.move('left', game.dino)
            pygame.event.clear()
