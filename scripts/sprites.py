import random

import pygame
import math
from numpy.random import shuffle
from scripts.constants import *

# Helper Classes

def rect_dist(r1, r2):
    return math.sqrt((r1.centerx - r2.centerx)**2 + (r1.centery - r2.centery)**2)

#=======================================================================================================================
# SPRITES
#=======================================================================================================================

# Abstract Classes
#-----------------------------------------------------------------------------------------------------------------------

# Sprite Abstract Base Class
class SpriteABC(pygame.sprite.Sprite):

    def __init__(self, groups):
        super(SpriteABC, self).__init__(groups)
        self.font_small = pygame.font.Font(TYPEFACE, 28)
        self.font_large = pygame.font.Font(TYPEFACE, 56)
        self.z = 0

    def update(self, dt, keys, mouse, mouse_button, cards):
        pass

    def on_click(self, mouse_event):
        pass

    def interact(self, target=None):
        return False


# Simple Sprite Class
class Sprite(SpriteABC):

    def __init__(self, groups, x=0, y=0, z=0, w=10, h=10, c=COLOURS['white'], path=None):
        super(Sprite, self).__init__(groups)
        if path:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (w, h))
        else:
            self.image = pygame.Surface((w, h), pygame.SRCALPHA)
            self.image.fill(c)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.z = z


# Simple Text Class
class Text(SpriteABC):

    def __init__(self, groups, x=0, y=0, z=0, p=0, c=COLOURS['transparent'], ct=COLOURS['black'], t='', s=True):
        super(Text, self).__init__(groups)
        self.text = t
        params = (t, True, ct)
        text_rendered = self.font_small.render(*params) if s else self.font_large.render(*params)
        text_rect = text_rendered.get_rect()
        self.image = pygame.Surface((text_rect.width + 2*p, text_rect.height + 2*p), pygame.SRCALPHA)
        self.image.fill(c)
        self.image.blit(text_rendered, (p, p))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.z = z


# 2D Game Classes
#-----------------------------------------------------------------------------------------------------------------------

