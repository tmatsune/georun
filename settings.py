import pygame as pg
import math, sys, random

# GAME CONSTANTS
ROWS = 16 
COLS = 16 
CS = 16
HALF_CS = CS//2
WIDTH = ROWS * CS 
HEIGHT = ROWS * CS
SCALE = 2
SCREEN_WIDTH = WIDTH * SCALE
SCREEN_HEIGHT = HEIGHT * SCALE
CENTER = [HEIGHT // 2, WIDTH // 2]
FPS = 60

# PLAYER CONSTANTS
PLAYER_RADIUS = CS//2
PLAYER_COLOR = (255,68,126)
PLAYER_STATES = ['idle', 'moving', 'dash']
PLAYER_MAX_JUMPS = 2
PLAYER_JUMP_SPEED = -2
PLAYER_FALL_SPEED = 2
PLAYER_SPEED = 200
PLAYER_NORM_SIZE = [CS, CS]

# OTHER 
SURROUND_POS = [
    [-1, 0],
    [0, 0],
    [1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
    [-1, 1],
    [0, 1],
    [1, 1],
]
for p in [[[x - 2, y - 2] for x in range(5)] for y in range(5)]:
    SURROUND_POS += p
'''
[-1,-1][ 0,-1][ 1, -1]
[-1, 0][ 0, 0][ 1, 0]
[-1, 1][ 0, 1][ 1, 1]
'''

# ACTION CONSTANS 
GRAVITY = 0.06

# COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKY_BLUE = (70,210,255)

