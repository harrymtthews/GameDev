import pygame

pygame.init()

from scripts.constants import *
from scripts.debugging import FPS
from scripts.scenes import load_scene
from scripts.sprites import *

screen = pygame.display.set_mode(SCREENSIZE) #, pygame.FULLSCREEN)
clock = pygame.time.Clock()

pygame.mixer.music.load('resources/sounds/bg_music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

dt = 1
scene = 0
cards = [False]*NUM_CARDS
mouse = (0, 0)
done = False
debug = False
game = None
interact_active = True
difficulty = 'easy'

pygame.time.set_timer(UPDATE_FREQUENT, 10)
pygame.time.set_timer(UPDATE_INFREQUENT, 1000)
pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 0}))

player, static = StaticCam(), StaticCam()
FPS_count = FPS()

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        if event.type == UPDATE_FREQUENT:
            # Update Inputs
            mouse = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()

            player.test_collisions()

            # Update Sprites
            player.update(dt, keys, mouse, mouse_buttons, cards)
            static.update(dt, keys, mouse, mouse_buttons, cards)

            if debug:
                FPS_count.update(dt, keys, mouse, mouse_buttons)

        if event.type == SCENE_LOAD:

            player.empty()
            static.empty()

            if scene == 2 and event.scene == 0:
                difficulty = 'easy'

            player, static = load_scene(scene, event.scene, difficulty)

            if event.scene == 3:
                screen_copy = screen.copy()
                new_surf = pygame.surface.Surface(SCREENSIZE, pygame.SRCALPHA).convert_alpha()
                new_surf.fill(COLOURS['dark-grey'])
                screen_copy.blit(new_surf, (0, 0))
                pygame.image.save(screen_copy, 'resources/bckg2.png')
                Sprite(static, 0, 0, 0, SCREENSIZE[0], SCREENSIZE[1], COLOURS['transparent'], 'resources/bckg2.png')
                game = CardGame(static)

            scene = event.scene
            cards = [False] * NUM_CARDS

        if event.type == pygame.MOUSEBUTTONDOWN:
            if debug:
                print(event.pos)
            player.on_click(event)
            static.on_click(event)

        if event.type == CREATE_SPRITE:
            new_sprite = event.sprite(player if event.player_cam else static, *event.params)
            if event.kill:
                new_event = pygame.event.Event(KILL_SPRITE, {'sprite':new_sprite})
                pygame.time.set_timer(new_event, event.kill, 1)

        if event.type == KILL_SPRITE:
            event.sprite.kill()

        if event.type == INTERACT_TIMER:
            interact_active = True

        if event.type == COLLECT_CARD:
            new_event = pygame.event.Event(CREATE_SPRITE, {'sprite': Effect, 'params': [4], 'kill': 1200, 'player_cam': True})
            pygame.event.post(new_event)
            cards[event.ID] = True
            if sum(int(x) for x in cards) == NUM_CARDS:
                for s in player:
                    if type(s) == NPC and s.name == 'Frederick':
                        s.state = 1
                        s.speech = 'You found them all! Now let\'s play top trumps. Choose a category.'

        if event.type == PICKUP_TP:
            for s in player:
                if type(s) == NPC and s.name == 'Johnny':
                    s.state = 1
                    s.speech = 'Wow thank you! Here, take this card... you should probably wash it first...'

        if event.type == USE_VENDING:
            for s in player:
                if type(s) == NPC and s.name == 'Jason Statham':
                    s.state = 1
                    s.speech = 'Quavers! That\'s exactly what I needed. Take this card I found on set.'

        if event.type == PICK_CATEGORY:
            game.input(event.category, event.isplayer)

        if event.type == UPDATE_INFREQUENT:
            if player:
                player.update_timer()

        if event.type == CHANGE_DIFFICULTY:
            difficulty = event.mode

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_e and interact_active:
                if static.interact() or player.interact():
                    interact_active = False
                    pygame.time.set_timer(INTERACT_TIMER, 1000, 1)

            elif event.key == pygame.K_TAB:
                debug ^= True

            elif event.key == pygame.K_1 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 0}))

            elif event.key == pygame.K_1 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 0}))

            elif event.key == pygame.K_2 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 1}))

            elif event.key == pygame.K_3 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 2}))

            elif event.key == pygame.K_4 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 3}))

            elif event.key == pygame.K_5 and debug:
                pygame.event.post(pygame.event.Event(SCENE_LOAD, {'scene': 4}))

    screen.fill(COLOURS['black'])
    player.draw()
    static.draw()
    if debug:
        screen.blit(FPS_count.image, FPS_count.rect)
    pygame.display.update()
    dt = clock.tick(60)

pygame.quit()