# Basic Player Class
class Player(Sprite):

    speed = 250
    width = 76
    height = 104
    path = 'resources/player/player_'
    hsize = 5
    animation_speed = 12

    def __init__(self, groups, x, y, z):
        super(Player, self).__init__(groups, x, y, z, self.width, self.height, 'black', f'{self.path}front_s.png')
        self.default = self.image.copy()
        self.pos = [x, y]
        self.vel = [0, 0]
        self.animation_num = 0
        self.imgs = [[pygame.image.load(f'{self.path}{x}').convert_alpha() for x in ('back_s.png', 'back_w1.png', 'back_w2.png')],
                     [pygame.image.load(f'{self.path}{x}').convert_alpha() for x in ('right_s.png', 'right_w1.png', 'right_w2.png')],
                     [pygame.image.load(f'{self.path}{x}').convert_alpha() for x in ('front_s.png', 'front_w1.png', 'front_w2.png')],
                     [pygame.image.load(f'{self.path}{x}').convert_alpha() for x in ('left_s.png', 'left_w1.png', 'left_w2.png')]]

        for i in range(4):
            for j in range(3):
                self.imgs[i][j] = self.imgs[i][j].subsurface(pygame.rect.Rect((8, 5), (18 ,27)))
                self.imgs[i][j] = pygame.transform.scale(self.imgs[i][j], (self.width, self.height))
        self.rect = self.imgs[0][0].get_rect(topleft=self.rect.topleft)
        self.direction = 0
        self.collisions = [False, False, False, False]
        self.hitbox = [pygame.rect.Rect((0,0), (0, 0)) for _ in range(4)]
        self.hitbox_update(x, y)
        self.hitbox_debug = [pygame.surface.Surface(self.hitbox[i].size) for i in range(4)]
        for i in range(4):
            self.hitbox_debug[i].fill(COLOURS['green'])

    def update(self, dt, keys, mouse, mouse_button, cards):
        # Get the wasd keys pressed
        dk = [keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a]]

        # Check for collisions in all directions
        for i in range(4):
            dk[i] = int(dk[i] and not self.collisions[i])

        # Update velocity
        self.vel[0], self.vel[1] = (dk[1] - dk[3]), (dk[2] - dk[0])
        mag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
        if mag:
            self.vel[0], self.vel[1] = self.vel[0]/mag, self.vel[1]/mag

        # Update the direction based on velocity
        d = self.direction
        if 1 in dk:
            d = dk.index(1)

        if d != self.direction:
            self.direction = d

        if mag:
            self.image = self.imgs[self.direction][(self.animation_num // self.animation_speed) + 1]
            self.animation_num = (self.animation_num + 1) % (2 * self.animation_speed)
        else:
            self.image = self.imgs[self.direction][0]

        # Update the position of the sprite using its velocity
        self.pos[0] += self.vel[0]*(dt/1000)*self.speed
        self.pos[1] += self.vel[1]*(dt/1000)*self.speed
        self.rect.update(self.pos, self.rect.size)
        self.hitbox_update(self.pos[0], self.pos[1])
        return

    def hitbox_update(self, x, y):
        self.hitbox[0].update((x - 1, y - self.hsize), (2*1 + self.width, self.hsize))
        self.hitbox[1].update((x + self.width, y - 1), (self.hsize, 2*1 + self.height))
        self.hitbox[2].update((x - 1, y + self.height), (2*1 + self.width, self.hsize))
        self.hitbox[3].update((x - self.hsize, y - 1), (self.hsize, 2*1 + self.height))


# Collectable Card Sprite
class Card2D(Sprite):

    def __init__(self, groups, x, y, z, ID):
        super(Card2D, self).__init__(groups, x, y, z, 25, 25, path='resources/CardThumb.png')
        self.ID = ID

    def interact(self, target):
        if rect_dist(self.rect, target.rect) < 100:
            new_event = pygame.event.Event(COLLECT_CARD, {'ID':self.ID})
            pygame.event.post(new_event)
            self.kill()
            return True
        return False


class Tp(Sprite):

    def __init__(self, groups, x, y, z, w, h, p):
        super(Tp, self).__init__(groups, x, y, z, w, h, COLOURS['transparent'], p)

    def interact(self, target):
        if rect_dist(self.rect, target.rect) < 100:
            new_event = pygame.event.Event(PICKUP_TP)
            pygame.event.post(new_event)
            self.kill()
            return True
        return False

class NPC(Sprite):

    def __init__(self, groups, x, y, z, path, name, speech, state=0, action=None):
        super(NPC, self).__init__(groups, x, y, z, 128, 128, COLOURS['white'], path)
        self.voice = pygame.mixer.Sound(f'resources/sounds/talk{random.randint(1,4)}.mp3')
        self.voice.set_volume(0.4)
        self.name = name
        self.speech = speech
        self.action = action
        self.state = state

    def interact(self, target):
        if rect_dist(self.rect, target.rect) < 150:

            if self.state != 0 and self.action:
                pygame.event.post(self.action)
                self.state = 0

            self.voice.play()

            new_event = pygame.event.Event(CREATE_SPRITE,
                                           {'sprite': TextCard, 'params': (self.name, self.speech),
                                            'kill': 0, 'player_cam': False})
            pygame.event.post(new_event)
            return True
        return False


class Effect(Sprite):

    path = 'resources/effect/effect'
    animation_speed = 6
    sound = pygame.mixer.Sound('resources/sounds/collect.wav')

    def __init__(self, groups, z):
        x, y = groups.player.rect.left, groups.player.rect.centery
        super(Effect, self).__init__(groups, x, y, z, 16, 16, COLOURS['transparent'], f'{self.path}_01.png')
        self.animation_num = 0
        self.default = self.image.copy()
        self.imgs = [pygame.image.load(f'{self.path}_{str(i).zfill(2)}.png').convert_alpha() for i in range(12)]
        self.sound.set_volume(0.8)
        self.sound.play()


    def update(self, dt, keys, mouse, mouse_button, cards):
        self.animation_num = min(self.animation_num + (self.animation_speed*dt/1000), 11)
        self.image = self.imgs[math.floor(self.animation_num)]

# Card Game Classes
#-----------------------------------------------------------------------------------------------------------------------

# Class for each card in top trumps
class Card(Sprite):
    width = 280
    height = 400
    path = 'resources/cards/card-'
    def __init__(self, groups, x, y, z, ID, path, stats):
        super(Card, self).__init__(groups, x, y, z, self.width, self.height, COLOURS['transparent'], path)
        self.ID = ID
        self.name = path[path.index('-'):-3]
        self.flipped = False
        self.front = self.image.copy()
        self.back = pygame.image.load(f'{self.path}back.png').convert_alpha()
        self.stats = stats

    def update(self, dt, keys, mouse, mouse_button, cards):
        self.image = self.front if self.flipped else self.back

    def flip(self):
        self.flipped ^= True


class CardGame():

    card_set = [
        {'ID': 0, 'path': 'resources/cards/card-ai.png', 'theory': 4, 'popularity': 5, 'difficulty': 5, 'fun': 3},
        {'ID': 1, 'path': 'resources/cards/card-software.png', 'theory': 1, 'popularity': 5, 'difficulty': 4, 'fun': 3},
        {'ID': 2, 'path': 'resources/cards/card-toc.png', 'theory': 5, 'popularity': 3, 'difficulty': 5, 'fun': 2},
        {'ID': 3, 'path': 'resources/cards/card-maths.png', 'theory': 5, 'popularity': 4, 'difficulty': 4, 'fun': 3},
        {'ID': 4, 'path': 'resources/cards/card-game.png', 'theory': 3, 'popularity': 2, 'difficulty': 2, 'fun': 5},
        {'ID': 5, 'path': 'resources/cards/card-network.png', 'theory': 3, 'popularity': 2, 'difficulty': 3, 'fun': 3},
        {'ID': 6, 'path': 'resources/cards/card-program.png', 'theory': 3, 'popularity': 4, 'difficulty': 3, 'fun': 4},
        {'ID': 7, 'path': 'resources/cards/card-cvision.png', 'theory': 4, 'popularity': 4, 'difficulty': 3, 'fun': 3},
    ]

    def __init__(self, static_group):
        self.player_turn = True
        shuffle(self.card_set)
        self.player_card_params = self.card_set[len(self.card_set) // 2:]
        self.com_card_params = self.card_set[:len(self.card_set) // 2]

        self.player_cards = []
        self.com_cards = []

        for i, card in enumerate(self.player_card_params):
            sprite = Card(static_group, 50+25*i, 75+25*i, 2+i, card['ID'], card['path'], {k: card[k] for k in ('theory', 'popularity', 'difficulty', 'fun')})
            self.player_cards.append(sprite)

        for i, card in enumerate(self.com_card_params):
            sprite = Card(static_group, 1100-25*i, 75+25*i, 2+i, card['ID'], card['path'], {k: card[k] for k in ('theory', 'popularity', 'difficulty', 'fun')})
            self.com_cards.append(sprite)

        self.player_topcard = self.player_cards[-1]
        self.com_topcard = self.com_cards[-1]

        self.player_topcard.flip()
        self.com_topcard.flip()
        self.state = 0
        self.static_group = static_group

    def input(self, category, isplayer):
        if self.player_turn == isplayer:
            self.turn(category)

    def turn(self, category):

        if self.player_topcard.stats[category] == self.com_topcard.stats[category]:
            print('draw')

        else:
            if self.player_topcard.stats[category] > self.com_topcard.stats[category]:
                self.player_cards.insert(0, self.com_cards.pop())
                self.player_cards.insert(0, self.player_cards.pop())
            else:
                self.com_cards.insert(0, self.com_cards.pop())
                self.com_cards.insert(0, self.player_cards.pop())

            is_winner = self.check_win()
            if is_winner:
                if is_winner == 1:
                    pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 2}))
                elif is_winner == 2:
                    pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 4}))
                return

            self.update_card_pos()
            self.player_topcard = self.player_cards[-1]
            self.com_topcard = self.com_cards[-1]
            self.player_topcard.flip()
            self.com_topcard.flip()
            # self.player_turn ^= True

    def check_win(self):
        if len(self.player_cards) == 0:
            return 1
        elif len(self.com_cards) == 0:
            return 2
        return False

    def update_card_pos(self):
        for i, sprite in enumerate(self.player_cards):
            sprite.rect.update((50 + 25 * i, 75 + 25 * i), sprite.rect.size)
            sprite.z = 2+i
            sprite.flipped = False

        for i, sprite in enumerate(self.com_cards):
            sprite.rect.update((1100 - 25 * i, 75 + 25 * i), sprite.rect.size)
            sprite.z = 2+i
            sprite.flipped = False

