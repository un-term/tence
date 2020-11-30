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

  def test_pol2cart(self):
    result = game.pol2cart(1,3*(math.pi*0.5))
    result = game.round_vector((result), 6)
    self.assertEqual((0,-1), result)

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

  def test_move_repeated(self)
    turret = Turret((100,200),5,300,2)
    baddie = Baddie(2,(125,275))

    it = 0
    done = 0
    while not done:
      it += 1
      baddie.move(turret,1)
      if i == 5:
        done = 1
        
  result = baddie.rect.center

  self.assertEqual((,result)

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


