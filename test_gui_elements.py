#!/usr/bin/env python

import pygame
import math
import random
import unittest
from unittest.mock import Mock

import game
import entity_group
from general_functions import *
import gui_elements
import entity

class TestGUI(unittest.TestCase):

    def test_gui(self):
        pygame.font.init()
        try: pygame.font.get_init()
        except: raise Exception("Fonts not initialising")

        ent_init_list = [
            # Baddie((200,400),speed=50.0),
            entity.Turret((250,250)),
            entity.Turret((450,250)),
            entity.Core((350,350)),
            entity.Turret((250,450)),
            entity.Turret((450,450))
        ]
        entity_group_obj = entity_group.EntityGroup(ent_init_list)
        state = game.State(entity_group_obj)

        # entity_group.add_ent(wall_list)
        gui = gui_elements.GUI(state)

        self.assertTrue(True)

    def test_camera(self):
        parent = Mock()
        size = (10,10)
        ent_init_list = [ entity.Turret((5,5)) ]
        entity_group_obj = entity_group.EntityGroup(ent_init_list)
        state = game.State(entity_group_obj)

        camera = gui_elements.Camera(parent, state, size)
        camera.specific_setup((0,0))

        print("camera top left: ",camera.map_rect.topleft)
        camera.capture()
        print(camera.ui_children[0].camera_rect.center)
        
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