# Need a class / event for the computer playing the game
#   - Create a class for AI that reacts and decides on Computers turns.
# Update the cards when someone loses.

# UI Elements
#-----------------------------------------------------------------------------------------------------------------------

# Simple Button
class Button(Sprite):

    click_sound = pygame.mixer.Sound('resources/sounds/button.wav')

    def __init__(self, groups, x=0, y=0, z=0, w=10, h=10, c=COLOURS['white'], ce=pygame.event.Event(0)):
        super(Button, self).__init__(groups, x, y, z, w, h, c, None)
        self.default = self.image.copy()
        self.hover = self.image.copy()
        temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        temp_surf.fill(COLOURS['highlight-1-half'])
        self.hover.blit(temp_surf, (0, 0))
        self.click_event = ce
        self.click_sound.set_volume(0.2)

    def update(self, dt, keys, mouse, mouse_button, cards):
        self.image = self.hover if self.rect.collidepoint(mouse) else self.default

    def on_click(self, mouse_event):
        self.click_sound.play()
        return pygame.event.post(self.click_event)


# Button with text
class TextButton(Text):

    click_sound = pygame.mixer.Sound('resources/sounds/button.wav')

    def __init__(self, groups, x=0, y=0, z=0, p=0, c=COLOURS['white'], ct=COLOURS['black'], t='', s=False, ce=pygame.event.Event(0)):
        super(TextButton, self).__init__(groups, x, y, z, p, c, ct, t, s)
        self.default = self.image.copy()
        self.hover = self.image.copy()
        temp_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        temp_surf.fill(COLOURS['highlight-1-half'])
        self.hover.blit(temp_surf, (0, 0))
        self.click_event = ce
        self.click_sound.set_volume(0.2)

    def update(self, dt, keys, mouse, mouse_button, cards):
        self.image = self.hover if self.rect.collidepoint(mouse) else self.default

    def on_click(self, mouse_event):
        self.click_sound.play()
        return pygame.event.post(self.click_event)


