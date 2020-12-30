#!/usr/bin/env python

import pygame
import math
import random
# from multipledispatch import dispatch

# user modules
from entity import *
from general_functions import *
from entity_group import EntityGroup

WINSIZE = [640, 480]

def draw_lines(surface,object_group):
  for object in object_group:
    if object.line:
      pygame.draw.aaline(surface,object.line.colour,object.line.start,object.line.end)

# set GUI to 1 to display
class Game:
  def __init__(self, ent_init_list, GUI=1,sound=1):
    self.game_over = 0
    # screen
    self.GUI = GUI
    self.sound = sound

    self.winsize = (400,400)
    self.grid = (20,20)

    self.clock = pygame.time.Clock()
    self.events = pygame.event

    # create objects and check if they exist to use them
    if self.GUI: # includes sounds
      self.screen = pygame.display.set_mode(self.winsize)
    if self.sound:
      pygame.mixer.init()
      self.laser_sound = pygame.mixer.Sound("pew.ogg")
      # self.sound_list = [] # load sounds list

    self.entity_group = EntityGroup(self) # linking objects
    self.entity_group.add_ent(ent_init_list)

  # mouse & keyboard input
  def check_events(self):
    for event in self.events.get():

      # quiting pygame
      if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        self.game_over = 1
        break
      # mouse button baddie creation
      mouse_buttons = pygame.mouse.get_pressed()
      if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()

        # new_baddie_list = [Baddie(mouse_pos, speed=30)]
        
        self.entity_group.add_ent([Baddie(mouse_pos, speed=30)])
        # self.add_sprites_to_groups(new_baddie_list)

  #=================================================================
  def loop(self, time_limit=0, step_limit=0, constant_step_time=0):
    """main game loop"""
    total_time = 0
    step_time = 0
    step = 0
 
    while not self.game_over:

      # update all sprites
      #-------------------------------------------------------------
      self.entity_group.get_group("all").update(step_time,total_time)

      if self.GUI:
        pygame.display.update()

        self.check_events()

        self.screen.fill(BLACK)
        self.entity_group.get_group("draw").draw(self.screen)
        # self.ent_group_dict["laser"].draw(self.screen)
        # draw_lines(self.screen,self.ent_group_dict["turret"])
        # alllines.draw(self.screen)

      if constant_step_time == 0: 
        step_time = self.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        step_time = constant_step_time

      step += 1
      total_time += step_time

      if not time_limit == 0 and total_time >= time_limit:
        # global continue_game
        self.game_over = 1
      if not step_limit == 0 and step >= step_limit:
        # global continue_game
        self.game_over = 1

      # remove dead
      self.entity_group.remove_ent_from_group(["remove"])

  pygame.quit()

def main():

  ent_init_list = [
    Baddie((200,400),speed=50.0),
    Turret((300,150)),
    Turret((100,150)),
    Core((200,50)),
    Wall((150,280)),
    Wall((160,280)),
    Wall((170,280)),
    Wall((180,280))
  ]

  facdustry = Game(ent_init_list, GUI=1, sound=0)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
