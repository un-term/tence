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

def calc_const_velocity(mover, target, speed):
  """velocity vector between 2 positions with constant speed
    S - position vector, V - velocity vector
    m - mover, t - target
  """
  # position vector between mover & target
  S_mt = vector_subtract(target,mover)
  # distance between mover & target
  magS_mt = magnitude(S_mt)
  # direction from mover to target
  unitS_mt = unit_vector(S_mt)

  return vector_scalar_mult(unitS_mt,speed)

def new_position(position,velocity,time):
  """change in position over time with constant velocity"""
  vector_distance = vector_scalar_mult(velocity,time)
  return vector_add(position,vector_distance)

def magnitude(v):
  mag = math.sqrt(v[0]**2 + v[1]**2)
  return mag

def unit_vector(v):
  vmag = magnitude(v)
  unit_vx = v[0]/vmag
  unit_vy = v[1]/vmag
  return(unit_vx,unit_vy)

def grid_snap_vector(grid,V):
  rx = math.remainder(V[0],grid[0])
  ry = math.remainder(V[1],grid[1])
  return(V[0]-rx, V[1]-ry)

def remove_obj(obj,obj_list):
  """remove object from list of objects"""
  return obj_list.remove(obj)

# set GUI to 1 to display
class Game:
  def __init__(self, ent_init_list, GUI=1,sound=1):
    self.game_over = 0
    # screen
    self.GUI = GUI
    self.sound = sound

    self.winsize = (400,400)
    self.grid = (20,20)

    self.clock = pygame.time.Clock()
    self.events = pygame.event

    if self.GUI: # includes sounds
      self.screen = pygame.display.set_mode(self.winsize)
    if self.sound:
      pygame.mixer.init()
      self.laser_sound = pygame.mixer.Sound("pew.ogg")
      # self.sound_list = [] # load sounds list

    self.ent_group_dict = {
      "all":pygame.sprite.Group(),
      "dead":pygame.sprite.Group()
    }
    self.create_sprite_groups(ent_init_list)
    self.add_sprites_to_groups(ent_init_list)

  def create_sprite_groups(self,entities_list):
    for entity in entities_list:
      self.ent_group_dict.update({entity.type:pygame.sprite.Group()})

  def add_sprites_to_groups(self, entities_list):
    for entity in entities_list:
      self.ent_group_dict[entity.type].add(entity)
      self.ent_group_dict["all"].add(entity)   
      #link game ref to entity
      entity.game = self

  # mouse & keyboard input
  def check_events(self):
    for event in self.events.get():

      # quiting pygame
      if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        self.game_over = 1
        break
      # mouse button baddie creation
      mouse_buttons = pygame.mouse.get_pressed()
      if mouse_buttons[0]:
        mouse_pos = pygame.mouse.get_pos()

        new_baddie_list = [Baddie(mouse_pos, speed=30)]
        
        self.add_sprites_to_groups(new_baddie_list)

  #=================================================================
  def loop(self, time_limit=0, step_limit=0, constant_step_time=0):
    """main game loop"""
    total_time = 0
    step_time = 0
    step = 0
 
    while not self.game_over:

      # update all sprites
      #-------------------
      self.ent_group_dict["all"].update(step_time,total_time)
      # delete dead
      for ent in self.ent_group_dict["dead"]: # CHANGE
        ent.kill()
      # self.ent_group_dict["dead"].empty()

      if self.GUI:
        pygame.display.update()

        self.check_events()

        self.screen.fill(BLACK)
        self.ent_group_dict["all"].draw(self.screen)
        draw_lines(self.screen,self.ent_group_dict["turret"])
        # alllines.draw(self.screen)

      if constant_step_time == 0: 
        step_time = self.clock.tick(60)/1000.0 # miliseconds to seconds
      else:
        step_time = constant_step_time

      step += 1
      total_time += step_time

      if not time_limit == 0 and total_time >= time_limit:
        # global continue_game
        self.game_over = 1
      if not step_limit == 0 and step >= step_limit:
        # global continue_game
        self.game_over = 1

  pygame.quit()
    

class Turret(pygame.sprite.Sprite):
  # Constructor
  def __init__(self,position):
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)
    self.type = "turret"
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

  def update(self,step_time,total_time):

    # Check for targets & fire
    if not self.reloading(total_time):
      hit_list = self._check_for_targets(self.game.ent_group_dict["baddie"])
      if hit_list:
        self._shoot(hit_list[0]) # shoot first baddie in list only
        self.shoot_timestamp = total_time
        self.line=Line(RED, self.position, hit_list[0].position) # laser
      else:
        self.line = 0

  def reloading(self,total_time):
    return (total_time - self.shoot_timestamp <= self.reload_time)

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
        if self.game.sound == 1:
          self.game.laser_sound.play()
        target.reduce_health(1) # CHANGE: assign damage