# Class for dialogue
class TextCard(Text):

    width = SCREENSIZE[0]
    height = 200

    c1 = COLOURS['highlight-1-half']
    c2 = COLOURS['main-half']
    c3 = COLOURS['highlight-2-half']
    ct = COLOURS['text']

    # c1 = (127, 127, 127, 200)
    # c2 = (127, 127, 127, 150)
    # c3 = (127, 127, 127, 100)
    # ct = COLOURS['black']

    def __init__(self, groups, name, text):
        super(TextCard, self).__init__(groups, 0, SCREENSIZE[1] - self.height + 2, 2, 10, self.c1, self.ct, name, False)
        self.body = TextCardBody(groups, 10, SCREENSIZE[1] - self.height + 12 + self.rect.height, self.c1, self.ct, text)
        header = pygame.surface.Surface((self.width, self.rect.height), pygame.SRCALPHA)
        header.fill(self.c2)
        outline = pygame.surface.Surface((self.width, 2), pygame.SRCALPHA)
        outline.fill(COLOURS['black'])
        outline2 = pygame.surface.Surface((2, self.height), pygame.SRCALPHA)
        outline2.fill(COLOURS['black'])
        body_bg = pygame.surface.Surface((self.width, self.height + 2), pygame.SRCALPHA)
        body_bg.fill(self.c3)
        body_bg.blit(outline, (0, 0))
        body_bg.blit(header, (0, 2))
        body_bg.blit(self.image, (0, 2))
        body_bg.blit(outline, (0, self.rect.height))
        body_bg.blit(outline2, (self.width-2, 0))
        self.image = body_bg
        self.rect = body_bg.get_rect(topleft=self.rect.topleft)
        self.killed = False

    def update(self, dt, keys, mouse, mouse_button, cards):
        if self.killed:
            self.rect.move_ip(0, 500*(dt/1000))

    def interact(self, target=None):
        self.body.kill()
        self.killed = True
        kill_event = pygame.event.Event(KILL_SPRITE, {'sprite':self})
        pygame.time.set_timer(kill_event, 400, 1)
        return True


