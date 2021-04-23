#!/usr/bin/env python

import pygame
import math
import random
# from multipledispatch import dispatch

# user modules
import entity
from general_functions import *
from entity_group import EntityGroup
import gui_elements

# class Sound:
#   """CHANGE: import list of sound files"""
#   def __init__(self):
#     self.mixer = pygame.mixer
#     self.mixer.init()
#     self.list = [pygame.mixer.Sound("pew.ogg")]

#   def play(self):


class UserInput:
    def __init__(self, state, gui):
        self.state = state
        self.gui = gui
        self.event = pygame.event
        self.selected_entity = None
        pygame.key.set_repeat(50)  # Allow holding down keys
        self.spawn_nb = 0

    def check(self):
        for event in self.event.get():
            self._check_quit(event)
            self._global_click_check(event) # CHANGE - not dependent on pygame events
            self._check_arrows(event)
            self._check_plus_minus(event)

    def _check_quit(self,event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            self.state.game_over.end_game()

    def _global_click_check(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self.gui.click(mouse_pos)

    def _check_arrows(self, event):
        jump = 20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.gui.move_camera((0,jump))
            elif event.key == pygame.K_UP:
                self.gui.move_camera((0,-1.0*jump))
            elif event.key == pygame.K_RIGHT:
                self.gui.move_camera((jump,0))
            elif event.key == pygame.K_LEFT:
                self.gui.move_camera((-1.0*jump,0))

    def _check_plus_minus(self, event):
        factor = 0.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                self.gui.zoom_camera(factor)
            elif event.key == pygame.K_MINUS:
                self.gui.zoom_camera(factor*-1.0)


class Event:
    def __init__(self, state):
        self.state = state
        self.spawn_timestamp = 0
        # Limits for random spawn location
        self.map_max_x_limit = self.state.max_map_size[0]*0.5
        self.map_max_y_limit = self.state.max_map_size[1]*0.5
        self.spawn_point_interval = 1  # s
        
    def generate_spawn_point(self, total_time):
        '''time in s'''
        time_diff = total_time - self.spawn_timestamp
        if time_diff > self.spawn_point_interval:
            x_pos = random.randrange(self.map_max_x_limit*-1.0, self.map_max_x_limit, 1)
            y_pos = random.randrange(self.map_max_y_limit*-1.0, self.map_max_y_limit, 1)
            spawn = entity.factory("spawn",(x_pos,y_pos))
            self.state.entity_group.add_ent([spawn])
            self.spawn_timestamp = total_time

       
class State:
    def __init__(self, entity_group):
        self.game_over = 0

        self.entity_group = entity_group
        self.entity_group.state = self

        self.grid = (20,20)
        self.max_map_size = (1000,1000)

        self.clock = pygame.time.Clock()

        self.total_time = 0
        self.tick_time = 0
        self.tick_nb = 0

        self.kill_count = 0

    def end_game(self):
        self.game_over = 1

    def set_and_get_tick(self):
        self.tick_time = self.clock.tick(60)/1000.0  # miliseconds to seconds
        self.tick_nb += 1
        self.total_time += self.tick_time


class Game:
    def __init__(self, state, event, gui=None, user_input=None, sound=None):
        try: self.state = state
        except: raise Exception("state not defined")
        self.gui = gui # screen
        self.user_input = user_input
        self.sound = sound
        self.event = event

    #===================================================================
    def loop(self):
        """main game loop"""
    
        while not self.state.game_over:

          # update all sprites
          #-------------------------------------------------------------
            self.event.generate_spawn_point(self.state.total_time)
            self.state.entity_group.get_group("all").update()

            if self.gui:
                self.gui.update()
                self.gui.draw()

                if self.user_input:
                    self.user_input.check()
                if self.sound:
                    self.sound

            # Limit map fps and get times
            self.state.set_and_get_tick()

            # remove dead & other ephemeral entities 
            self.state.entity_group.rm_ent_from_all_groups(["remove"])

    pygame.quit()


def main():

    pygame.font.init()
    try: pygame.font.get_init()
    except: raise Exception("Fonts not initialising")

    # coordinate system - right +x, down +y
    ent_init_list = [
        entity.Turret((150,150)),
        entity.Turret((-150,150)),
        entity.Core((0,0)),
        entity.Turret((150,-150)),
        entity.Turret((-150,-150))
    ]
    entity_group = EntityGroup(ent_init_list)
    state = State(entity_group)

    gui = gui_elements.GUI(pygame.display, state, camera_size=(700,700))
    # sound = Sound()
    user_input = UserInput(state, gui)
    event = Event(state)
    facdustry = Game(state, event, gui, user_input, sound=None)
    facdustry.loop()

# if python says run, then we should run
if __name__ == "__main__":
    main()
#     