class Baddie(pygame.sprite.Sprite):
  def __init__(self, initial_pos,speed=10):
    pygame.sprite.Sprite.__init__(self)
    self.type = "baddie"
    self.game = None

    self.health = 3

    self.image = pygame.Surface((10,10))
    self.image.fill(WHITE)
    self.radius = 5 # circle collision detection
    self.rect = self.image.get_rect()
    self.position = initial_pos # set after rect creation CHANGE

    self.speed = speed # pixels per second - decimal important!
    self.velocity = (0,0)

  @property
  def position(self):
    return self._position
  
  @position.setter
  def position(self,value):
    self._position = value
    self.rect.center = value

  def update(self,step_time,total_time):
    """calls internal methods"""
    if self._check_for_collisions("core"):
      print("GAME OVER - BADDIE WIN")
      self.game.game_over = 1
    # elif self._check_for_collisions_within_group("baddie"): # colliding with self
      # self.velocity = self._bounce_velocity()
    elif self._check_for_collisions("turret"):
      self.health = 0
    elif self._check_for_collisions("wall"):
      wall_hit = self._check_for_collisions("wall") # CHANGE: check nearest
      self.velocity = self._bounce_velocity(wall_hit[0],scalar=50)
    else:
      core_position = self._find_nearest_core()
      self.velocity = self._calc_velocity_to_core(core_position)

    self.position = self._new_position_from_velocity(step_time)

    self._check_dead()

  def _check_for_collisions_within_group(self,group):
    if self.game.ent_group_dict[group].has(self):
      tmp_group = self.game.ent_group_dict[group].copy()
      tmp_group.remove(self)
      return pygame.sprite.spritecollide(self,tmp_group,False, pygame.sprite.collide_rect)

  def _check_for_collisions(self,group):
    """list of collided sprites for group"""
    return pygame.sprite.spritecollide(self,self.game.ent_group_dict[group],False, pygame.sprite.collide_rect)

    # hit_list = pygame.sprite.spritecollide(self,self.game.ent_group_dict[group],False, pygame.sprite.collide_rect)
    # return hit_list
  
  def _check_core_collision(self,collided_list):
    """check if objects belong to group core - game over"""
    for entity in collided_list:
      if entity.type is "core":
        print("GAME OVER - BADDIE WIN")
        self.game.game_over = 1

  def _bounce_velocity(self,obj_hit,scalar=1):
    """bounce back in the opposite direction of nearest wall block"""
    dir = calc_const_velocity(self.position, obj_hit.position, speed=1) # speed not needed
    return vector_scalar_mult(dir,scalar*(-1.0))

  def _find_nearest_core(self):
    """CHANGE - currently returns one core only"""
    return self.game.ent_group_dict["core"].sprites()[0].position

  def _calc_velocity_to_core(self,core_position):
    return calc_const_velocity(self.position, core_position, self.speed)

  def _new_position_from_velocity(self,step_time):
    return new_position(self.position,self.velocity,step_time)

  def reduce_health(self,damage):
    self.health -= damage
  
  def _check_dead(self):
    if self.health <= 0:
      self.game.ent_group_dict["dead"].add(self)
  

class Core(pygame.sprite.Sprite):
  # Constructor
  def __init__(self,position):
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)
    self.type = "core"
    self.game = None  
 
    self.position = position
    self.radius = 25 # shoot range - circle collision detection

    self.image = pygame.Surface((50,50))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.center = position

class Wall(pygame.sprite.Sprite):
  def __init__(self,position):
    pygame.sprite.Sprite.__init__(self)
    self.type = "wall"
    self.game = None 

    self.position = position
    self.radius = 25 # shoot range - circle collision detection

    self.image = pygame.Surface((10,10))
    self.image.fill(YELLOW)
    self.rect = self.image.get_rect()
    self.rect.center = position

class Line:
  def __init__(self,colour, start, end):
    self.colour = colour
    self.start = start
    self.end = end

def draw_lines(surface,object_group):
  for object in object_group:
    if object.line:
      pygame.draw.aaline(surface,object.line.colour,object.line.start,object.line.end)

class RenderLines:
  def __init__(self):
    self.lines_list = []

  def store_lines(self,line_list):
    self.lines_list = line_list

  def draw(self, surface):
    for line in self.lines_list:
      pygame.draw.line(surface,line.colour,line.start,line.end)

def main():

  ent_init_list = [
    Baddie((200,400),speed=30.0),
    Turret((300,150)),
    Turret((100,150)),
    Core((200,50)),
    Wall((160,280)),
    Wall((170,280)),
    Wall((180,280))
  ]

  facdustry = Game(ent_init_list, GUI=1, sound=0)
  facdustry.loop(time_limit = 0, step_limit=0, constant_step_time=0)

# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
