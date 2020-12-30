#!/usr/bin/env python

import pygame
import math
import random
import unittest

from general_functions import *

class TestGeneralFunctions(unittest.TestCase):

  def test_round_sig(self):
    result = round_sig(-567.3884, 3)
    self.assertEqual(-567, result)

  def test_round_sig_vector(self):
    result = round_sig_vector((75.67,1224.67775),2)
    self.assertEqual((76,1200),result)

  def test_round_vector(self):
    result = round_vector((467.4229,0.0000034),3)
    self.assertEqual((467.423,0),result)

  def test_vector_abs(self):
    result = vector_abs((-0.245,-4.8))
    self.assertEqual((0.245,4.8),result)

  def test_pol2cart(self):
    result = pol2cart((1,3*(math.pi*0.5)))
    result = round_vector((result), 6)
    self.assertEqual((0,-1), result)

  def test_cart2pol(self):
    # result = cart2pol((2,2))
    # result = round_vector((result), 2)
    # self.assertEqual((2.83,round(math.pi/4.0,2)), result)
    result = cart2pol((-2,-3))
    result = round_vector((result), 2)
    self.assertEqual((3.61,4.12), result)

  def test_rad2deg(self):
    result = rad2deg(math.pi/4.0)
    result = round(result, 2)
    self.assertEqual(45.00, result)

  def test_vector_add(self):
    result = vector_add((-2,3),(1,-3))
    self.assertEqual((-1,0),result)

  def test_vector_subtract(self):
    result = vector_subtract((2,4),(3,10))
    self.assertEqual((-1,-6),result)

  def test_vector_scalar_mult(self):
    result = vector_scalar_mult((10,5),0.5)
    self.assertEqual((5,2.5),result)
 
  def test_magnitude(self):
    result = magnitude((3,4))
    self.assertEqual(5,result)

  def test_unit_vector(self):
    result = unit_vector((5,5))
    result = round_sig_vector(result, 3)
    self.assertEqual((0.707,0.707), result)

  def test_vector_vector_midpoint(self):
    result = vector_vector_midpoint((1,1),(3,3))
    self.assertEqual((2,2), result)

  def test_grid_snap_vector(self):
    result = grid_snap_vector((20,20),(127.44, 9.0))
    self.assertEqual((120.0,0), result)

  def test_calc_const_velocity(self):
    result = calc_const_velocity(mover=(125,275), target=(100,200), speed=10)
    result = round_vector(result,1)
    self.assertEqual((-3.2,-9.5), result)

  def test_new_position(self):
    result = new_position(position=(125,275),velocity=(-3.2,-9.5),time=2)
    result = round_vector(result,1)
    self.assertEqual((118.6,256.0), result)
 
if __name__ == '__main__':
  unittest.main()


