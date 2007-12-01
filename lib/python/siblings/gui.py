# Copyright 2007 Mikael Lind.

import pygame, sys, os, math
from pygame.locals import *
import config
from Event import Event, MoveEvent, QuitEvent, SelectEvent
from geometry import *
 
pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Siblings in Arms")
screen = pygame.display.get_surface() 

map_rect = pygame.Rect((0, 0), (640, 400))
control_rect = pygame.Rect((0, 400), (640, 80))

unit_surfaces = {}

def load_unit_surface(name):
    path = os.path.join(config.root, "data", name + ".png")
    surface = pygame.image.load(path)
    unit_surfaces[name] = surface

load_unit_surface("tavern")
load_unit_surface("warrior")

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

def get_sorted_units(game):
    units = game.units.values()
    units.sort(lambda a, b: cmp(b.pos[1], a.pos[1]))
    return units

def update_screen(game):
    screen.fill(pygame.color.Color('gold'), map_rect)
    for unit in get_sorted_units(game):
        screen_pos = to_screen_coords(unit.pos, screen.get_size())
        surface = unit_surfaces[unit.spec.name]
        min_p = get_rect_min(screen_pos, surface.get_size())
        screen.blit(surface, min_p)

    screen.fill(pygame.color.Color('black'), control_rect)

    pygame.display.flip()

def transform_click_event(event, game):
    screen_size = screen.get_size()
    clicked_unit = None
    for unit in game.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, screen_size)
        surface = unit_surfaces[unit.spec.name]
        surface_size = surface.get_size()
        rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if (rectangle_contains_point(rect, event.pos)
            and (clicked_unit == None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit

    if clicked_unit is None:
        return MoveEvent(to_world_coords(event.pos, screen_size))
    else:
        return SelectEvent(clicked_unit)

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
