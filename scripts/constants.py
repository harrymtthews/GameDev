# All of the constants required for the game.
import pygame

COLOURS = {
    'black': (0, 0, 0, 255),
    'white': (255, 255, 255, 255),
    'green': (0, 255, 0, 255),
    'red': (255, 0, 0, 255),
    'transparent': (0, 0, 0, 0),
    'half-grey': (127, 127, 127, 127),
    'half-dark-grey': (94, 94, 94, 127),
    'dark-grey': (28, 28, 28, 240),
    'mandarin': (229, 122, 68, 255),
    'main': (119, 2, 2, 255),
    'main-half': (119, 2, 2, 127),
    'highlight-1': (89, 1, 1, 255),
    'highlight-1-half': (89, 1, 1, 127),
    'highlight-2': (149, 3, 3, 255),
    'highlight-2-half': (149, 3, 3, 127),
    'text': (255, 177, 81, 255),
    'text-light': (252, 231, 204, 255)
}

SCREENSIZE = (1920, 1200)

TYPEFACE = pygame.font.get_default_font()

NUM_CARDS = 4

UPDATE_FREQUENT = pygame.USEREVENT + 1
SCENE_LOAD = pygame.USEREVENT + 2
CREATE_SPRITE = pygame.USEREVENT + 3
KILL_SPRITE = pygame.USEREVENT + 4
INTERACT_TIMER = pygame.USEREVENT + 5
COLLECT_CARD = pygame.USEREVENT + 6
PICKUP_TP = pygame.USEREVENT + 7
USE_VENDING = pygame.USEREVENT + 8
PICK_CATEGORY = pygame.USEREVENT + 9
UPDATE_INFREQUENT = pygame.USEREVENT + 10
CHANGE_DIFFICULTY = pygame.USEREVENT + 11
