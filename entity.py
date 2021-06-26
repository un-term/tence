import pygame
import math
import random

from general_functions import *
from constants import *
import graphical_surface


def get_rect_edge_axis(rect, midpoint):
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

# unused
def find_closest_entity(ref_entity, entity_list):
    closest_entity = entity_list[0]
    for entity in entity_list[1:]:
        if magnitude(vector_subtract(ref_entity.position,entity.position)) < magnitude(vector_subtract(ref_entity.position,closest_entity.position)):
            closest_entity = entity
        else:
            pass
    return closest_entity


class GroupCollisionDetection:
    def __init__(self, state):
        self.state = state
        self.entity_list = [
        factory("baddie",(0,0)),
        factory("turret",(0,0))
        ]

    def collision_detection(self):
        for entity in self.entity_list:
            entity_group = self.state.entity_group.get_group(entity.type)
            for target in entity.targets:
                target_group = self.state.entity_group.get_group(target)
                if entity_group and target_group:
                    dict_collisions = self.state.entity_group.group_collision_detection(entity_group, target_group, entity.collision_function())
                    self.process_collisions(dict_collisions)

    def process_collisions(self, dict_collisions):
        for entity in dict_collisions:
            if dict_collisions[entity]:
                # first collision only
                target = dict_collisions[entity][0] 
                entity.collision_detection(target)

                       
def factory(entity_name, *args, **kwargs):
    entities = {
        "turret" : Turret,
        "baddie" : Baddie,
        "wall" : Wall,
        "core" : Core,
        "spawn" : Spawn
    }
    return entities[entity_name](*args, **kwargs)


class SurfaceStore():
    def __init__(self):
        self.dict = {}

    def add_surface(self, type, size, colour):
        if not self.dict.get(type):
            surface = pygame.Surface(size)
            surface.fill(colour)
            self.dict[type] = surface
            # self.dict.update({type, surface})

    def get_surface(self, type):
        return self.dict[type]


class Entity(graphical_surface.GraphicalSurface):
    def __init__(self, parent=None, surface_store=SurfaceStore()):
        graphical_surface.GraphicalSurface.__init__(self,parent)
        self.surface_store = surface_store
        self.entity_group = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self,value):
        self._position = value
        self.rect.center = value

    @property
    def surface(self):
        return self.surface_store.get_surface(self.type)

    # @surface.setter
    # def surface(self, colour, size):
    #     self._position = value
    #     self.rect.center = value

class Laser(graphical_surface.GraphicalSurface):
    def __init__(self, entity_group, laser_colour, start, end):
        graphical_surface.GraphicalSurface.__init__(self, parent=None)
        '''Laser linked directly to entity_group'''
        self.entity_group = entity_group
        size = vector_abs(vector_subtract(start,end))
        bg_colour = BLACK
        # self.surface_store.add_surface(self.type, size, bg_colour)
        self.surface = pygame.Surface(size)
        self.surface.fill(bg_colour)
        self.rect = pygame.Rect((0,0), size)  # rect position not required since self.position used
        self.created_timestamp = self.entity_group.state.total_time
        self.alive_duration = 0.10 # seconds
        self.surface.set_colorkey(bg_colour) #  background colour, like transparency

        center = vector_vector_midpoint(end,start)
        self.rect.center = center
        self.position = center  # Required by camera
        local_start = coord_sys_map_translation(self.rect.topleft, start)
        local_end = coord_sys_map_translation(self.rect.topleft, end)
        pygame.draw.line(self.surface,laser_colour,local_start,local_end,3)
        # pygame.draw.aaline(self.surface,laser_colour,local_start,local_end,3)

    def update(self):
        pass

    def collision(self,ent):
        pass


