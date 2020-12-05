#!/usr/bin/env python

import pygame
import math
import random

WINSIZE = [640, 480]
WHITE = (255, 255, 255)
BLACK = (20, 20, 40)
RED =   (255,   0,   0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
DEEPSKYBLUE = (0,191,255)
YELLOW = (255,255,0)

def round_sig(x, sig=5):
  return round(x, sig - int(math.floor(math.log10(abs(x))))-1)

def round_sig_vector(V,sig=5):
  Vx = round_sig(V[0],sig)
  Vy = round_sig(V[1],sig)
  return (Vx,Vy)

def round_vector(V,digits):
  Vx = round(V[0],digits)
  Vy = round(V[1],digits)
  return (Vx,Vy)

def pol2cart(r, phi):
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return(x, y)

def vector_add(v1,v2):
  v3_x = v1[0]+v2[0]
  v3_y = v1[1]+v2[1]
  return (v3_x,v3_y)

def vector_subtract(v1,v2):
  v3_x = v1[0]-v2[0]
  v3_y = v1[1]-v2[1]
  return (v3_x,v3_y)

def vector_scalar_mult(v,a):
  vx = v[0]*a
  vy = v[1]*a
  return(vx,vy)

def magnitude(v):
  mag = math.sqrt(v[0]**2 + v[1]**2)
  return mag

def unit_vector(v):
  vmag = magnitude(v)
  unit_vx = v[0]/vmag
  unit_vy = v[1]/vmag
  return(unit_vx,unit_vy)

# def update_vector_position(vectorA,vectorB,speed,time)

# set GUI to 1 to display
class Game:
  def __init__(self,baddie_list,turret, GUI=1):
    # screen
    self.GUI = GUI
    self.winsize = (400,400)

    self.clock = pygame.time.Clock()
    self.events = pygame.event

    # sprites and groups
    self.baddie_group = pygame.sprite.Group(baddie_list)
    self.turret_group = pygame.sprite.Group(turret)
    self.allsprites_group = pygame.sprite.RenderPlain(self.baddie_group,self.turret_group)

    if self.GUI:
      self.screen = pygame.display.set_mode(self.winsize)

    self.continue_game = 1

  # mouse & keyboard input
  def check_events(self):
    for event in self.events.get():

      # quiting pygame
      if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        self.continue_game = 0
        break
      # mouse button baddie creation
      mouse_buttons = pygame.mouse.get_pressed()
      if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()
        new_baddie = Baddie(mouse_pos)
        new_baddie.add(self.baddie_group,self.allsprites_group)

  def loop(self, time_limit, step_limit, constant_step_time):
    total_time = 0
    step_time = 0
    step = 0
    while self.continue_game:

      #update all sprites
      self.baddie_group.update(self.turret_group.sprites()[0],step_time)
      self.turret_group.update(self.baddie_group)

      if self.GUI:
        pygame.display.update()

        self.check_events()

        self.screen.fill(BLACK)
        # pygame.display.set_caption("BLACK")
        self.allsprites_group.draw(self.screen)
        # alllines.draw(self.screen)

      if constant_step_time == 0: 
        step_time = self.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        step_time = constant_step_time

      
      step += 1

      total_time += step_time

      if not time_limit == 0 and total_time >= time_limit:
          self.continue_game = 0
      if not step_limit == 0 and step >= step_limit:
        self.continue_game = 0

  pygame.quit()
    

class Turret(pygame.sprite.Sprite):
  # Constructor
  def __init__(self,position):
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)  

    self.position = position
    self.radius = 15 # shoot range - circle collision detection
    self.ammo = 5

    # body
    self.image = pygame.Surface((30,30))
    self.image.fill(DEEPSKYBLUE)
    # Fetch the rectangle object that has the dimensions of the image
    # Update the position of this object by setting the values of rect.x and rect.y
    self.rect = self.image.get_rect()
    self.rect.center = position

  def update(self,baddie_group):
    # self._scan(line_list)
    hit_list = self._check_for_targets(baddie_group)
    for baddie in hit_list:
      self._shoot(baddie)

  def _check_for_targets(self,target_group):
    hit_list = []
    hit_list = pygame.sprite.spritecollide(self,target_group, False, pygame.sprite.collide_circle)
    return hit_list

  def _shoot(self,target):
    if self.ammo > 0:
        print("Shoot: ", target)
        target.kill()

class Baddie(pygame.sprite.Sprite):
  def __init__(self,position,speed=10):
    pygame.sprite.Sprite.__init__(self)  

    self.position = position
    self.health = 5

    self.image = pygame.Surface((10,10))
    self.image.fill(WHITE)
    self.radius = 5 # circle collision detection
    self.rect = self.image.get_rect()
    self.rect.center = position
    self.speed = speed # pixels per second - decimal important!
    self.velocity = ()

  def update(self,turret,time_passed):
    self._move(turret,time_passed) # miliseconds
    # self._move(turret,time_passed)
  
  def _move(self,turret,time_passed):
    # S - position, V - velocity, l - local, g - global, n - new
    S_g_a = turret.position
    S_g_b = self.position
    # speed
    # dist between (mag), direction (unit), 

    S_l_b_a = vector_subtract(S_g_a,S_g_b)
    # distance between turret and this baddie
    magS_l_b_a = magnitude(S_l_b_a)
    # print(magS_l_b_a)

    if not magS_l_b_a < 10:

      # direction of turret from this baddie
      unitS_l_b_a = unit_vector(S_l_b_a)
      
      if not self.velocity:
        # print("direction: ", unitS_l_b_a)
        V_l_b_a = vector_scalar_mult(unitS_l_b_a,self.speed)
        self.velocity = V_l_b_a
      # breakpoint()

      # move baddie to new position towards turret
      V_l_b_a = self.velocity

      S_l_b_bn = vector_scalar_mult(V_l_b_a,time_passed)
      S_g_bn = vector_add(S_g_b,S_l_b_bn)
      #print(S_g_bn)

      self.position= S_g_bn
      self.rect.center = round_vector(S_g_bn,0) # update rect seperately - rounds to integers
      # print(self.rect.center)

class Line:
  def __init__(self,colour, start, end):
    self.colour = colour
    self.start = start
    self.end = end

class RenderLines:
  def __init__(self):
    self.lines_list = []
  def storelines(self,line_list):
    self.lines_list = line_list
  def draw(self, surface):
    for line in self.lines_list:
      pygame.draw.line(surface,line.colour,line.start,line.end)

def main():
  
  baddie_list = [ Baddie((300,300),speed=10.0) ]
  turret = Turret((100,100))

  facdustry = Game(baddie_list, turret, GUI=1)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
