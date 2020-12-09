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

continue_game = 1

# set GUI to 1 to display
class Game:
  def __init__(self,baddie_list,turret, GUI=1,sound_on=1):
    # screen
    self.GUI = GUI
    self.sound_on = sound_on
    self.winsize = (400,400)

    self.clock = pygame.time.Clock()
    self.events = pygame.event

    # sprites and groups
    self.baddie_group = pygame.sprite.Group(baddie_list)
    self.turret_group = pygame.sprite.Group(turret)
    self.allsprites_group = pygame.sprite.Group(baddie_list,turret)
    # self.being_shot_group = pygame.sprite.Group()

    # link sprites to game
    for sprite in self.allsprites_group:
      sprite.game = self

    if self.GUI: # includes sounds
      self.screen = pygame.display.set_mode(self.winsize)
    if self.sound_on:
      pass
      # sound
      # self.mixer = pygame.mixer
      # pygame.mixer.init()
      # self.laser_sound = pygame.mixer.Sound("pew.ogg")
      # self.sound_list = [] # load sounds list

    # self.continue_game = 1

  # mouse & keyboard input
  def check_events(self):
    for event in self.events.get():

      # quiting pygame
      if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        global continue_game
        continue_game = 0
        break
      # mouse button baddie creation
      mouse_buttons = pygame.mouse.get_pressed()
      if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()
        new_baddie = Baddie(mouse_pos, speed=30)
        new_baddie.game = self
        new_baddie.add(self.baddie_group,self.allsprites_group)

  def loop(self, time_limit, step_limit, constant_step_time):
    total_time = 0
    step_time = 0
    step = 0
    global continue_game
    while continue_game:

      #update all sprites
      self.baddie_group.update(step_time)
      self.turret_group.update(total_time)

      if self.GUI:
        pygame.display.update()

        self.check_events()

        self.screen.fill(BLACK)
        # pygame.display.set_caption("BLACK")
        self.allsprites_group.draw(self.screen)
        draw_lines(self.screen,self.turret_group)
        # alllines.draw(self.screen)

      if constant_step_time == 0: 
        step_time = self.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        step_time = constant_step_time

      
      step += 1

      total_time += step_time

      if not time_limit == 0 and total_time >= time_limit:
        # global continue_game
        continue_game = 0
      if not step_limit == 0 and step >= step_limit:
        # global continue_game
        continue_game = 0

  pygame.quit()
    

class Turret(pygame.sprite.Sprite):
  # Constructor
  def __init__(self,position):
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)
    self.game = None  

    self.position = position
    self.radius = 100 # shoot range - circle collision detection
    self.ammo = 5
    self.reload_time = 0.05
    self.shoot_timestamp = 0
    self.line = 0 

    # body
    self.image = pygame.Surface((30,30))
    self.image.fill(DEEPSKYBLUE)
    # Fetch the rectangle object that has the dimensions of the image
    # Update the position of this object by setting the values of rect.x and rect.y
    self.rect = self.image.get_rect()
    self.rect.center = position

  def update(self,total_time):

    # Check for targets & fire
    if total_time - self.shoot_timestamp > self.reload_time: # reloading
      hit_list = self._check_for_targets(self.game.baddie_group)
      if hit_list:
        self._shoot(hit_list[0]) # shoot first baddie in list only
        self.shoot_timestamp = total_time
        self.line=Line(RED, self.position, hit_list[0].position) # laser
      else:
        self.line = 0

    # check for baddies touching turret - end game
    touch_list = self._check_for_touching(self.game.baddie_group)
    if touch_list:
      global continue_game
      continue_game = 0

    # for baddie in hit_list:
    #   self._shoot(baddie)

  def _check_for_targets(self,target_group):
    hit_list = []
    hit_list = pygame.sprite.spritecollide(self,target_group, False, pygame.sprite.collide_circle)
    return hit_list

  def _check_for_touching(self,target_group):
    touch_list =[]
    touch_list = pygame.sprite.spritecollide(self,target_group, False, pygame.sprite.collide_rect)
    return touch_list

  def _shoot(self,target):
    if self.ammo > 0:
        print("Shoot: ", target)
        target.kill()

class Baddie(pygame.sprite.Sprite):
  def __init__(self,position,speed=10):
    pygame.sprite.Sprite.__init__(self)
    self.game = None  

    self.position = position
    self.health = 5

    self.image = pygame.Surface((10,10))
    self.image.fill(WHITE)
    self.radius = 5 # circle collision detection
    self.rect = self.image.get_rect()
    self.rect.center = position
    self.speed = speed # pixels per second - decimal important!
    self.velocity = ()
    self.being_shot = 0

  def update(self,time_passed):
    self._move(time_passed) # miliseconds
    self._check_touching_turret()
    # self._move(turret,time_passed)

  def _check_touching_turret(self):
    if pygame.sprite.collide_rect(self,self.game.turret_group.sprites()[0]):
      print("GAME OVER - BADDIE WIN")
      # return 0

  
  def _move(self,time_passed):
    # S - position, V - velocity, l - local, g - global, n - new
    S_g_a = self.game.turret_group.sprites()[0].position
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

def draw_lines(surface,object_group):
  for object in object_group:
    if object.line:
      pygame.draw.line(surface,object.line.colour,object.line.start,object.line.end)

class RenderLines:
  def __init__(self):
    self.lines_list = []

  def store_lines(self,line_list):
    self.lines_list = line_list

  def draw(self, surface):
    for line in self.lines_list:
      pygame.draw.line(surface,line.colour,line.start,line.end)

def main():
  


  baddie_list = [ Baddie((300,300),speed=30.0) ]
  turret = Turret((200,200))

  facdustry = Game(baddie_list, turret, GUI=1, sound_on=1)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
