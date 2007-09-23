import pygame, sys,os
from pygame.locals import * 

from Warrior import Warrior
from GameEngine import GameEngine
 
pygame.init() 

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Siblings in Arms') 
screen = pygame.display.get_surface() 

PIXELS_PER_METER = 20

warrior_path = os.path.join('data', 'warrior.png')
warrior_surface = pygame.image.load(warrior_path)

game = GameEngine()
game.add_unit(Warrior(), (2, 3))
game.add_unit(Warrior(), (-3, 1))
game.add_unit(Warrior(), (1, -2))

def handle_events(events):
   for event in events: 
      if event.type == QUIT: 
         sys.exit(0) 
      else: 
         print event 

def to_screen_pos(pos, screen_size):
   return (int(screen_size[0] / 2 + pos[0] * PIXELS_PER_METER),
           int(screen_size[1] / 2 - pos[1] * PIXELS_PER_METER))

def redraw_screen(screen, game):
   screen.fill(pygame.color.Color('gold'))
   for unit in game.units:
      screen.blit(warrior_surface, to_screen_pos(unit.pos, screen.get_size()))
   pygame.display.flip() 

while True: 
   handle_events(pygame.event.get())
   redraw_screen(screen, game)
