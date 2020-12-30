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
  
    entity_group = EntityGroup(1)

    entity_group.add_ent(ent_init_list)

    entity_group.add_ent([Baddie((200,100),speed=30.0)])

    # print(entity_group.dict["all"].sprites())
    # print(entity_group.dict)

    result = len(entity_group.dict["all"].sprites())
    self.assertEqual(8, result)

  def test_add_ent_to_remove(self):

    ent_init_list = [
      Baddie((200,400),speed=30.0),
      Turret((100,150)),
      Core((200,50)),
      Wall((160,280)),
      Wall((170,280))
    ]
  
    entity_group = EntityGroup(1)
    entity_group.add_ent(ent_init_list)
    entity_group.add_ent([Baddie((200,100),speed=30.0)], ["remove"])

    result = len(entity_group.dict["remove"].sprites())
    self.assertEqual(1, result)

  def test_delete_remove_ents(self):

    ent_init_list = [
      Baddie((200,400),speed=30.0),
      Turret((100,150)),
      Core((200,50)),
      Wall((160,280)),
      Wall((170,280))
    ]
  
    entity_group = EntityGroup(1)
    entity_group.add_ent(ent_init_list,["remove"])
    result = len(entity_group.dict["remove"].sprites())

    entity_group.remove_ent_from_group(["remove"])
    result -= len(entity_group.dict["remove"].sprites())
    self.assertEqual(5, result)

  def test_dict_group_get(self):

    ent_init_list = [
      Baddie((200,400),speed=30.0),
      Turret((100,150))
    ]

    entity_group = EntityGroup(game_ref="1")
    entity_group.add_ent(ent_init_list)   

    result = len(entity_group.get_group("all"))
    self.assertEqual(2, result)

  # def test_dict_special_len(self):

  #   ent_init_list = [
  #     Baddie((200,400),speed=30.0),
  #     Turret((100,150)),
  #     Core((200,50)),
  #     Wall((160,280)),
  #     Wall((170,280))
  #   ]

  #   entity_group = EntityGroup(game_ref="1")
  #   entity_group.add_ent(ent_init_list)   

  #   result = len(entity_group)
  #   self.assertEqual(7, result)

  # def test_dict_special_get(self):

  #   ent_init_list = [
  #     Baddie((200,400),speed=30.0),
  #     Turret((100,150))
  #   ]

  #   entity_group = EntityGroup(game_ref="1")
  #   entity_group.add_ent(ent_init_list)   

  #   result = len(entity_group["all"].sprites())
  #   self.assertEqual(2, result)

  # def test_dict_special_set(self):

  #   ent_init_list = [
  #     Baddie((200,400)),
  #     Turret((100,150))
  #   ]

  #   entity_group = EntityGroup(game_ref="1")
  #   entity_group.add_ent(ent_init_list)   


  #   print(entity_group["all"])

  #   result = 0
  #   self.assertEqual(7, result)

if __name__ == '__main__':
  unittest.main()

