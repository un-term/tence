import pygame
import math
import random

from general_functions import *
from constants import *

class LineSprite(pygame.sprite.Sprite):
  def __init__(self,colour, start, end):
  # def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.type = "laser"
    self.game = None 
    self.colour = RED

    size = vector_abs(vector_subtract(start,end))
    center = vector_vector_midpoint(end,start)

    self.image = pygame.Surface(size)
    self.image.fill(BLACK)
    self.image.set_colorkey(BLACK)
    
    self.rect = self.image.get_rect()
    self.rect.center = center
    # pygame.draw.aaline(self.image,self.colour,start,end)
    local_start = coord_sys_map_translation(self.rect.topleft, start)
    local_end = coord_sys_map_translation(self.rect.topleft, end)
    pygame.draw.line(self.image,self.colour,local_start,local_end,2)
    # line drawn on surface local coordinate system

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
    self.reload_time = 0.2
    self.shoot_timestamp = 0

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
      hit_list = self._check_for_targets(self.game.entity_group.get_group("baddie"))
      if hit_list:
        self._shoot(hit_list[0]) # shoot first baddie in list only
        self.shoot_timestamp = total_time
        # self.line=Line(RED, self.position, hit_list[0].position) # laser
        laser = LineSprite(RED, self.position, hit_list[0].position)
        # line[0].draw(self.game.screen)
        self.game.entity_group.add_ent([laser],["draw","remove"])

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
        # print("Shoot: ", target)
        if self.game.sound == 1:
          self.game.sound.laser_sound.play()
        target.reduce_health(1) # CHANGE: assign damage

class Baddie(pygame.sprite.Sprite):
  def __init__(self, initial_pos,speed=10):
    pygame.sprite.Sprite.__init__(self)
    self.type = "baddie"
    self.game = None

    self.health = 2

    self.image = pygame.Surface((10,10))
    self.image.fill(RED)
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

  # def _check_for_collisions_within_group(self,group):
  #   if self.game.ent_group_dict[group].has(self):
  #     tmp_group = self.game.ent_group_dict[group].copy()
  #     tmp_group.remove(self)
  #     return pygame.sprite.spritecollide(self,tmp_group,False, pygame.sprite.collide_rect)

  def _check_for_collisions(self,group):
    """list of collided sprites for group"""
    return pygame.sprite.spritecollide(self,self.game.entity_group.get_group(group),False, pygame.sprite.collide_rect)

    # hit_list = pygame.sprite.spritecollide(self,self.game.ent_group_dict[group],False, pygame.sprite.collide_rect)
    # return hit_list
  
  def _check_core_collision(self,collided_list):
    """check if objects belong to group core - game over"""
    for entity in collided_list:
      if entity.type == "core":
        print("GAME OVER - BADDIE WIN")
        self.game.game_over = 1

  def _bounce_velocity(self,obj_hit,scalar=1):
    """bounce back in the opposite direction of nearest wall block"""
    dir = calc_const_velocity(self.position, obj_hit.position, speed=1) # speed not needed
    return vector_scalar_mult(dir,scalar*(-1.0))

  def _find_nearest_core(self):
    """CHANGE - currently returns one core only"""
    return self.game.entity_group.get_group("core").sprites()[0].position

  def _calc_velocity_to_core(self,core_position):
    return calc_const_velocity(self.position, core_position, self.speed)

  def _new_position_from_velocity(self,step_time):
    return new_position(self.position,self.velocity,step_time)

  def reduce_health(self,damage):
    self.health -= damage
  
  def _check_dead(self):
    if self.health <= 0:
      # self.game.entity_group["remove"].add(self)
      self.game.entity_group.add_ent([self],["remove"])
  

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