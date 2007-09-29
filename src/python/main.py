from __future__ import division
import pygame, sys,os
from pygame.locals import *
import random

from Warrior import Warrior
from GameEngine import GameEngine
 
pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Siblings in Arms') 
screen = pygame.display.get_surface() 

PIXELS_PER_METER = 20

warrior_path = os.path.join('data', 'warrior.png')
warrior_surface = pygame.image.load(warrior_path)

def pick_pos():
    return -12.0 + 24.0 * random.random(), -8.0 + 16.0 * random.random()

game = GameEngine()

for i in range(50):
    game.add_unit(Warrior(), pick_pos())
            
def to_screen_pos(pos, screen_size):
    return (int(screen_size[0] / 2 + pos[0] * PIXELS_PER_METER),
            int(screen_size[1] / 2 - pos[1] * PIXELS_PER_METER))

def to_world_pos(pos, screen_size):
    return (float((pos[0] - screen_size[0] / 2) / PIXELS_PER_METER),
            float((pos[1] - screen_size[1] / 2) / PIXELS_PER_METER))

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
            and (clicked_unit == None or unit.pos[1] < clicked_unit.pos[1])):
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
    units.sort(lambda a, b: cmp(b.pos[1], a.pos[1]))
    return units

def redraw_screen(screen, game):
    screen.fill(pygame.color.Color('gold'))
    
    for unit in get_sorted_units(game):
        screen_pos = to_screen_pos(unit.pos, screen.get_size())
        top_left = get_top_left(screen_pos, warrior_surface.get_size())
        screen.blit(warrior_surface, top_left)
    pygame.display.flip() 

while True: 
    handle_events(pygame.event.get())
    redraw_screen(screen, game)
