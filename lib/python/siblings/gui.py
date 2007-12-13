# Copyright 2007 Mikael Lind.

import pygame, sys, os, math
from pygame.locals import *
import config
from geometry import *
from tasks.AttackTask import AttackTask
from tasks.BuildTask import BuildTask
from tasks.MoveTask import MoveTask

pygame.init() 

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Siblings in Arms")
screen = pygame.display.get_surface()

map_rect = pygame.Rect((0, 0), (800, 550))
control_rect = pygame.Rect((0, 550), (800, 50))
map_surface = screen.subsurface(map_rect)
control_panel = screen.subsurface(control_rect)

def load_image(name):
    path = os.path.join(config.root, "data", name + ".png")
    return pygame.image.load(path)

unit_images = {}
unit_icons = {}

def load_unit_images():
    for name in ["knight", "monk", "priest", "ranger", "rogue", "tavern",
                 "warrior", "wizard"]:
        unit_images[name] = load_image(name)
        unit_icons[name] = load_image(name + "-icon")

load_unit_images()

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

def get_sorted_units(game_engine):
    units = game_engine.unit_manager._units.values()
    units.sort(lambda a, b: cmp(b.pos[1], a.pos[1]))
    return units

def paint_image(surface, image, pos):
    x, y = pos
    width, height = image.get_size()
    surface.blit(image, (x - width // 2, y - height // 2))

def update(game_engine, fps):
    new_selection = set(unit for unit in selection if unit.pos)
    if new_selection != selection:
        selection.clear()
        selection.update(new_selection)
    handle_events(game_engine)
    update_screen(game_engine)

mouse_button_down_pos = None

def handle_events(game_engine):
    global mouse_button_down_pos
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_button_down_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            if (mouse_button_down_pos is not None
                and manhattan_distance(event.pos, mouse_button_down_pos) <= 6):
                handle_click_event(event, game_engine)
            else:
                handle_rectangle_event(mouse_button_down_pos, event,
                                       game_engine)
            mouse_button_down_pos = None

def handle_click_event(event, game_engine):
    x, y = event.pos
    if map_rect.collidepoint(x, y):
        if event.button == 1:
            handle_select_event(event, game_engine)
        else:
            handle_command_event(event, game_engine)
    else:
        handle_control_event(event, game_engine)

def handle_select_event(event, game_engine):
    clicked_unit = None
    for unit in game_engine.unit_manager._units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[unit.spec.name]
        surface_size = surface.get_size()
        rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if (rectangle_contains_point(rect, event.pos)
            and (clicked_unit is None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit

    if clicked_unit is not None:
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

def handle_command_event(event, game_engine):
    clicked_unit = None
    for unit in game_engine.unit_manager._units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[unit.spec.name]
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
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    game_engine.taskmaster.clear_tasks(unit)
                    print "Cleared tasks for unit #%d." % unit.key
                game_engine.taskmaster.append_task(unit, MoveTask(pos))
                print "Added waypoint %s to unit #%d." % (pos, unit.key)
    else:
        for unit in selection:
            if unit.damage and unit.player != clicked_unit.player:
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    game_engine.taskmaster.clear_tasks(unit)
                    print "Cleared tasks for unit #%d." % unit.key
                game_engine.taskmaster.append_task(unit,
                                                   AttackTask(clicked_unit))
                print ("Added target #%d to unit #%d."
                       % (clicked_unit.key, unit.key))

def handle_control_event(event, game_engine):
    x, y = event.pos
    button = x // 50
    if len(selection) == 1:
        unit = iter(selection).next()
        if unit.spec.name == "tavern":
            if button == 0:
                game_engine.taskmaster.append_task(unit, BuildTask("monk"))
            elif button == 1:
                game_engine.taskmaster.append_task(unit, BuildTask("warrior"))
            elif button == 2:
                game_engine.taskmaster.append_task(unit, BuildTask("ranger"))
            elif button == 3:
                game_engine.taskmaster.append_task(unit, BuildTask("knight"))
            elif button == 4:
                game_engine.taskmaster.append_task(unit, BuildTask("rogue"))
            elif button == 5:
                game_engine.taskmaster.append_task(unit, BuildTask("priest"))
            elif button == 6:
                game_engine.taskmaster.append_task(unit, BuildTask("wizard"))

def handle_rectangle_event(old_pos, event, game_engine):
    global selection
    selection_rect = normalize_rectangle((old_pos, event.pos))
    new_selection = set()
    for unit in game_engine.unit_manager._units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[unit.spec.name]
        surface_size = surface.get_size()
        surface_rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if rectangle_intersects_rectangle(selection_rect, surface_rect):
            new_selection.add(unit)

    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        old_size = len(selection)
        selection |= new_selection
        print "Added %d unit(s) to selection." % (len(selection) - old_size)
    else:
        selection = new_selection
        print "Selected %d unit(s)." % len(selection)

def update_screen(game_engine):
    paint_map_surface(game_engine)
    paint_control_panel(game_engine)
    pygame.display.flip()

def paint_map_surface(game_engine):
    map_surface.fill(pygame.color.Color("#886644"))
    for unit in get_sorted_units(game_engine):
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        image = unit_images[unit.spec.name]
        width, height = image.get_size()
        radius = max(width, height) // 2
        if unit in selection:
            pygame.draw.circle(map_surface, pygame.color.Color("green"),
                               screen_pos, radius - 2, 3)
        pygame.draw.circle(map_surface, pygame.color.Color(unit.player),
                           screen_pos, radius - 3, 1)
        paint_image(map_surface, image, screen_pos)
    paint_selection_rectangle(game_engine)

def paint_selection_rectangle(game_engine):
    if mouse_button_down_pos is not None:
        old_x, old_y = mouse_button_down_pos
        new_x, new_y = pygame.mouse.get_pos()
        x = min(old_x, new_x)
        y = min(old_y, new_y)
        width = abs(old_x - new_x)
        height = abs(old_y - new_y)
        pygame.draw.rect(map_surface, pygame.color.Color("green"),
                         pygame.Rect(x, y, width, height), 1)

def paint_control_panel(game_engine):
    control_panel.fill(pygame.color.Color("gray"))
    if len(selection) == 1:
        unit = iter(selection).next()
        if unit.spec.name == "tavern":
            paint_image(control_panel, unit_icons["monk"], (25, 25))
            paint_image(control_panel, unit_icons["warrior"], (75, 25))
            paint_image(control_panel, unit_icons["ranger"], (125, 25))
            paint_image(control_panel, unit_icons["knight"], (175, 25))
            paint_image(control_panel, unit_icons["rogue"], (225, 25))
            paint_image(control_panel, unit_icons["priest"], (275, 25))
            paint_image(control_panel, unit_icons["wizard"], (325, 25))
