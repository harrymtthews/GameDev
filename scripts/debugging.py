# Classes related to debugging the game
import pygame
from scripts.constants import *
from scripts.sprites import SpriteABC

class FPS(SpriteABC):

    def __init__(self, *groups):
        super(FPS, self).__init__(groups)
        self.image = self.font_small.render('00', True, COLOURS['green'])
        self.rect = self.image.get_rect(topleft=(10,10))

    def update(self, dt, *args, **kwargs):
        if dt > 0:
            self.image = self.font_small.render(str(1000 / dt).split('.')[0], True, COLOURS['green'])