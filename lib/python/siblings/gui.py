# Copyright (c) 2007 Mikael Lind
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pygame, pygame.transform, sys, os, math
from pygame.locals import *
from geometry import *
from Task import AttackTask, BuildTask, MoveTask
from Unit import Building, Hero, Tavern


root = os.path.dirname(__file__)
while root != '/' and not os.path.isfile(os.path.join(root, 'siblings.root')):
    root = os.path.dirname(root)

pygame.init() 

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Siblings in Arms')
screen = pygame.display.get_surface()

map_rect = pygame.Rect((0, 0), (800, 550))
control_rect = pygame.Rect((0, 550), (800, 50))
map_surface = screen.subsurface(map_rect)
control_panel = screen.subsurface(control_rect)

def load_image(name):
    path = os.path.join(root, 'data', name + '.png')
    image = pygame.image.load(path).convert_alpha()
    image.set_colorkey((0, 0, 255))
    return image

unit_images = {}
team_colors = dict(cyan=(0, 255, 255), green=(0, 255, 0), red=(255, 0, 0),
                   yellow=(255, 255, 0))
team_images = {}
unit_icons = {}

def create_team_image(image, team_color, team_colorkey=(0, 255, 0)):
    team_image = image.copy()
    team_image.lock()
    team_r, team_g, team_b = team_color
    for x in xrange(image.get_width()):
        for y in xrange(image.get_height()):
            r, g, b, a = image.get_at((x, y))
            if (r, g, b) == team_colorkey:
                team_image.set_at((x, y), (team_r, team_g, team_b, a))
    team_image.unlock()
    return team_image

def load_unit_images():
    for cls in Hero.__subclasses__() + Building.__subclasses__():
        name = cls.__name__.lower()
        unit_images[cls] = image = load_image(name)
        for team, team_color in team_colors.iteritems():
            team_images[team, cls] = create_team_image(image, team_color)
        unit_icons[cls] = load_image(name + '-icon')

load_unit_images()

PIXELS_PER_METER_X = 45
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
    units = game_engine.units.values()
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
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
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
    for unit in game_engine.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[type(unit)]
        surface_size = surface.get_size()
        rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if (rectangle_contains_point(rect, event.pos)
            and (clicked_unit is None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit

    if clicked_unit is not None:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if clicked_unit in selection:
                selection.remove(clicked_unit)
                print 'Removed %s from selection.' % clicked_unit
            else:
                selection.add(clicked_unit)
                print 'Added %s to selection.' % clicked_unit
        else:
            selection.clear()
            selection.add(clicked_unit)
            print 'Selected %s.' % clicked_unit

def handle_command_event(event, game_engine):
    clicked_unit = None
    for unit in game_engine.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[type(unit)]
        surface_size = surface.get_size()
        rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if (rectangle_contains_point(rect, event.pos)
            and (clicked_unit is None or unit.pos[1] < clicked_unit.pos[1])):
            clicked_unit = unit

    if clicked_unit is None:
        pos = to_world_coords(event.pos, map_surface.get_size())
        cell = game_engine.pos_to_cell(pos)
        for unit in selection:
            if unit.speed is not None:
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if unit.task is not None:
                        unit.task.aborting = True
                    del unit.task_queue[:]
                    print '%s aborted all tasks.' % unit
                unit.task_queue.append(MoveTask(game_engine, unit, cell))
                print '%s added waypoint %s.' % (unit, cell)
    else:
        for unit in selection:
            if unit.damage and unit.player != clicked_unit.player:
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if unit.task is not None:
                        unit.task.aborting = True
                    del unit.task_queue[:]
                    print '%s aborted all tasks.' % unit
                unit.task_queue.append(AttackTask(game_engine, unit,
                                                  clicked_unit))
                print ('%s targeted %s.' % (unit, clicked_unit))

def handle_control_event(event, game_engine):
    x, y = event.pos
    button = x // 50
    if len(selection) == 1:
        unit = iter(selection).next()
        if type(unit) is Tavern:
            classes = Hero.__subclasses__()
            if 0 <= button < len(classes):
                unit.task_queue.append(BuildTask(game_engine, unit,
                                                 classes[button]))

def handle_rectangle_event(old_pos, event, game_engine):
    global selection
    selection_rect = normalize_rectangle((old_pos, event.pos))
    new_selection = set()
    for unit in game_engine.units.itervalues():
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        surface = unit_images[type(unit)]
        surface_size = surface.get_size()
        surface_rect = rectangle_from_center_and_size(screen_pos, surface_size)
        if rectangle_intersects_rectangle(selection_rect, surface_rect):
            new_selection.add(unit)

    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
        old_size = len(selection)
        selection |= new_selection
        print 'Added %d unit(s) to selection.' % (len(selection) - old_size)
    else:
        selection = new_selection
        print 'Selected %d unit(s).' % len(selection)

def update_screen(game_engine):
    paint_map_surface(game_engine)
    paint_control_panel(game_engine)
    pygame.display.flip()

def paint_map_surface(game_engine):
    map_surface.fill(pygame.color.Color('#886644'))
    for unit in get_sorted_units(game_engine):
        screen_pos = to_screen_coords(unit.pos, map_surface.get_size())
        image = team_images[unit.player, type(unit)]
        width, height = image.get_size()
        radius = max(width, height) // 2
        if unit in selection:
            pygame.draw.circle(map_surface, pygame.color.Color('black'),
                               screen_pos, radius - 1, 3)
            pygame.draw.circle(map_surface, pygame.color.Color('green'),
                               screen_pos, radius - 2, 1)
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
        pygame.draw.rect(map_surface, pygame.color.Color('green'),
                         pygame.Rect(x, y, width, height), 1)

def paint_control_panel(game_engine):
    control_panel.fill(pygame.color.Color('gray'))
    if len(selection) == 1 and type(list(selection)[0]) is Tavern:
        for i, cls in enumerate(Hero.__subclasses__()):
            paint_image(control_panel, unit_icons[cls], (25 + i * 50, 25))
