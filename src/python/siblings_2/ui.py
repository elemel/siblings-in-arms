# Copyright 2007 Mikael Lind.

import pygame, sys, os
from pygame.locals import *
import math
from Event import Event, MoveEvent, QuitEvent, SelectEvent
 
pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Siblings in Arms")
screen = pygame.display.get_surface() 

warrior_path = os.path.join('data', 'warrior.png')
warrior_surface = pygame.image.load(warrior_path)

PIXELS_PER_METER_X = 40
PIXELS_PER_METER_Y = 30

def to_screen_coords(point, screen_size):
    x, y = point
    width, height = screen_size
    return (int(x * PIXELS_PER_METER_X),
            int(height - y * PIXELS_PER_METER_Y))

def to_world_coords(point, screen_size):
    x, y = point
    width, height = screen_size
    return (float(x) / PIXELS_PER_METER_X,
            float(height - y) / PIXELS_PER_METER_Y)

def get_rect_min(center, size):
    x, y = center
    width, height = size
    return int(x - width / 2.0), int(y - height / 2.0)

def is_x_and_y_less_or_equal(p, q):
    return p[0] <= q[0] and p[1] <= q[1]

def log_click(clicked_unit):
    if clicked_unit != None:
        message = "Clicked unit #%d" % clicked_unit.num
        found_units = game.find_units(Circle2(clicked_unit.pos, 5.0))
        if len(found_units) > 1:
            found_units.remove(clicked_unit)
            message += (", which is close to unit(s) %s"
                        % (", ".join(map(lambda unit: "#" + str(unit.num),
                                         found_units))))
        print message + "."

def handle_click(event):
    screen_size = screen.get_size()
    surface_size = warrior_surface.get_size()
    clicked_unit = None
    for unit in game.units:
        screen_pos = to_screen_coords(unit.pos, screen_size)
        top_left = get_rect_min(screen_pos, surface_size)
        lower_right = (top_left[0] + surface_size[0],
                       top_left[1] + surface_size[1])
        if (is_x_and_y_less_or_equal(top_left, event.pos)
            and is_x_and_y_less_or_equal(event.pos, lower_right)
            and (clicked_unit == None or unit.pos.y < clicked_unit.pos.y)):
            clicked_unit = unit
    log_click(clicked_unit)

def handle_events(events):
    for event in events: 
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            handle_click(event)

def get_sorted_units(game):
    units = game.units.values()
    units.sort(lambda a, b: cmp(b.pos[1], a.pos[1]))
    return units

def update_screen(game):
    screen.fill(pygame.color.Color('gold'))
    for unit in get_sorted_units(game):
        screen_pos = to_screen_coords(unit.pos, screen.get_size())
        top_left = get_rect_min(screen_pos, warrior_surface.get_size())
        screen.blit(warrior_surface, top_left)
    pygame.display.flip()

def transform_click_event(event, game):
    screen_size = screen.get_size()
    surface_size = warrior_surface.get_size()
    clicked_unit = None
    for unit in game.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, screen_size)
        surface_min = get_rect_min(screen_pos, surface_size)
        surface_max = (surface_min[0] + surface_size[0],
                       surface_min[1] + surface_size[1])
        if (is_x_and_y_less_or_equal(surface_min, event.pos)
            and is_x_and_y_less_or_equal(event.pos, surface_max)
            and (clicked_unit is None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit
    if clicked_unit is not None:
        return SelectEvent(clicked_unit)
    else:
        return MoveEvent(to_world_coords(event.pos, screen_size))

def transform_event(event, game):
    if event.type == QUIT:
        return QuitEvent()
    elif event.type == MOUSEBUTTONDOWN:
        return transform_click_event(event, game)
    else:
        return None

def poll_events(game):
    transformed = (transform_event(e, game) for e in pygame.event.get())
    return (e for e in transformed if e is not None)
