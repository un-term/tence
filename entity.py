import pygame
import math
import random

from general_functions import *
from constants import *

class LineSprite(pygame.sprite.Sprite):
    def __init__(self,colour, start, end):
        # def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.entity_group = None
        self.type = "laser"
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
        pygame.draw.line(self.image,self.colour,local_start,local_end,3)
        # line drawn on surface local coordinate system

    def update(self):
        pass

    def collision(self,ent):
        pass

class Turret(pygame.sprite.Sprite):
    # Constructor
    def __init__(self,position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.entity_group = None
        self.type = "turret"
    
        self.position = position
        self.size = (30,30)
        self.radius = 100 # shoot range - circle collision detection
        self.ammo = 5
        self.damage = 1
        self.reload_time = 0.2
        self.shoot_timestamp = 0

        # body
        self.image = pygame.Surface(self.size)
        self.image.fill(DEEPSKYBLUE)
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        # Check for targets & fire
        if not self._reloading(self.entity_group.state.total_time):
            target_group = self.entity_group.get_group("baddie")
            hit_list = self._check_for_targets(target_group)
            if hit_list:
                self._shoot(hit_list[0],self.entity_group.state.total_time) # shoot first baddie in list only
                # self.line=Line(RED, self.position, hit_list[0].position) # laser
                laser = LineSprite(RED, self.position, hit_list[0].position)
                # line[0].draw(self.game.screen)
                self.entity_group.add_ent([laser],["draw","remove"])

    def collision(self,ent):
        if ent.type == "baddie":
            ent.take_damage(ent.health)

    def _reloading(self,total_time):
        return (total_time - self.shoot_timestamp <= self.reload_time)

    def _check_for_targets(self,target_group):
        hit_list = []
        if target_group:
            hit_list = pygame.sprite.spritecollide(self,target_group, False, pygame.sprite.collide_circle)
            return hit_list
        else:
            return hit_list

    def _check_for_touching(self,target_group):
        touch_list =[]
        if target_group:
            touch_list = pygame.sprite.spritecollide(self,target_group, False, pygame.sprite.collide_rect)
            return touch_list
        else:
            return touch_list

    def _shoot(self,target,total_time):
        """CHANGE: ammo"""
        if self.ammo > 0:
            target.take_damage(self.damage)
            self.shoot_timestamp = total_time

        # print("shooting!!!")
        # self.entity_group.add_ent([self],["sound"])
        # self.game.sound.laser_sound.play()

class Baddie(pygame.sprite.Sprite):
    def __init__(self, initial_pos,speed=10.0):
        pygame.sprite.Sprite.__init__(self)
        self.entity_group = None
        self.type = "baddie"

        self.health = 2
        self.size = (10,10)
        self.image = pygame.Surface(self.size)
        self.image.fill(RED)
        self.radius = 5 # circle collision detection
        self.rect = self.image.get_rect()
        self.position = initial_pos # set after rect creation CHANGE

        self.speed = speed # pixels per second - decimal important!
        self.velocity = (0,0)

        self.damage = 1

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,value):
        self._position = value
        self.rect.center = value

    def update(self):
        """calls internal methods"""
        colsn_list = self._check_for_collision(["all"]) # all may need changing
        colsn_list.remove(self)
        # bouncing = 0
        if colsn_list:
            for ent in colsn_list:
                ent.collision(self)
        else: # does not collide
            core_position = self._find_nearest_core()
            self.velocity = self._calc_velocity_to_core(core_position)

        self.position = self._new_position_from_velocity(self.entity_group.state.step_time)

        self._check_dead()

  # def _check_for_collisions_within_group(self,group):
  #   if self.game.ent_group_dict[group].has(self):
  #     tmp_group = self.game.ent_group_dict[group].copy()
  #     tmp_group.remove(self)
  #     return pygame.sprite.spritecollide(self,tmp_group,False, pygame.sprite.collide_rect)

    def _check_for_collision(self,group_list):
        """list of collided sprites for group"""
        cld_list = []
        for group in group_list:
            cld_list += pygame.sprite.spritecollide(self,self.entity_group.get_group(group),False, pygame.sprite.collide_rect)
        return cld_list

    def collision(self, entity):
        """continues moving baddie when colliding with other baddie"""
        core_position = self._find_nearest_core()
        self.velocity = self._calc_velocity_to_core(core_position)

    def _find_nearest_core(self):
        """CHANGE - currently returns one core only"""
        if self.entity_group.get_group("core") is not None:
            return self.entity_group.get_group("core").sprites()[0].position
        else:
            return (0.0,0.0)       

    def _calc_velocity_to_core(self,core_position):
        return calc_const_velocity(self.position, core_position, self.speed)

    def _new_position_from_velocity(self,step_time):
        return new_position(self.position,self.velocity,step_time)

    def take_damage(self,damage):
        self.health -= damage
    
    def _do_damage(self,target,damage):
        target.health -= damage
    
    def _check_dead(self):
        if self.health <= 0:
            # self.game.entity_group["remove"].add(self)
            self.entity_group.add_ent([self],["remove"])
  

class Core(pygame.sprite.Sprite):
    # Constructor
    def __init__(self,position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.entity_group = None
        self.type = "core"
    
        self.position = position
        self.size = (50,50)
        self.radius = 25 # shoot range - circle collision detection

        self.image = pygame.Surface(self.size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.health = 40.0

    def update(self):
        self._check_dead()
        self._check_health()

    def collision(self, ent):
        if ent.type == "baddie":
            ent._do_damage(self,ent.damage)
            ent.health = 0
        else:
            pass

    def _check_dead(self):
        """CHANGE - adding entities to game_over group to avoid having to know game object"""
        if self.health < 0:
            self.entity_group.state.end_game()
            print("game over")

    def _check_health(self):
        if self.health < 10:
            self.image.fill(RED)
        elif self.health < 20:
            self.image.fill(YELLOW)

class Wall(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.entity_group = None
        self.type = "wall"

        self.position = position
        self.size = (10,10)

        self.image = pygame.Surface(self.size)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        pass

    def collision(self,ent):
        if ent.type == "baddie":
            ent.velocity = self._bounce_velocity(ent,scalar=50)
        else:
            pass

    def _bounce_velocity(self,ent,scalar=1):
        """bounce back in the opposite direction of nearest wall block"""
        dir = calc_const_velocity(ent.position, self.position, speed=1) # speed not needed
        return vector_scalar_mult(dir,scalar*(-1.0))

      