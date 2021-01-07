#!/usr/bin/env python

import pygame
import unittest

from entity import *
from constants import *
from entity_group import EntityGroup
from game import State

class TestEntity(unittest.TestCase):

  def test_line_sprite(self):

    entity_group = EntityGroup([LineSprite(RED,(0,0),(100,100))])
    state = State(entity_group)

    result = len(entity_group.dict["all"].sprites())
    self.assertEqual(1, result)

  def test_baddie_collision_with_other_baddie(self):
    """baddie should continue moving when touching another baddie"""

    ent_init_list = [
      Baddie((148,148)), #overlapping but not exactly
      Baddie((150,150)),
      Turret((100,100)),
      Core((50,50))
    ]
    entity_group = EntityGroup(ent_init_list)
    state = State(entity_group)

    bad1_pos = state.entity_group.get_group("baddie").sprites()[0].position

    state.entity_group.get_group("all").update(step_time=1,total_time=1)
    state.entity_group.get_group("all").update(step_time=1,total_time=1)

    result = state.entity_group.get_group("baddie").sprites()[0].position


    self.assertNotEqual(bad1_pos, result)


  def test_turret_shooting(self):
    """CHANGE: assumes baddie is within range of turret"""

    ent_init_list = [
      Baddie((150,150),speed=0.01),
      Turret((100,100)),
      Core((50,50))
    ]
    entity_group = EntityGroup(ent_init_list)
    state = State(entity_group)

    health = state.entity_group.dict["baddie"].sprites()[0].health #[0] first and only in list
    shoot_damage = state.entity_group.dict["turret"].sprites()[0].damage

    state.entity_group.get_group("all").update(step_time=1,total_time=1)
    state.entity_group.get_group("all").update(step_time=1,total_time=2)

    result = state.entity_group.dict["baddie"].sprites()[0].health

    health = health-shoot_damage*2

    self.assertEqual(health, result)

  def test_core_damage(self):

    ent_init_list = [
      Baddie((100,100),speed=10),
      Core((50,50))
    ]
    entity_group = EntityGroup(ent_init_list)
    state = State(entity_group)

    core_health = state.entity_group.dict["core"].sprites()[0].health
    baddie_damage = state.entity_group.dict["baddie"].sprites()[0].damage

    # baddies do collision detection before moving
    state.entity_group.get_group("all").update(step_time=3,total_time=3)
    state.entity_group.get_group("all").update(step_time=3,total_time=6)

    result = state.entity_group.dict["core"].sprites()[0].health
    core_health -= baddie_damage

    self.assertEqual(core_health, result)

if __name__ == '__main__':
  unittest.main()