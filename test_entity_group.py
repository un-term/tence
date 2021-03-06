#!/usr/bin/env python

import pygame
import unittest

from entity import *
from entity_group import EntityGroup
from game import State

class TestEntityGroup(unittest.TestCase):

    def test_add_ent(self):

        ent_init_list = [
            Baddie((200,400),speed=30.0),
            Turret((300,150)),
            Turret((100,150)),
            Core((200,50)),
            Wall((160,280)),
            Wall((170,280)),
            Wall((180,280))
        ]
        entity_group = EntityGroup(ent_init_list)
        state = State(entity_group)

        state.entity_group.add_ent([Baddie((200,100),speed=30.0)])

        result = len(state.entity_group.dict["all"].sprites())
        self.assertEqual(8, result)

    def test_add_ent_to_remove(self):

        ent_init_list = [
            Baddie((200,400),speed=30.0),
            Turret((100,150)),
            Core((200,50)),
            Wall((160,280)),
            Wall((170,280))
        ]
      
        entity_group = EntityGroup(ent_init_list)
        state = State(entity_group)
        state.entity_group.add_ent([Baddie((200,100),speed=30.0)], ["remove"])

        result = len(state.entity_group.dict["remove"].sprites())
        self.assertEqual(1, result)

    def test_delete_remove_ents(self):

        ent_init_list = [
            Baddie((200,400),speed=30.0),
            Turret((100,150)),
            Core((200,50)),
            Wall((160,280)),
            Wall((170,280))
        ]
      
        entity_group = EntityGroup([])
        state = State(entity_group)

        state.entity_group.add_ent(ent_init_list,["remove"])
        result = len(state.entity_group.dict["remove"].sprites())

        state.entity_group.rm_ent_from_all_groups(["remove"])
        result -= len(state.entity_group.dict["remove"].sprites())
        self.assertEqual(5, result)

    def test_dict_group_get(self):

        ent_init_list = [
            Baddie((200,400),speed=30.0),
            Turret((100,150))
        ]

        entity_group = EntityGroup(ent_init_list)
        state = State(entity_group)

        result = len(state.entity_group.get_group("all"))
        self.assertEqual(2, result)

    def test_dict_missing_group_get(self):
        """group missing - test response"""
        ent_init_list = [
            Baddie((200,400),speed=30.0),
            Turret((100,150))
        ]

        entity_group = EntityGroup(ent_init_list)
        state = State(entity_group)


        result = entity_group.get_group("core")
        self.assertEqual(None, result)

    def test_adding_duplicate(self):
        """duplicates should not be added"""

        b = Baddie((200,400))

        entity_group = EntityGroup([])
        state = State(entity_group)

        state.entity_group.add_ent([b])   

        state.entity_group.add_ent([b])

        result = len(state.entity_group.get_group("all"))
        self.assertEqual(1, result)

    def test_finding_overlap(self):

        b1 = Baddie((200,400))
        b2 = Baddie((220,420))
        c = Core((100,100))
        t = Turret((150,150))


        entity_group = EntityGroup([])
        state = State(entity_group)

        state.entity_group.add_ent([b1,b2,c,t])
        state.entity_group.add_ent([b1,c],["collision"])
        overlap = state.entity_group.find_overlap("all","collision")

        result = len(overlap)

        self.assertEqual(2, result)

    def test_empty_group_only(self):

        b1 = Baddie((200,400))
        b2 = Baddie((220,420))
        c = Core((100,100))
        t = Turret((150,150))

        entity_group = EntityGroup([])
        state = State(entity_group)

        state.entity_group.add_ent([b1,b2,c,t], ["test"])

        before_size = len(state.entity_group.get_group("test"))
        entity_group.empty_this_group_only("test")
        after_size = len(state.entity_group.get_group("test"))

        result = before_size - after_size

        self.assertEqual(4, result)


if __name__ == '__main__':
    unittest.main()


