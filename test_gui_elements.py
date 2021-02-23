#!/usr/bin/env python

import pygame
import math
import random
import unittest
from unittest.mock import Mock

from general_functions import *
from gui_elements import *
import entity

class TestSurfaces(unittest.TestCase):

    # def test_screen(self):

    #     display = Mock()
    #     screen = Screen(None,display,(700,700))
    #     # map = Map(screen,menu_height=40)

    #     if screen:
    #       result = True
    #     self.assertTrue(result) 

    def test_map(self):

        display = Mock()
        screen = Screen(None,display,(700,700))
        map = Map(screen,menu_height=40)
        menu = Menu(screen,menu_height=40)
        menu_box = MenuBox(menu)
        entity_menu_items = [entity.Core((0,0)),entity.Turret((0,0)),entity.Wall((0,0)),entity.Spawn((0,0))]
        menu_box.add_menu_entity(entity_menu_items)
        for item in menu_box.ui_children:
            print(item.position)
        # menu = Menu()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()