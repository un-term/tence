#!/usr/bin/env python

import pygame
import unittest

from entity import *
from constants import *
from entity_group import EntityGroup

class TestEntity(unittest.TestCase):

  def test_line_sprite(self):

    entity_group = EntityGroup()

    entity_group.add_ent([LineSprite(RED,(0,0),(100,100))])

    result = len(entity_group.dict["all"].sprites())
    self.assertEqual(1, result)

  def test_baddie_collision_with_other_baddie(self):
    """baddie should continue moving when touching another baddie"""

    ent_init_list = [
      Baddie((150,150)),
      Baddie((150,150)),
      Turret((100,100))
      # Core((50,50))
    ]
    entity_group = EntityGroup(ent_init_list)
    state = State(entity_group)

    bad1_pos = state.entity_group.get_group("baddie").sprites()[0].position

    state.entity_group.get_group("all").update(step_time=1,total_time=1)

    result = state.entity_group.get_group("baddie").sprites()[0].position


    self.assertNotEqual(bad1_pos, result)
  def test_turret_shooting(self):

    entity_group = EntityGroup()

    ent_init_list = [
      Baddie((150,150),speed=0.01),
      Turret((100,100)),
      Core((50,50))
    ]
    entity_group.add_ent(ent_init_list)

    health = entity_group.dict["baddie"].sprites()[0].health #[0] first and only in list
    shoot_damage = entity_group.dict["turret"].sprites()[0].damage

    entity_group.get_group("all").update(step_time=1,total_time=1)
    entity_group.get_group("all").update(step_time=1,total_time=2)

    result = entity_group.dict["baddie"].sprites()[0].health

    health = health-shoot_damage*2

    self.assertEqual(health, result)

  def test_core_damage(self):
    entity_group = EntityGroup()
    ent_init_list = [
      Baddie((100,100),speed=10),
      Core((50,50))
    ]

    entity_group.add_ent(ent_init_list)

    core_health = entity_group.dict["core"].sprites()[0].health
    baddie_damage = entity_group.dict["baddie"].sprites()[0].damage

    # baddies do collision detection before moving
    entity_group.get_group("all").update(step_time=3,total_time=3)
    entity_group.get_group("all").update(step_time=3,total_time=6)

    result = entity_group.dict["core"].sprites()[0].health
    core_health -= baddie_damage

    self.assertEqual(core_health, result)

if __name__ == '__main__':
  unittest.main()