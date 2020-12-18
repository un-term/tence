#!/usr/bin/env python

import pygame
import math
import random

# user modules
from entity import *
from general_functions import *

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

    if self.GUI: # includes sounds
      self.screen = pygame.display.set_mode(self.winsize)
    if self.sound:
      pygame.mixer.init()
      self.laser_sound = pygame.mixer.Sound("pew.ogg")
      # self.sound_list = [] # load sounds list

    self.ent_group_dict = {
      "all":pygame.sprite.Group(),
      "dead":pygame.sprite.Group()
    }
    self.create_sprite_groups(ent_init_list)
    self.add_sprites_to_groups(ent_init_list)

  def create_sprite_groups(self,entities_list):
    for entity in entities_list:
      self.ent_group_dict.update({entity.type:pygame.sprite.Group()})

  def add_sprites_to_groups(self, entities_list):
    for entity in entities_list:
      self.ent_group_dict[entity.type].add(entity)
      self.ent_group_dict["all"].add(entity)   
      #link game ref to entity
      entity.game = self

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

        new_baddie_list = [Baddie(mouse_pos, speed=30)]
        
        self.add_sprites_to_groups(new_baddie_list)

  #=================================================================
  def loop(self, time_limit=0, step_limit=0, constant_step_time=0):
    """main game loop"""
    total_time = 0
    step_time = 0
    step = 0
 
    while not self.game_over:

      # update all sprites
      #-------------------
      self.ent_group_dict["all"].update(step_time,total_time)
      # delete dead
      for ent in self.ent_group_dict["dead"]: # CHANGE
        ent.kill()
      # self.ent_group_dict["dead"].empty()

      if self.GUI:
        pygame.display.update()

        self.check_events()

        self.screen.fill(BLACK)
        self.ent_group_dict["all"].draw(self.screen)
        draw_lines(self.screen,self.ent_group_dict["turret"])
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

  pygame.quit()

def main():

  ent_init_list = [
    Baddie((200,400),speed=30.0),
    Turret((300,150)),
    Turret((100,150)),
    Core((200,50)),
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