# Helper class for dialog
class TextCardBody(Text):

    def __init__(self, groups, x, y, c, ct, text):
        super(TextCardBody, self).__init__(groups, x, y, 3, 5, c, ct, text, True)
        self.image_full = self.image.copy()
        self.image = pygame.transform.chop(self.image_full, pygame.rect.Rect(self.rect.topleft, self.rect.size))
        self.animation_num = 0
        self.animation_speed = 600

    def update(self, dt, keys, mouse, mouse_button, cards):
        if self.animation_num < self.rect.width:
            self.animation_num = self.animation_num + self.animation_speed*(dt / 1000)
            crop = pygame.rect.Rect((self.rect.left + self.animation_num, self.rect.top), (self.rect.width - self.animation_num, self.rect.height))
            self.image = pygame.transform.chop(self.image_full, crop)


# Slider for the settings page
class VolumeSlider(Sprite):

    width = 800

    def __init__(self, groups, y, z):
        super(VolumeSlider, self).__init__(groups, (SCREENSIZE[0] - self.width)//2, y, z, self.width, 50, COLOURS['highlight-1-half']) # , path='resources/volume.png'"
        self.slide = Sprite(groups, (SCREENSIZE[0] - 5)//2, y, z+1, 5, 50, COLOURS['red'])
        self.val = 0.2

    def update(self, dt, keys, mouse, mouse_button, cards):
        if mouse_button[0] and self.rect.collidepoint(mouse):
            self.slide.rect.centerx = mouse[0]
            self.val = (mouse[0] - (SCREENSIZE[0] - self.width) // 2) / self.width
            pygame.mixer.music.set_volume(self.val)


# Display for the number of cards collected
class CardCounter(Text):

    def  __init__(self, groups, num):
        super(CardCounter, self).__init__(groups, 0, 50, 2, 10, COLOURS['highlight-2-half'], COLOURS['text'], f'{num}/{NUM_CARDS} Cards Found', True)
        self.num = num

    def update(self, dt, keys, mouse, mouse_button, cards):
        if self.num != sum(int(x) for x in cards):
            new_event = pygame.event.Event(CREATE_SPRITE, {'sprite': CardCounter, 'params': [self.num+1], 'kill': 0, 'player_cam':False})
            pygame.event.post(new_event)
            self.kill()


class Timer(Sprite):

    difficulty = {'easy':120, 'normal':90, 'hard':45}
    height = 8
    width = 70

    def __init__(self, groups, mode):

        super(Timer, self).__init__(groups, 1000, 1000, 4, self.width, self.height, COLOURS['red'])
        self.time = self.difficulty[mode]
        self.remaining_time = self.time
        self.default = self.image.copy()

    def update(self, dt, keys, mouse, mouse_button, cards):
        self.remaining_time -= dt / 2000
        if self.remaining_time <= 0:
            new_event = pygame.event.Event(SCENE_LOAD, {'scene':0})
            pygame.event.post(new_event)

    def update_timer(self):
        new_width = math.floor(self.width*(self.remaining_time/self.time))
        new_surf = pygame.surface.Surface((new_width, 50))
        new_surf.fill(COLOURS['green'])
        self.image = self.default.copy()
        self.image.blit(new_surf, (self.width - new_width, 0))

#=======================================================================================================================
# SPRITE GROUPS
#=======================================================================================================================

# Sprite group for following a target sprite
# Instantiates a player at the same time
class PlayerCam(pygame.sprite.Group):

    def __init__(self, x, y, z, mode):
        super(PlayerCam, self).__init__()
        self.player = Player(self, x, y, z)
        self.timer = Timer(self, mode)
        self.screen = pygame.display.get_surface()
        self.offset = [0, 0]
        self.cam_rect = pygame.rect.Rect(100, 100, SCREENSIZE[0]-200, SCREENSIZE[1]-200)

    def draw(self):

        self.cam_rect.left = min(self.player.rect.left, self.cam_rect.left)
        self.cam_rect.right = max(self.player.rect.right, self.cam_rect.right)
        self.cam_rect.top = min(self.player.rect.top, self.cam_rect.top)
        self.cam_rect.bottom = max(self.player.rect.bottom, self.cam_rect.bottom)

        for sprite in sorted(self.sprites(), key=lambda x:(x.z, x.rect.centery)):
            new_pos = (sprite.rect.left - self.cam_rect.left + 100, sprite.rect.top - self.cam_rect.top + 100)
            self.screen.blit(sprite.image, new_pos)

    def on_click(self, event):
        offset_mouse = (event.pos[0] + self.cam_rect.left - 100, event.pos[1] + self.cam_rect.top - 100)
        for sprite in self.sprites():
            if sprite.rect.collidepoint(offset_mouse):
                sprite.on_click(event)

    def test_collisions(self):
        self.player.collisions = [False] * 4
        for sprite in self.sprites():
            if self.player.z == sprite.z and sprite != self.player:
                for i, hbox in enumerate(self.player.hitbox):
                    if sprite.rect.colliderect(hbox):
                        self.player.collisions[i] = True

    def interact(self):
        for sprite in self.sprites():
            if sprite.interact(self.player):
                sprite.active = False
                return True
        return False

    def update(self, dt, keys, mouse, mouse_button, cards):
        offset_mouse = (mouse[0] + self.cam_rect.left - 100, mouse[1] + self.cam_rect.top - 100)
        for sprite in self.sprites():
            sprite.update(dt, keys, offset_mouse, mouse_button, cards)
        self.timer.rect.update((self.player.rect.left, self.player.rect.top-15), self.timer.rect.size)

    def update_timer(self):
        self.timer.update_timer()

# A sprite group that doesn't move
class StaticCam(pygame.sprite.Group):

    def __init__(self):
        super(StaticCam, self).__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in sorted(self.sprites(), key=lambda x:(x.z, x.rect.centery)):
            self.screen.blit(sprite.image, sprite.rect)

    def on_click(self, event):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(event.pos):
                sprite.on_click(event)

    def test_collisions(self):
        pass

    def interact(self):
        for sprite in self.sprites():
            if sprite.interact():
                sprite.active = False
                return True
        return False

    def update(self, dt, keys, mouse, mouse_button, cards):
        for sprite in self.sprites():
            sprite.update(dt, keys, mouse, mouse_button, cards)