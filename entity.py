import pygame
import math
import random

from general_functions import *
from constants import *
import graphical_surface

def check_for_type(ent_list, ent_type):
    exists = False
    for ent in ent_list:
        if ent.type == ent_type:
            exists = True
    return exists

def remove_type_from_list(ent_list, ent_type):
    for ent in ent_list:
        if ent.type == ent_type:
            ent_list.remove(ent)
    return ent_list

def get_rect_edge_axis(rect,midpoint):
    """CHANGE: brittle if rect is rotated"""
    if rect.midtop == midpoint:
        return "x"
    elif rect.midbottom == midpoint:
        return "x"
    if rect.midleft == midpoint:
        return "y"
    elif rect.midright == midpoint:
        return "y"
    else:
        raise Exception("Point not found on rect")
    
def find_closest_entity(ref_entity,entity_list):
    closest_entity = entity_list[0]
    for entity in entity_list[1:]:
        if magnitude(vector_subtract(ref_entity.position,entity.position)) < magnitude(vector_subtract(ref_entity.position,closest_entity.position)):
            closest_entity = entity
        else:
            pass
    return closest_entity

def entity_factory(entity_name, *args, **kwargs):
    entities = {
        "turret" : Turret,
        "baddie" : Baddie,
        "wall" : Wall,
        "core" : Core,
        "spawn" : Spawn
    }
    return entities[entity_name](*args, **kwargs)


class Entity(graphical_surface.GraphicalSurface):
    def __init__(self,parent=None):
        graphical_surface.GraphicalSurface.__init__(self,parent)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self,value):
        self._position = value
        self.rect.center = value


class LineSprite(Entity):
    def __init__(self,colour, start, end):
        # def __init__(self):
        Entity.__init__(self)
        size = vector_abs(vector_subtract(start,end))
        colour = BLACK
        self.create_surface_and_rect(size, colour)
        self.surface.set_colorkey(BLACK)

        center = vector_vector_midpoint(end,start)
        # self.rect.center = center
        self.position = center
        # pygame.draw.aaline(self.surface,self.colour,start,end)
        local_start = coord_sys_map_translation(self.rect.topleft, start)
        local_end = coord_sys_map_translation(self.rect.topleft, end)
        pygame.draw.line(self.surface,RED,local_start,local_end,3)
        # line drawn on surface local coordinate system

    def update(self):
        pass

    def collision(self,ent):
        pass


