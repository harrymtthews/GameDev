import pygame
from scripts.sprites import *
from scripts.constants import *
from scripts.debugging import *
pygame.init()

# Structured class for storing the information of a sprite.
class SpriteInfo():

    def __init__(self, s, p, k):
        self.sprite = s
        self.params = p
        self.kill = k

# Contains all of the information required for one scene.
class Scene():

    def __init__(self, num, player, static, ppos = None):
        self.number = num
        self.player_sprites = player
        self.static_sprites = static
        self.player_pos = ppos


SCENES = [Scene(num=0,
                player=None,
                static=[SpriteInfo(Sprite, (0, 0, 0, SCREENSIZE[0], SCREENSIZE[1], COLOURS['white'], 'resources/mcs_2.png'), 0),
                        SpriteInfo(Sprite, (100, 288, 1, 451, 270, COLOURS['half-dark-grey']), 0),
                        SpriteInfo(Text, (100, 170, 3, 30, COLOURS['highlight-1-half'], COLOURS['text'], 'Degree Hunter', False), 0),
                        SpriteInfo(TextButton, (100, 280+50, 3, 10, COLOURS['transparent'], COLOURS['text'], 'Play', True, pygame.event.Event(SCENE_LOAD,{'scene':2})), 0),
                        SpriteInfo(TextButton, (100, 350+50, 3, 10, COLOURS['transparent'], COLOURS['text'], 'Settings', True, pygame.event.Event(SCENE_LOAD,{'scene':1})), 0),
                        SpriteInfo(TextButton, (100, 420+50, 3, 10, COLOURS['transparent'], COLOURS['text'], 'Quit', True, pygame.event.Event(pygame.QUIT)), 0)]
                ),
          Scene(num=1,
                player=None,
                static=[SpriteInfo(Sprite, (0, 0, 0, SCREENSIZE[0], SCREENSIZE[1], COLOURS['white'], 'resources/mcs_2.png'), 0),
                        SpriteInfo(Sprite, (510, 150, 1, 900, 780, COLOURS['half-dark-grey']), 0),
                        SpriteInfo(VolumeSlider, (400, 2), 0),
                        SpriteInfo(Text, (902, 350, 2, 5, COLOURS['transparent'], COLOURS['text'], 'Volume', True), 0),
                        SpriteInfo(Text, (810, 185, 2, 30, COLOURS['highlight-1-half'], COLOURS['text'], 'Settings', False), 0),
                        SpriteInfo(Text, (896, 640-125, 2, 5, COLOURS['transparent'], COLOURS['text'], 'Difficulty', True), 0),
                        SpriteInfo(TextButton, (510+190, 700-125, 3, 20, COLOURS['transparent'], COLOURS['text'], 'Easy', True, pygame.event.Event(CHANGE_DIFFICULTY,{'mode':'easy'})), 0),
                        SpriteInfo(TextButton, (700+190, 700-125, 3, 20, COLOURS['transparent'], COLOURS['text'], 'Normal', True, pygame.event.Event(CHANGE_DIFFICULTY,{'mode':'normal'})), 0),
                        SpriteInfo(TextButton, (932+190, 700-125, 3, 20, COLOURS['transparent'], COLOURS['text'], 'Hard', True, pygame.event.Event(CHANGE_DIFFICULTY,{'mode':'hard'})), 0),
                        SpriteInfo(TextButton, (510, 862, 3, 20, COLOURS['transparent'], COLOURS['text'], 'Back', True, pygame.event.Event(SCENE_LOAD,{'scene':0})), 0)]
                ),
          Scene(num=2,
                player=[SpriteInfo(Sprite, (0, 0, 0, 1920, 2160, COLOURS['black'], 'resources/bckg1.png'), 0),
                        # Map Borders
                        SpriteInfo(Sprite, (1872, 0, 1, 5, 2160, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (0, 0, 1, 1920, 5, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (4, 0, 1, 5, 2160, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (13, 2151, 1, 1900, 5, COLOURS['transparent']), 0),
                        # Walls and floors
                        SpriteInfo(Sprite, (218, 0, 1, 973, 207, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (1740, 142, 1, 132, 251, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (210, 386, 1, 31, 692, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (5, 1080, 1, 416, 405, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (421, 1080, 1, 206, 597, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (627, 1080, 1, 594, 23, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (1221, 1080, 1, 310, 597, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (237, 1989, 1, 201, 9, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (422, 1677, 1, 16, 322, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (437, 1948, 1, 190, 14, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (612, 1792, 1, 15, 169, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (241, 816, 1, 956, 8, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (442, 386, 1, 742, 8, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (1184, 386, 1, 8, 309, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (742, 596, 1, 8, 226, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (742, 595, 1, 444, 8, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (742, 595, 1, 211, 120, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (826, 1940, 1, 582, 23, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (826, 1894, 1, 24, 47, COLOURS['transparent']), 0),
                        SpriteInfo(Sprite, (1386, 1894, 1, 24, 47, COLOURS['transparent']), 0),
                        # Chairs and tables
                        SpriteInfo(Sprite, (891, 1811, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_g.png'), 0),
                        SpriteInfo(Sprite, (980, 1813, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (1105, 1813, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (1230, 1811, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_g.png'), 0),
                        SpriteInfo(Sprite, (302, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_o.png'), 0),
                        SpriteInfo(Sprite, (382, 942, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (522, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_o.png'), 0),
                        SpriteInfo(Sprite,(350+302, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_o.png'), 0),
                        SpriteInfo(Sprite, (350+382, 942, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (350+522, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_o.png'), 0),
                        SpriteInfo(Sprite, (700+302, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_o.png'), 0),
                        SpriteInfo(Sprite, (700+382, 942, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite,  (700+522, 940, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_o.png'), 0),
                        SpriteInfo(Sprite, (666, 1159, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_g.png'), 0),
                        SpriteInfo(Sprite, (746, 1161, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (886, 1159, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_o.png'), 0),
                        SpriteInfo(Sprite, (666+220, 1159+300, 1, 68, 140, COLOURS['transparent'], 'resources/chair_right_o.png'), 0),
                        SpriteInfo(Sprite, (746+220, 1161+300, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (886+220, 1159+300, 1, 68, 140, COLOURS['transparent'], 'resources/chair_left_o.png'), 0),
                        SpriteInfo(Sprite, (258, 580, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (425, 667, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        SpriteInfo(Sprite, (598, 586, 1, 120, 124, COLOURS['transparent'], 'resources/table.png'), 0),
                        # Desks
                        SpriteInfo(Sprite, (100, 1510, 1, 84, 340, COLOURS['transparent'], 'resources/longdesk.png'), 0),
                        SpriteInfo(Sprite, (320, 1620, 1, 64, 170, COLOURS['transparent'], 'resources/shortdesk.png'), 0),
                        SpriteInfo(Sprite, (1594, 560, 1, 84, 340, COLOURS['transparent'], 'resources/longdesk.png'), 0),
                        # Other
                        SpriteInfo(Sprite, (754, 607, 1, 64, 64, COLOURS['transparent'], 'resources/Toilet.png'), 0),
                        SpriteInfo(Sprite, (871, 609, 1, 64, 64, COLOURS['transparent'], 'resources/Toilet.png'), 0),
                        SpriteInfo(Tp, (38, 1014, 1, 48, 48, 'resources/TP.png'), 0),
                        # NPC
                        SpriteInfo(NPC, (1742, 1, 1, 'resources/Vending.png', 'Vending Machine', 'BRRRRR BRRR BRRRRRRRRR *DONK*', 1, pygame.event.Event(USE_VENDING)), 0),
                        SpriteInfo(NPC, (518, 1788, 0, 'resources/mandy.png', 'Mandy', 'I don\'t get paid enough for this,  I\'m going on strike.'), 0),
                        SpriteInfo(NPC, (325, 1690, 1, 'resources/li.png', 'Frederick', 'I\'ll give you a degree, but only if you can beat me at Computer Sceince top trumps! Go get some cards and come back to me.', 0, pygame.event.Event(SCENE_LOAD, {'scene':3})), 0),
                        SpriteInfo(NPC, (54, 19, 1, 'resources/JasonStatham.png', 'Jason Statham', 'Being an action star is hungry work, I could do with a snack.', 0, pygame.event.Event(COLLECT_CARD, {'ID':2})), 0),
                        SpriteInfo(NPC, (1068, 1150, 1, 'resources/Girl.png', 'Ellie', 'What\'s up with the colour of these chairs?'), 0),
                        SpriteInfo(NPC, (839, 585, 2, 'resources/Nerd.png', 'Johnny', 'Umm this is awkward... I\'ve run out of toilet paper, can you get some for me?', 0, pygame.event.Event(COLLECT_CARD, {'ID':3})), 0),
                        SpriteInfo(NPC, (990, 414, 1, 'resources/Dude.png', 'Buck', 'Are you meant to be in this class?'), 0),
                        # Cards
                        SpriteInfo(Card2D, (148, 1517, 2, 0), 0),
                        SpriteInfo(Card2D, (276, 594, 2, 1), 0)],
                static=[SpriteInfo(CardCounter, [0], 0)],
                ppos={0:(1615, 2045, 1), 3:(244, 1845, 1)}
                ),
          Scene(num=3,
                player=None,
                static=[SpriteInfo(Sprite, (1200, 300, 2, 768, 768, COLOURS['transparent'], 'resources/li.png'), 0),
                        SpriteInfo(TextButton, (500, 75, 2, 20, COLOURS['text-light'], COLOURS['text'], 'Theory', False, pygame.event.Event(PICK_CATEGORY, {'category':'theory', 'isplayer':True})), 0),
                        SpriteInfo(TextButton, (500, 200, 2, 20, COLOURS['text-light'], COLOURS['text'], 'Popularity', False, pygame.event.Event(PICK_CATEGORY, {'category':'popularity', 'isplayer':True})), 0),
                        SpriteInfo(TextButton, (500, 325, 2, 20, COLOURS['text-light'], COLOURS['text'], 'Difficulty', False, pygame.event.Event(PICK_CATEGORY, {'category':'difficulty', 'isplayer':True})), 0),
                        SpriteInfo(TextButton, (500, 450, 2, 20, COLOURS['text-light'], COLOURS['text'], 'Fun', False, pygame.event.Event(PICK_CATEGORY, {'category':'fun', 'isplayer':True})), 0),]),
          Scene(num=4,
                player=None,
                static=[SpriteInfo(Sprite, (0, 0, 0, SCREENSIZE[0], SCREENSIZE[1], COLOURS['white'], 'resources/mcs_2.png'), 0),
                        SpriteInfo(Sprite, (740, 440, 1, 435, 250, COLOURS['half-dark-grey']), 0),
                        SpriteInfo(Text, (820, 460, 3, 10, COLOURS['highlight-2-half'], COLOURS['text'], 'You Win!', False), 0),
                        SpriteInfo(TextButton, (770, 620, 3, 10, COLOURS['transparent'], COLOURS['text'], 'Title Menu', True, pygame.event.Event(SCENE_LOAD,{'scene':0})), 0),
                        SpriteInfo(TextButton, (1040, 620, 3, 10, COLOURS['transparent'], COLOURS['text'], 'Quit', True, pygame.event.Event(pygame.QUIT)), 0)
                        ])
          ]

# Loads a scene using two scene numbers
def load_scene(prev, new, mode):

    scene = SCENES[new]
    static = StaticCam()
    if scene.static_sprites:
        for s in scene.static_sprites:
            s.sprite(static, *s.params)

    if not scene.player_sprites:
        return StaticCam(), static

    if prev not in scene.player_pos.keys():
        prev = 0

    player = PlayerCam(*(scene.player_pos[prev]), mode)
    for s in scene.player_sprites:
        s.sprite(player, *s.params)

    return player, static