class Turret(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        size = (30,30)
        colour = DEEPSKYBLUE
        self.surface_store.add_surface(self.type, size, colour)
        self.rect = pygame.Rect((0,0), size)
        # self.create_surface_and_rect(size, colour)
        self.position = position
    
        self.radius = 100 # shoot range - circle collision detection
        self.ammo = 5
        self.damage = 1
        self.health = 10
        self.reload_time = 0.2
        self.shoot_timestamp = 0
        self.targets = ["baddie"]

    def update(self):
        self._check_dead()

    def collision_detection(self, target):
        ''' Collision detection always happens even if reloading ''' 
        if not self._reloading(self.entity_group.state.total_time):
            self._shoot(target ,self.entity_group.state.total_time) # shoot first baddie in list only
            laser = Laser(self.entity_group, RED, self.position, target.position)
            self.entity_group.add_ent([laser],["special_effects"])

    def collision(self,ent):
        if ent.type == "baddie":
            self.take_damage(ent.damage)
            ent.take_damage(ent.health)

    def collision_function(self):
        return pygame.sprite.collide_circle

    def _reloading(self,total_time):
        return (total_time - self.shoot_timestamp <= self.reload_time)

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
        self.surface_store.add_surface(self.type, size, colour)
        self.rect = pygame.Rect((0,0), size)
        self.position = position

        self.health = 2
        self.radius = 5 # circle collision detection

        self.speed = speed # pixels per second - decimal important!
        self.velocity = (0,0)
        self.bounce_timestamp = 0
        self.bouncing_time = 0.25

        self.damage = 1
        self.targets = ["core", "turret", "wall"]

    def update(self):
        if self.check_not_bounce():
            core_position = self._find_nearest_core()
            self.velocity = self._calc_velocity_to_core(core_position)
        self.position = self._new_position_from_velocity(self.entity_group.state.tick_time)
        self._check_dead()

    def collision_detection(self, target):
        target.collision(self)
        # wall collision is with the first in the list, not the necessarily the closest
        # wall = find_closest_entity(self,target) # bounce off closest

    def collision(self, entity):
        """continues moving baddie when colliding with other baddie"""
        pass

    def collision_function(self):
        return pygame.sprite.collide_rect

    def _find_nearest_core(self):
        """CHANGE - currently returns one core only"""
        if self.entity_group.get_group("core") is not None:
            return self.entity_group.get_group("core").sprites()[0].position
        else:
            return (0.0,0.0) # No core, head to origin instead       

    def _calc_velocity_to_core(self,core_position):
        return calc_const_velocity(self.position, core_position, self.speed)

    def _new_position_from_velocity(self,tick_time):
        return new_position(self.position,self.velocity,tick_time)

    def take_damage(self,damage):
        self.health -= damage
    
    def do_damage(self,target,damage):
        target.health -= damage
    
    def _check_dead(self):
        if self.health <= 0:
            self.entity_group.add_ent([self],["remove"])
            self.entity_group.state.kill_count += 1
    
    def check_not_bounce(self):
        time_passed = self.entity_group.state.total_time - self.bounce_timestamp
        if time_passed > self.bouncing_time:
            return True
        else:
            return False
  

class Core(Entity):
    def __init__(self,position):
        Entity.__init__(self)
        size = (50,50)
        colour = GREEN
        self.surface_store.add_surface(self.type, size, colour)
        self.rect = pygame.Rect((0,0), size)
        self.position = position

        self.radius = 25 # shoot range - circle collision detection
        self.health = 40.0

    def update(self):
        self._check_dead()
        self._check_health()

    def collision(self, ent):
        if ent.type == "baddie":
            self.take_damage(ent.damage)
            ent.health = 0

    def take_damage(self, damage):
        self.health -= damage

    def _check_dead(self):
        if self.health <= 0:
            # Game over
            self.entity_group.state.end_game()

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
        self.surface_store.add_surface(self.type, size, colour)
        self.rect = pygame.Rect((0,0), size)
        self.position = position
        self.health = 6
        
    def update(self):
        self._check_dead()

    def collision(self,ent):
        if ent.type == "baddie":
            ent.velocity = self._bounce_velocity(ent)
            ent.bounce_timestamp = self.entity_group.state.total_time
            self.take_damage(ent.damage)
            ent.take_damage(ent.health)
        else:
            pass
    
    def take_damage(self, damage):
        self.health -= damage

    def _check_dead(self):
        if self.health <= 0:
            self.entity_group.add_ent([self],["remove"])

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
        self.surface_store.add_surface(self.type, size, colour)
        self.rect = pygame.Rect((0,0), size)
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
