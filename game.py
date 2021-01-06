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
  def __init__(self, state):
    self.state = state
    self.event = pygame.event

  def check_event(self):
    for event in self.event.get():
      self._check_quit(event)
      self._check_click() # CHANGE - not dependent on pygame events

  def _check_quit(self,event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
      self.state.game_over.end_game()

  def _check_click(self):
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
      mouse_pos = pygame.mouse.get_pos()
      self.state.entity_group.add_ent([Baddie(mouse_pos, speed=30)])

class State:
  def __init__(self, entity_group):
    self.game_over = 0
    try: 
      self.entity_group = entity_group
      self.entity_group.state = self
    except: raise Exception("entity group not defined")

    self.grid = (20,20)

    self.clock = pygame.time.Clock()

    self.total_time = 0
    self.step_time = 0
    self.step = 0

  def end_game(self):
    self.game_over = 1

class Game:
  def __init__(self, state, gui=None, event=None,sound=None):
    try: self.state = state
    except: raise Exception("state not defined")
    self.gui = gui # screen
    self.event = event
    self.sound = sound

    self.winsize = (400,400)

    if gui: 
      self.gui.start_display(winsize=[640, 480])
      if event:
        self.event.game=self

  #=================================================================
  def loop(self, time_limit=0, step_limit=0, constant_step_time=0):
    """main game loop"""
 
    while not self.state.game_over:

      # update all sprites
      #-------------------------------------------------------------
      self.state.entity_group.get_group("all").update(self.state.step_time,self.state.total_time)

      if self.gui:
        self.gui.display.update()
        self.gui.screen.fill(BLACK)
        self.state.entity_group.get_group("draw").draw(self.gui.screen)
        if self.event:
          self.event.check_event()
        if self.sound:
          self.sound

      if constant_step_time == 0: 
        self.state.step_time = self.state.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        self.state.step_time = constant_step_time

      self.state.step += 1
      self.state.total_time += self.state.step_time

      if not time_limit == 0 and total_time >= time_limit:
        self.state.game_over = 1
      if not step_limit == 0 and step >= step_limit:
        self.state.game_over = 1

      # remove dead & other ephemeral entities 
      self.state.entity_group.rm_ent_from_all_groups(["remove"])

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
    Wall((180,280)),
    Wall((150,270)),
    Wall((150,260)),
    Wall((150,250)),
    Wall((150,240))
  ]
  entity_group = EntityGroup(ent_init_list)
  state = State(entity_group)

  gui = GUI()
  # sound = Sound()
  event = Event(state)
  facdustry = Game(state, gui, event, sound=None)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
