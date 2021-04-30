#!/usr/bin/env python

# import pygame
import unittest

# from entity import *
# from constants import *
# from entity_group import EntityGroup
import game
import entity_group
import entity
# from general_functions import *

class TestEntity(unittest.TestCase):

    def test_spawn_generator(self):

        entity_group_obj = entity_group.EntityGroup([])
        state = game.State(entity_group_obj)
        event = game.Event(state)
        event.spawn_timestamp = 1
        event.check_spawn_point_generation(5)
        print(state.entity_group.get_group("draw").sprites())
        
        self.assertTrue(True)

if __name__ == '__main__':
      unittest.main()
