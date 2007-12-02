# Copyright 2007 Mikael Lind.

import pygame, sys, os, math
from pygame.locals import *
import config
from geometry import *
from Task import WaypointTask

pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Siblings in Arms")
screen = pygame.display.get_surface()

map_surface = screen.subsurface(pygame.Rect((0, 0), (640, 400)))
control_surface = screen.subsurface(pygame.Rect((0, 400), (640, 80)))

unit_surfaces = {}

def load_unit_surface(name):
    path = os.path.join(config.root, "data", name + ".png")
    surface = pygame.image.load(path)
    unit_surfaces[name] = surface

load_unit_surface("tavern")
load_unit_surface("warrior")

PIXELS_PER_METER_X = 40
PIXELS_PER_METER_Y = 30

selection = set()

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

def update(game):
    handle_events(game)
    update_screen(game)

mouse_button_down_pos = None

def handle_events(game):
    global mouse_button_down_pos
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_button_down_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.pos == mouse_button_down_pos:
                handle_click_event(event, game)
            else:
                handle_rectangle_event(mouse_button_down_pos, event, game)
            mouse_button_down_pos = None

def handle_click_event(event, game):
    clicked_unit = None
    for unit in game.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_surfaces[unit.spec.name]
        surface_size = surface.get_size()
        rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if (rectangle_contains_point(rect, event.pos)
            and (clicked_unit is None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit

    if clicked_unit is None:
        x, y = to_world_coords(event.pos, map_surface.get_size())
        pos = (int(round(x)), int(round(y)))
        for unit in selection:
            if unit.speed:
                unit.add_task(WaypointTask(pos))
                print ("Added waypoint %s to unit #%d." % (pos, unit.key))
    else:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if clicked_unit in selection:
                selection.remove(clicked_unit)
                print "Removed unit #%d from selection." % clicked_unit.key
            else:
                selection.add(clicked_unit)
                print "Added unit #%d to selection." % clicked_unit.key
        else:
            selection.clear()
            selection.add(clicked_unit)
            print "Selected unit #%d." % clicked_unit.key

def handle_rectangle_event(old_pos, event, game):
    selection_rect = normalize_rectangle((old_pos, event.pos))
    new_selection = set()
    for unit in game.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_surfaces[unit.spec.name]
        surface_size = surface.get_size()
        surface_rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if rectangle_intersects_rectangle(selection_rect, surface_rect):
            new_selection.add(unit)

    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        old_size = len(selection)
        selection |= new_selection
        print "Added %d unit(s) to selection." % (len(selection) - old_size)
    else:
        global selection
        selection = new_selection
        print "Selected %d unit(s)." % len(selection)

def update_screen(game):
    paint_map_surface(game)
    paint_control_surface(game)
    pygame.display.flip()

def paint_map_surface(game):
    map_surface.fill(pygame.color.Color("gold"))
    for unit in get_sorted_units(game):
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_surfaces[unit.spec.name]
        min_p = get_rect_min(screen_pos, surface.get_size())
        map_surface.blit(surface, min_p)
    paint_selection_rectangle(game)

def paint_selection_rectangle(game):
    if mouse_button_down_pos is not None:
        old_x, old_y = mouse_button_down_pos
        new_x, new_y = pygame.mouse.get_pos()
        x = min(old_x, new_x)
        y = min(old_y, new_y)
        width = abs(old_x - new_x)
        height = abs(old_y - new_y)
        pygame.draw.rect(map_surface, pygame.color.Color("white"),
                         pygame.Rect(x, y, width, height), 1)

def paint_control_surface(game):
    control_surface.fill(pygame.color.Color("gray"))
    if len(selection) == 1:
        unit = iter(selection).next()
        if unit.spec.name == "tavern":
            control_surface.blit(unit_surfaces["warrior"], (8, 8))
