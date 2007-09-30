from __future__ import division
import pygame, sys, os
from pygame.locals import *
import random
from Vector2 import Vector2

from Warrior import Warrior
from GameEngine import GameEngine
 
pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Siblings in Arms') 
screen = pygame.display.get_surface() 

PIXELS_PER_METER = 20.0

warrior_path = os.path.join('data', 'warrior.png')
warrior_surface = pygame.image.load(warrior_path)

def pick_pos():
    return Vector2(-12.0 + 24.0 * random.random(),
                   -8.0 + 16.0 * random.random())

def pick_velocity():
    return Vector2(-1.0 + 2.0 * random.random(),
                   -1.0 + 2.0 * random.random())

def get_time():
    return float(pygame.time.get_ticks()) / 1000.0

game = GameEngine(get_time())
for i in range(50):
    unit = Warrior()
    unit.pos = pick_pos()
    unit.velocity = pick_velocity()
    game.add_unit(unit)
            
def to_screen_pos(pos, screen_size):
    return (screen_size[0] // 2 + int(pos.x * PIXELS_PER_METER),
            screen_size[1] // 2 - int(pos.y * PIXELS_PER_METER))

def to_world_pos(pos, screen_size):
    return Vector2(float((pos[0] - screen_size[0] // 2) / PIXELS_PER_METER),
                   float((pos[1] - screen_size[1] // 2) / PIXELS_PER_METER))

def get_top_left(center, rect_size):
    return center[0] - rect_size[0] // 2, center[1] - rect_size[1] // 2

def is_x_and_y_less_or_equal(p, q):
    return p[0] <= q[0] and p[1] <= q[1]

def handle_click(event):
    screen_size = screen.get_size()
    surface_size = warrior_surface.get_size()
    clicked_unit = None
    for unit in game.units:
        screen_pos = to_screen_pos(unit.pos, screen_size)
        top_left = get_top_left(screen_pos, surface_size)
        lower_right = (top_left[0] + surface_size[0],
                       top_left[1] + surface_size[1])
        if (is_x_and_y_less_or_equal(top_left, event.pos)
            and is_x_and_y_less_or_equal(event.pos, lower_right)
            and (clicked_unit == None or unit.pos.y < clicked_unit.pos.y)):
            clicked_unit = unit
    if clicked_unit != None:
        print "Clicked unit #%d." % clicked_unit.num

def handle_events(events):
    for event in events: 
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            handle_click(event)

def get_sorted_units(game):
    units = list(game.units)
    units.sort(lambda a, b: cmp(b.pos.y, a.pos.y))
    return units

def redraw_screen(screen, game):
    screen.fill(pygame.color.Color('gold'))
    
    for unit in get_sorted_units(game):
        screen_pos = to_screen_pos(unit.pos, screen.get_size())
        top_left = get_top_left(screen_pos, warrior_surface.get_size())
        screen.blit(warrior_surface, top_left)
    pygame.display.flip()

old_ticks = pygame.time.get_ticks()
frame_count = 0
while True:
    handle_events(pygame.event.get())
    game.update(get_time())
    redraw_screen(screen, game)

    ticks = pygame.time.get_ticks()
    frame_count = frame_count + 1
    if ticks // 1000 != old_ticks // 1000:
        print "Drawing %d frames per second." % frame_count
        old_ticks = ticks
        frame_count = 0
