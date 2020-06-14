import time
import sys
import random
import itertools

import pygame
import numpy as np

from generate import generate_maze
from bot import Bot


mode = input('Two players or one player? (Enter 2 or 1)')

pygame.init()

# maze related
maze_size = np.array([35, 25])
width, height = maze_size
maze = generate_maze(width, height)
SCALE = 25

screen_size = maze_size * SCALE
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Maze!')

scales = {
    'dog.jpg': (SCALE, SCALE),
    'cat.jpg': (SCALE, SCALE),
    'bone.png': (SCALE, SCALE),
    'you win.png': (300, 200)
}

images = []
for name, size in scales.items():
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, size)
    images.append(image)

dog, cat, bone, win = images

# load sounds
sounds = {}
for name in ['eat', 'walk', 'oof', 'dog_win', 'cat_win']:
    sounds[name] = pygame.mixer.Sound(f'{name}.ogg')
    
sounds['walk'].set_volume(0.1)

# dog = pygame.transform.scale(dog, (100, 100))
# take in a surfact and scale it to ( , ) size

# screen.blit(dog, (0,0)) 
# (actual pic, where you want on the screen).

dog_pos = np.array([1, 1])
cat_pos = np.array([width-2, 1])

# List of all coordinates where the maze is empty
valid_locations = list(np.array(np.where(maze == 0)).T)

# Choose 10 empty cells to put bones
bone_locations = random.sample(valid_locations, 15)

movements = {
    pygame.K_s: (dog_pos, 0, 1),
    pygame.K_w: (dog_pos, 0, -1),
    pygame.K_a: (dog_pos, -1, 0),
    pygame.K_d: (dog_pos, 1, 0),
    pygame.K_DOWN: (cat_pos, 0, 1),
    pygame.K_UP: (cat_pos, 0, -1),
    pygame.K_LEFT: (cat_pos, -1, 0),
    pygame.K_RIGHT: (cat_pos, 1, 0),
}

#text related
font = pygame.font.SysFont('Bradley Hand', 24)

text = {}
points = {'cat': 0, 'dog': 0}

def render_text():
    for key, value in points.items():
        text[key] = font.render(f'{key.title()}: {value}', True, (255, 255, 255))
render_text()

def eat_bones(pos, character):
    global bone_locations

    new_locations = []
    for loc in bone_locations:
        if (loc == pos).all():
            points[character] += 10
            render_text()

            if len(bone_locations) == 1:
                end_game()
            else:
                play_sound('eat', 3)
        else:
            new_locations.append(loc)
    bone_locations = new_locations

def end_game():
    winner = max(points.keys(), key=points.get)
    print(winner)
    play_sound(f'{winner}_win', 2)

def play_sound(name, channel):
    pygame.mixer.Channel(channel).play(sounds[name])

def process_key(key):
    try:
        pos, dx, dy = movements[key]
        pos += np.array([dx, dy])
        if maze[tuple(pos)] == 1:
            pos -= np.array([dx, dy])
            play_sound('oof', 0)
        else:
            play_sound('walk', 1)
    except KeyError:
        pass

# Bot player (optional)
bot_keys = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}
bot = Bot(maze)

for frame in itertools.count():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            process_key(event.key)

    if frame % 3 == 0 and mode == '1':
        # Move bot
        bot_choice = bot.choose_move(bone_locations, cat_pos)
        if bot_choice in keys:
            process_key(bot_keys[bot_choice])

    screen.fill([255,255,255])

    for (y, row) in enumerate(maze.T):
        for (x, cell) in enumerate(row):
            if cell:
                rect = pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE)
                pygame.draw.rect(screen, (132, 134, 139), rect)

    screen.blit(dog, dog_pos * SCALE)
    screen.blit(cat, cat_pos * SCALE)

    screen.blit(text['dog'], (10, 5))
    screen.blit(text['cat'], (screen_size[0] - 70,  5))

    eat_bones(dog_pos,'dog')
    eat_bones(cat_pos,'cat')

    for loc in bone_locations:
        screen.blit(bone, loc * SCALE)

    if not bone_locations:
        screen.blit(win, screen_size//2 - np.array([150, 100]))
    
    pygame.display.flip()
    time.sleep(0.02)
