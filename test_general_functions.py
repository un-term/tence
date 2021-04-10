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

    def test_sort_vector_small_big(self):
        result = sort_vector_small_big((20,4),(20,1))
        self.assertLess(result[0][1],result[1][1])

    def test_gen_coords_from_range(self):
        start=(5,7)
        end=(21,11)
        points = gen_coords_from_range(start,end,spacing=3)
        result = len(points)
        self.assertEqual(5+1,result)

    def test_find_closest_vector(self):
        vectors = [(1,1),(-2,3),(4,4),(10,20)]
        ref_vector = (-3.4,5)
        result = find_closest_vector(ref_vector,vectors)
        self.assertEqual(vectors[1],result)

    def test_snap_to_nearest_axis(self):
        start = (5,5)
        end = (6,20)
        new_end = snap_to_nearest_axis(start, end)
        self.assertEqual((5,20),new_end)

    def test_vector_convert_to_integer(self):
        result = vector_convert_to_integer((17.7,12.2))
        self.assertEqual((18,12),result)

 
if __name__ == '__main__':
    unittest.main()