class Turret(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        size = (30,30)
        colour = DEEPSKYBLUE
        self.create_surface_and_rect(size, colour)
        self.position = position
    
        self.radius = 100 # shoot range - circle collision detection
        self.ammo = 5
        self.damage = 1
        self.health = 10
        self.reload_time = 0.2
        self.shoot_timestamp = 0

    def update(self):
        # Check for targets & fire
        if not self._reloading(self.entity_group.state.total_time):
            target_group = self.entity_group.get_group("baddie")
            hit_list = self._check_for_targets(target_group)
            if hit_list:
                self._shoot(hit_list[0],self.entity_group.state.total_time) # shoot first baddie in list only
                laser = LineSprite(RED, self.position, hit_list[0].position)
                self.entity_group.add_ent([laser],["draw","remove"])
            self._check_dead()

    def collision(self,ent):
        if ent.type == "baddie":
            self.take_damage(ent.damage)
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

    def _check_dead(self):
        if self.health <= 0:
            self.entity_group.add_ent([self],["remove"])

    def take_damage(self, damage):
        self.health -= damage


class Baddie(Entity):
    def __init__(self, position,speed=30.0):
        Entity.__init__(self)
        size = (10,10)
        colour = RED
        self.create_surface_and_rect(size, colour)
        self.position = position

        self.health = 2
        self.radius = 5 # circle collision detection

        self.speed = speed # pixels per second - decimal important!
        self.velocity = (0,0)
        self.bounce_timestamp = 0

        self.damage = 1

    def update(self):
        """calls internal methods"""

        self.entity_group.get_group("collision").empty()
        self.entity_group.add_ent(self._check_for_collision(["all"]),["collision"])

        core_list = self.entity_group.find_overlap("core","collision")
        turret_list = self.entity_group.find_overlap("turret","collision")
        wall_list = self.entity_group.find_overlap("wall","collision")
        if core_list:
            core_list[0].collision(self)
        elif turret_list:
            turret_list[0].collision(self)
        elif self.check_bounce(self.entity_group.state.total_time, bounce_limit=0.15):
            pass # keep bounce velocity
        elif wall_list:
            wall = find_closest_entity(self,wall_list) # bounce off closest
            wall.collision(self)
        else:
            core_position = self._find_nearest_core()
            self.velocity = self._calc_velocity_to_core(core_position)

        self.position = self._new_position_from_velocity(self.entity_group.state.step_time)

        self._check_dead()

    def _check_for_collision(self,group_list):
        """list of collided sprites for group"""
        cld_list = []
        for group in group_list:
            cld_list += pygame.sprite.spritecollide(self,self.entity_group.get_group(group),False, pygame.sprite.collide_rect)
        return cld_list

    def collision(self, entity):
        """continues moving baddie when colliding with other baddie"""
        pass

    def _find_nearest_core(self):
        """CHANGE - currently returns one core only"""
        if self.entity_group.get_group("core") is not None:
            return self.entity_group.get_group("core").sprites()[0].position
        else:
            return (0.0,0.0) # No core, head to origin instead       

    def _calc_velocity_to_core(self,core_position):
        return calc_const_velocity(self.position, core_position, self.speed)

    def _new_position_from_velocity(self,step_time):
        return new_position(self.position,self.velocity,step_time)

    def take_damage(self,damage):
        self.health -= damage
    
    def do_damage(self,target,damage):
        target.health -= damage
    
    def _check_dead(self):
        if self.health <= 0:
            self.entity_group.add_ent([self],["remove"])
            self.entity_group.state.kill_count += 1
    
    def check_bounce(self,total_time, bounce_limit=0.5):
      return (total_time - self.bounce_timestamp <= bounce_limit)
  

class Core(Entity):
    # Constructor
    def __init__(self,position):
        Entity.__init__(self)
        size = (50,50)
        colour = GREEN
        self.create_surface_and_rect(size, colour)
        self.position = position

        self.radius = 25 # shoot range - circle collision detection
        self.health = 40.0

    def update(self):
        self._check_dead()
        self._check_health()

    def collision(self, ent):
        if ent.type == "baddie":
            self.take_damage(ent.damage)
           # ent.health(self,ent.damage)
            ent.health = 0

    def take_damage(self, damage):
        self.health -= damage

    def _check_dead(self):
        """CHANGE - adding entities to game_over group to avoid having to know game object"""
        if self.health < 0:
            self.entity_group.state.end_game()
            print("game over")

    def _check_health(self):
        if self.health < 10:
            self.change_colour(RED)
        elif self.health < 20:
            self.change_colour(YELLOW)


class Wall(Entity):
    def __init__(self,position):
        Entity.__init__(self)
        size = (10,10)
        colour = YELLOW
        self.create_surface_and_rect(size, colour)
        self.position = position
        

    def update(self):
        pass

    def collision(self,ent):
        if ent.type == "baddie":
            ent.velocity = self._bounce_velocity(ent)
            ent.bounce_timestamp = self.entity_group.state.total_time
        else:
            pass
    
    def get_edge_midpoints(self):
        return [self.rect.midtop,self.rect.midright,self.rect.midbottom,self.rect.midleft]

    def _bounce_velocity(self,ent):
        """bounce back in the opposite direction of nearest wall block"""
        closest_midpoint = find_closest_vector(ent.position,self.get_edge_midpoints())
        axis = get_rect_edge_axis(self.rect,closest_midpoint)

        if axis == "x":
            return (ent.velocity[0],ent.velocity[1]*(-1.0))
        elif axis == "y":
            return (ent.velocity[0]*(-1.0),ent.velocity[1])
        else:
            raise Exception("Incorrect bounce axis")


class Spawn(Entity):
    """Produces Baddie entities on Spawn position"""
    def __init__(self,position):
        Entity.__init__(self)
        size = (20,20)
        colour = ORANGE
        self.create_surface_and_rect(size, colour)
        self.position = position

        self.baddie_count = 0
        self.spawn_timestamp = 0
        self.spawn_wait = 1

    def update(self):
        self.spawn_baddie()

    def spawn_baddie(self):
        if not self._check_spawn_wait():
            self.entity_group.add_ent([Baddie(self.position)])
            self.spawn_timestamp = self.entity_group.state.total_time

    def _check_spawn_wait(self):
        return self.entity_group.state.total_time - self.spawn_timestamp <= self.spawn_wait
