#!/usr/bin/env python

import pygame
import math
import random
# from multipledispatch import dispatch

# user modules
from entity import *
from general_functions import *
from entity_group import EntityGroup

class GUI:
  def __init__(self):
    self.display = pygame.display
  def start_display(self,winsize=[640, 480]):
    self.screen = self.display.set_mode(winsize)

# class Sound:
#   """CHANGE: import list of sound files"""
#   def __init__(self):
#     self.mixer = pygame.mixer
#     self.mixer.init()
#     self.list = [pygame.mixer.Sound("pew.ogg")]

#   def play(self):


class Event:
  def __init__(self):
    self.game = None
    self.event = pygame.event

  def check_event(self):
    for event in self.event.get():
      self._check_quit(event)
      self._check_click()

  def _check_quit(self,event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
      self.game.game_over = 1

  def _check_click(self):
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
      mouse_pos = pygame.mouse.get_pos()
      self.game.entity_group.add_ent([Baddie(mouse_pos, speed=30)])


class Game:
  def __init__(self, ent_init_list, gui=None, event=None,sound=None):
    self.game_over = 0
    # screen
    self.gui = gui
    self.event = event
    self.sound = sound

    self.winsize = (400,400)
    self.grid = (20,20)

    self.clock = pygame.time.Clock()

    self.entity_group = EntityGroup() # linking objects
    self.entity_group.add_ent(ent_init_list)

    if gui: 
      self.gui.start_display(winsize=[640, 480])
      if event:
        self.event.game=self

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

      if self.gui:
        self.gui.display.update()
        self.gui.screen.fill(BLACK)
        self.entity_group.get_group("draw").draw(self.gui.screen)
        if self.event:
          self.event.check_event()

      if constant_step_time == 0: 
        step_time = self.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        step_time = constant_step_time

      step += 1
      total_time += step_time

      if not time_limit == 0 and total_time >= time_limit:
        self.game_over = 1
      if not step_limit == 0 and step >= step_limit:
        self.game_over = 1

      # remove dead & other ephemeral entities 
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

  gui = GUI()
  # sound = Sound()
  event = Event()

  facdustry = Game(ent_init_list,gui,event, sound=None)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
