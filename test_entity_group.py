#!/usr/bin/env python

import pygame
import unittest

from entity import *
from entity_group import EntityGroup

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
  
    # entity_group = EntityGroup(1,ent_init_list)
    entity_group = EntityGroup(1)

    entity_group.add_ent(ent_init_list)

    entity_group.add_ent([Baddie((200,100),speed=30.0)])

    print(entity_group.dict["all"].sprites())
    print(entity_group.dict)

    # entity_group.add_ent([Turret((300,150))])

    # print(entity_group.dict["all"].sprites())
    # print(entity_group.dict)


    result = len(entity_group.dict["all"].sprites())
    self.assertEqual(8, result)

if __name__ == '__main__':
  unittest.main()


