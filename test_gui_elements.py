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

    def test_1_coords_map_to_camera_topleft(self):
        '''Based on map_camera_zoom_pan.drawio
        scaled x10'''
        pygame.font.init()
        try: pygame.font.get_init()
        except: raise Exception("Fonts not initialising")

        ent_init_list = [
            entity.Turret((-20,30))
        ]
        entity_group_obj = entity_group.EntityGroup(ent_init_list)
        state = game.State(entity_group_obj)

        display = Mock()
        gui = gui_elements.GUI(display, state, camera_size=(120,120))

        gui.move_camera((10,20))
        gui.zoom_camera(1)
        gui.draw() # draw_list emptied at start of next draw

        turret_rect = gui.ui_elements["camera"].draw_list[0][0]

        self.assertEqual((0,80), turret_rect.center)

    def test_2_click_with_zoom_pan(self):
        '''Based on map_camera_zoom_pan.drawio
        scaled x10'''

        camera = gui_elements.Camera(None, None, (120,120))
        camera.specific_setup((0,0))
        camera.zoom_level = 2 # 1/zoom_level
        camera.map_rect.move_ip((10,20))

        mouse_pos = (0,80)
        result = camera.translate_camera_vector_to_map_vector(mouse_pos)

        self.assertEqual((-20,30), result)

    # def test_camera(self):
    #     parent = Mock()
    #     size = (10,10)
    #     ent_init_list = [ entity.Turret((5,5)) ]
    #     entity_group_obj = entity_group.EntityGroup(ent_init_list)
    #     state = game.State(entity_group_obj)

    #     camera = gui_elements.Camera(parent, state, size)
    #     camera.specific_setup((0,0))
    #     camera.zoom_level = 2
    #     camera.map_rect.move_ip

    #     # call gui.draw
        
    #     self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
