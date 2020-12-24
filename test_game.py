import unittest
import game
import math
 
class TTD(unittest.TestCase):

  def test_round_sig(self):
    result = game.round_sig(-567.3884, 3)
    self.assertEqual(-567, result)

  def test_round_sig_vector(self):
    result = game.round_sig_vector((75.67,1224.67775),2)
    self.assertEqual((76,1200),result)

  def test_round_vector(self):
    result = game.round_vector((467.4229,0.0000034),3)
    self.assertEqual((467.423,0),result)

  def test_abs_vector(self):
    result = game.abs_vector((-0.245,-4.8))
    self.assertEqual((0.245,4.8),result)

  def test_pol2cart(self):
    result = game.pol2cart((1,3*(math.pi*0.5)))
    result = game.round_vector((result), 6)
    self.assertEqual((0,-1), result)

  def test_cart2pol(self):
    # result = game.cart2pol((2,2))
    # result = game.round_vector((result), 2)
    # self.assertEqual((2.83,round(math.pi/4.0,2)), result)
    result = game.cart2pol((-2,-3))
    result = game.round_vector((result), 2)
    self.assertEqual((3.61,4.12), result)

  def test_rad2deg(self):
    result = game.rad2deg(math.pi/4.0)
    result = round(result, 2)
    self.assertEqual(45.00, result)

  def test_vector_add(self):
    result = game.vector_add((-2,3),(1,-3))
    self.assertEqual((-1,0),result)

  def test_vector_subtract(self):
    result = game.vector_subtract((2,4),(3,10))
    self.assertEqual((-1,-6),result)

  def test_vector_scalar_mult(self):
    result = game.vector_scalar_mult((10,5),0.5)
    self.assertEqual((5,2.5),result)
 
  def test_magnitude(self):
    result = game.magnitude((3,4))
    self.assertEqual(5,result)

  def test_unit_vector(self):
    result = game.unit_vector((5,5))
    result = game.round_sig_vector(result, 3)
    self.assertEqual((0.707,0.707), result)

  def test_vector_vector_midpoint(self):
    result = game.vector_vector_midpoint((1,1),(3,3))
    self.assertEqual((2,2), result)

  def test_grid_snap_vector(self):
    result = game.grid_snap_vector((20,20),(127.44, 9.0))
    self.assertEqual((120.0,0), result)

  def test_calc_const_velocity(self):
    result = game.calc_const_velocity(mover=(125,275), target=(100,200), speed=10)
    result = game.round_vector(result,1)
    self.assertEqual((-3.2,-9.5), result)

  def test_new_position(self):
    result = game.new_position(position=(125,275),velocity=(-3.2,-9.5),time=2)
    result = game.round_vector(result,1)
    self.assertEqual((118.6,256.0), result)

  # def test_shoot_one_baddie(self):
  #   ent_init_list = [
  #     game.Baddie((200,250),speed=10),
  #     game.Turret((100,0)),
  #     game.Core((100,150))
  #   ]
  #   facdustry = game.Game(ent_init_list, GUI=0,sound=0)
  #   facdustry.loop(time_limit = 6, step_limit=0, constant_step_time=0)
  #   baddie_list = facdustry.ent_group_dict["baddie"].sprites()
  #   self.assertFalse(baddie_list)

  # def test_shoot_one_baddie_within_time(self):
  #   # tested from speedsheet calcs
  #   baddie_list = [ game.Baddie((100,300),speed=10) ]
  #   turret = game.Turret((0,0))
  #   facdustry = game.Game(baddie_list, turret, GUI=0,sound=0)
  #   facdustry.loop(time_limit = 32, step_limit=0, constant_step_time=1)
  #   baddie_list = facdustry.baddie_group.sprites()
  #   self.assertFalse(baddie_list)

  # test time for baddie to be destroyed

  # def test_new_position(self):
  #   S_g_a = (100,200)  
  #   S_g_b = (125,275)
    
  #   S_l_b_a = game.vector_subtract(S_g_a,S_g_b)
  #   magS_l_b_a = round(game.magnitude(S_l_b_a), 2)
  #   unitS_l_b_a = game.round_vector(game.unit_vector(S_l_b_a), 2)

  #   speed = 10
  #   V_l_b_a = game.vector_scalar_mult(unitS_l_b_a,speed)

  #   # New b position
  #   time_passed = 2
  #   S_l_b_bn = game.vector_scalar_mult(V_l_b_a,time_passed)
  #   S_g_bn = game.vector_add(S_g_b,S_l_b_bn)
  #   result = S_g_bn

  #   self.assertEqual((118.6,256),result)
    
  # def test_new_position2(self):
  #   S_g_b = (100,200)  
  #   S_g_a = (125,275)
    
  #   S_l_b_a = game.vector_subtract(S_g_a,S_g_b)
  #   magS_l_b_a = round(game.magnitude(S_l_b_a), 2)
  #   unitS_l_b_a = game.round_vector(game.unit_vector(S_l_b_a), 2)

  #   speed = 10
  #   V_l_b_a = game.vector_scalar_mult(unitS_l_b_a,speed)

  #   # New b position
  #   time_passed = 2
  #   S_l_b_bn = game.vector_scalar_mult(V_l_b_a,time_passed)
  #   S_g_bn = game.vector_add(S_g_b,S_l_b_bn)
  #   result = S_g_bn

  #   self.assertEqual((106.4,219),result)
    

  # def test_unit_vector(self):
  #   unitV = game.unit_vector((7,20))
  #   result = game.round_sig_vector(unitV,5)
  #   self.assertEqual((0.33035,0.94386),result)


  # def test_baddie_velocity_vector(self):
  #   baddie = game.Baddie(2,(200,300))
  #   turret = game.Turret((100,100),5,300,2)
  #   time = 1

  #   baddie.calculate_velocity(turret,time)
  #   result = baddie.velocity
  #   self.assertEqual((-4.47,-8.94),result)

  # def test_baddie_move(self):

  #   baddie = game.Baddie(2,(200,300))
  #   turret = game.Turret((100,100),5,300,2)
  #   time = 1

  #   baddie.calculate_velocity(turret,time)

  #   baddie.move(time)
  #   result = baddie.rect.center

  #   self.assertEqual((195.53,291.06),result)

  # def test_baddie_vector_before(self):

  #   baddie = game.Baddie(2,(150,90))
  #   turret = game.Turret((200,300),5,300,2)
  #   time = 1

  #   baddie.calculate_velocity(turret,time)
  #   result = baddie.velocity

  #   self.assertEqual((4.1,9.1),result)

  # def test_baddie_move_twice(self):

  #   baddie = game.Baddie(2,(200,300))
  #   turret = game.Turret((100,100),5,300,2)
  #   time = 1

  #   baddie.calculate_velocity(turret,time)
  #   baddie.move(time)

  #   baddie.calculate_velocity(turret,time)
  #   baddie.move(time)

  #   result = baddie.rect.center
  #   self.assertEqual((191.06,282.12),result)
 
if __name__ == '__main__':
  unittest.main()


