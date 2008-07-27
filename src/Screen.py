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
from geometry import (manhattan_dist, normalize_rect, rect_contains_point,
                      rect_from_center_and_size, rect_intersects_rect,
                      vector_add, vector_mul)
from Task import AttackTask, BuildTask, MoveTask, ProduceTask, StepTask
from Unit import Building, Golem, Hero, Minion, Monk, Priest, Tavern


class Screen(object):

    def __init__(self):

        root = os.path.dirname(__file__)
        while (root != '/'
               and not os.path.isfile(os.path.join(root, 'siblings.root'))):
            root = os.path.dirname(root)
        self.root = root

        pygame.init()

        self.PIXELS_PER_METER_X = 45
        self.PIXELS_PER_METER_Y = 30
        self.SCROLL_X, self.SCROLL_Y = 50, 50

        self.selection = set()
        self.screen_x, self.screen_y = 0, 0
        self.mouse_button_down_pos = None

        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Siblings in Arms')
        self.screen = pygame.display.get_surface()

        self.map_rect = pygame.Rect((0, 0), (800, 500))
        self.control_rect = pygame.Rect((0, 500), (800, 100))
        self.minimap_rect = pygame.Rect((0, 450), (150, 150))
        self.button_rect = pygame.Rect((650, 450), (150, 150))

        self.map_panel = self.screen.subsurface(self.map_rect)
        self.control_panel = self.screen.subsurface(self.control_rect)
        self.minimap_panel = self.screen.subsurface(self.minimap_rect)
        self.button_panel = self.screen.subsurface(self.button_rect)

        self.control_panel.fill(pygame.color.Color('gray'))
        pygame.draw.line(self.control_panel, pygame.color.Color('black'),
                         (0, 0), (800, 0))

        self.unit_images = {}
        self.team_colors = dict(cyan=(0, 255, 255), green=(0, 255, 0),
                                red=(255, 0, 0), yellow=(255, 255, 0))
        self.team_images = {}
        self.unit_icons = {}

        self.load_unit_images()

    def load_image(self, name):
        path = os.path.join(self.root, 'data', name + '.png')
        image = pygame.image.load(path).convert_alpha()
        image.set_colorkey((0, 0, 255))
        return image

    def create_team_image(self, image, team_color, team_colorkey=(0, 255, 0)):
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

    def load_unit_images(self):
        for cls in (Hero.__subclasses__() + Building.__subclasses__()
                    + Minion.__subclasses__()):
            name = cls.__name__.lower()
            self.unit_images[cls] = image = self.load_image(name)
            for team, team_color in self.team_colors.iteritems():
                team_image = self.create_team_image(image, team_color)
                self.team_images[team, cls] = team_image
            self.unit_icons[cls] = self.load_image(name + '-icon')

    def to_screen_coords(self, point, screen_size):
        x, y = point
        width, height = screen_size
        return (int(x * self.PIXELS_PER_METER_X) - self.screen_x,
                int(height - y * self.PIXELS_PER_METER_Y) - self.screen_y)

    def to_world_coords(self, point, screen_size):
        x, y = point
        width, height = screen_size
        return (float(x + self.screen_x) / self.PIXELS_PER_METER_X,
                float(height - y - self.screen_y) / self.PIXELS_PER_METER_Y)

    def interpolate_pos(self, game, unit):
        if (unit.task_stack and type(unit.task_stack[-1]) is StepTask
            and unit.task_stack[-1].step_time):
            task = unit.task_stack[-1]
            origin_point = game.cell_to_point(task.origin)
            dest_point = game.cell_to_point(task.dest)
            progress = ((game.time - task.departure_time)
                        / task.step_time)
            progress = max(0, min(1, progress))
            return vector_add(vector_mul(origin_point, 1 - progress),
                              vector_mul(dest_point, progress))
        else:
            return game.cell_to_point(unit.cell)

    def sorted_units(self, game):
        units = []
        for unit in game.units:
            unit_pos = self.interpolate_pos(game, unit)
            screen_pos = self.to_screen_coords(unit_pos,
                                               self.map_panel.get_size())
            screen_x, screen_y = screen_pos
            units.append((screen_y, screen_x, unit))
        units.sort()
        return units

    def paint_image(self, surface, image, pos):
        x, y = pos
        width, height = image.get_size()
        surface.blit(image, (x - width // 2, y - height // 2))

    def update(self, game):
        self.selection &= game.units
        self.handle_events(game)
        self.update_screen(game)

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_UP:
                    self.screen_y -= self.SCROLL_Y
                elif event.key == K_DOWN:
                    self.screen_y += self.SCROLL_Y
                elif event.key == K_LEFT:
                    self.screen_x -= self.SCROLL_X
                elif event.key == K_RIGHT:
                    self.screen_x += self.SCROLL_X
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_button_down_pos = event.pos
            elif event.type == MOUSEBUTTONUP:
                if (self.mouse_button_down_pos is not None
                    and manhattan_dist(event.pos, self.mouse_button_down_pos)
                    <= 6):
                    self.handle_click_event(event, game)
                else:
                    self.handle_rect_event(self.mouse_button_down_pos, event,
                                           game)
                self.mouse_button_down_pos = None

    def handle_click_event(self, event, game):
        x, y = event.pos
        if self.minimap_rect.collidepoint(x, y):
            self.handle_minimap_event(event, game)
        if self.button_rect.collidepoint(x, y):
            self.handle_button_event(event, game)
        elif self.map_rect.collidepoint(x, y):
            if event.button == 1:
                self.handle_select_event(event, game)
            else:
                self.handle_command_event(event, game)

    def handle_select_event(self, event, game):
        clicked_unit = None
        clicked_unit_pos = None
        for unit in game.units:
            unit_pos = game.cell_to_point(unit.cell)
            screen_pos = self.to_screen_coords(unit_pos,
                                               self.map_panel.get_size())
            surface = self.unit_images[type(unit)]
            surface_size = surface.get_size()
            rect = rect_from_center_and_size(screen_pos, surface_size)
            if (rect_contains_point(rect, event.pos)
                and (clicked_unit is None
                     or unit_pos[1] < clicked_unit_pos[1])):
                clicked_unit = unit
                clicked_unit_pos = unit_pos

        if clicked_unit is not None:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if clicked_unit in self.selection:
                    self.selection.remove(clicked_unit)
                else:
                    self.selection.add(clicked_unit)
            else:
                self.selection.clear()
                self.selection.add(clicked_unit)

    def handle_command_event(self, event, game):
        clicked_unit = None
        clicked_unit_pos = None
        for unit in game.units:
            unit_pos = game.cell_to_point(unit.cell)
            screen_pos = self.to_screen_coords(unit_pos,
                                               self.map_panel.get_size())
            surface = self.unit_images[type(unit)]
            surface_size = surface.get_size()
            rect = rect_from_center_and_size(screen_pos, surface_size)
            if (rect_contains_point(rect, event.pos)
                and (clicked_unit is None
                     or unit_pos[1] < clicked_unit_pos[1])):
                clicked_unit = unit
                clicked_unit_pos = unit_pos

        point = self.to_world_coords(event.pos, self.map_panel.get_size())
        cell = game.point_to_cell(point)
        for unit in self.selection:
            if (unit.speed is not None
                and (clicked_unit is None
                     or unit.color == clicked_unit.color)):
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    game.stop_unit(unit)
                game.add_task(unit, MoveTask(cell))
            elif unit.damage is not None and unit.color != clicked_unit.color:
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    game.stop_unit(unit)
                game.add_task(unit, AttackTask(clicked_unit))

    def handle_minimap_event(self, event, game):
        pass

    def handle_button_event(self, event, game):
        x, y = event.pos
        col = (x - self.button_rect.left) // 50
        row = (y - self.button_rect.top) // 50
        button = col + 3 * row
        if len(self.selection) == 1:
            unit = list(self.selection)[0]
            if type(unit) is Tavern:
                classes = Hero.__subclasses__()
                if 0 <= button < len(classes):
                    game.add_task(unit, ProduceTask(classes[button]))
            elif type(unit) is Monk:
                classes = Building.__subclasses__()
                if 0 <= button < len(classes):
                    game.add_task(unit, BuildTask(classes[button]))
            elif type(unit) is Priest:
                if button == 0:
                    game.add_task(unit, ProduceTask(Golem))

    def handle_rect_event(self, old_pos, event, game):
        if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.selection.clear()
        selection_rect = normalize_rect((old_pos, event.pos))
        for unit in game.units:
            unit_pos = game.cell_to_point(unit.cell)
            screen_pos = self.to_screen_coords(unit_pos,
                                               self.map_panel.get_size())
            surface = self.unit_images[type(unit)]
            surface_size = surface.get_size()
            surface_rect = rect_from_center_and_size(screen_pos, surface_size)
            if rect_intersects_rect(selection_rect, surface_rect):
                self.selection.add(unit)

    def update_screen(self, game):
        self.paint_map_panel(game)
        self.paint_control_panel(game)
        pygame.display.update()

    def paint_map_panel(self, game):
        self.map_panel.fill(pygame.color.Color('#886644'))
        for screen_y, screen_x, unit in self.sorted_units(game):
            screen_pos = screen_x, screen_y
            image = self.team_images[unit.color, type(unit)]
            if unit in self.selection:
                width, height = image.get_size()
                radius = max(width, height) // 2
                pygame.draw.circle(self.map_panel, pygame.color.Color('black'),
                                   screen_pos, radius - 1, 3)
                pygame.draw.circle(self.map_panel, pygame.color.Color('green'),
                                   screen_pos, radius - 2, 1)
            self.paint_image(self.map_panel, image, screen_pos)
        self.paint_selection_rect(game)

    def paint_selection_rect(self, game):
        if self.mouse_button_down_pos is not None:
            old_x, old_y = self.mouse_button_down_pos
            new_x, new_y = pygame.mouse.get_pos()
            x = min(old_x, new_x)
            y = min(old_y, new_y)
            width = abs(old_x - new_x)
            height = abs(old_y - new_y)
            pygame.draw.rect(self.map_panel, pygame.color.Color('black'),
                             pygame.Rect(x, y, width, height), 3)
            pygame.draw.rect(self.map_panel, pygame.color.Color('green'),
                             pygame.Rect(x, y, width, height), 1)

    def paint_button(self, button, image):
        row, col = divmod(button, 3)
        self.paint_image(self.button_panel, image,
                         (25 + col * 50, 25 + row * 50))

    def paint_control_panel(self, game):
        self.paint_minimap_panel(game)
        self.paint_button_panel(game)

    def paint_minimap_panel(self, game):
        self.minimap_panel.fill(pygame.color.Color('gray'))
        pygame.draw.line(self.minimap_panel, pygame.color.Color('black'),
                         (0, 0), (self.minimap_rect.width, 0))
        pygame.draw.line(self.minimap_panel, pygame.color.Color('black'),
                         (self.minimap_rect.width - 1, 0),
                         (self.minimap_rect.width - 1,
                          self.minimap_rect.height))

    def paint_button_panel(self, game):
        self.button_panel.fill(pygame.color.Color('gray'))
        pygame.draw.line(self.button_panel, pygame.color.Color('black'),
                         (0, 0), (self.button_rect.width, 0))
        pygame.draw.line(self.button_panel, pygame.color.Color('black'),
                         (0, 0), (0, self.button_rect.height))
        if len(self.selection) == 1:
            unit = list(self.selection)[0]
            if type(unit) is Tavern:
                for button, cls in enumerate(Hero.__subclasses__()):
                    self.paint_button(button, self.unit_icons[cls])
            elif type(unit) is Monk:
                for button, cls in enumerate(Building.__subclasses__()):
                    self.paint_button(button, self.unit_icons[cls])
            elif type(unit) is Priest:
                self.paint_button(0, self.unit_icons[Golem])
