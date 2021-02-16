import pygame

from constants import *
from general_functions import *
import entity

class UserInterfaceElement():
    def __init__(self,image,colour):
        self.image = image
        self.rect = self.image.get_rect()
        if colour: self.image.fill(colour)
        self.colour = colour
        self.elements = []


    def update(self):
        pass

    def add_elements(self,elements):
        pass

    def draw(self):
        # self.image.fill(self.colour)
        try:
            for item in self.elements:
                self.image.blit(item.image,item.rect)
                item.draw()
        except: pass

class MenuBox(UserInterfaceElement):
    def __init__(self,image,colour):
        UserInterfaceElement.__init__(self,image,colour)
        self.menu_item_size = (30,30)
        self.offset = 5 # 
    
    def add_elements(self,menu_items):
        for count, item in enumerate(menu_items):
            dist = self.menu_item_size[0] + self.offset
            coord_x = dist * (count+1) - 0.5*self.menu_item_size[0]
            # print("Coord: ", (coord_x,self.menu_item_size[1]/2.0))
            # print(item.rect.midright)
            item.position = (coord_x,self.rect.center[1])
            item.size = self.menu_item_size

            self.elements.append(item)


class Menu(UserInterfaceElement):
    def __init__(self,image,colour):
        UserInterfaceElement.__init__(self,image,colour)

    def add_elements(self,menu_box):
        menu_box.rect.bottomleft = self.rect.bottomleft
        self.elements = [menu_box]

class Map(UserInterfaceElement):
    def __init__(self,image,colour):
        UserInterfaceElement.__init__(self,image,colour)
    
    def add_elements(self,entity_group):
        self.elements = entity_group # iterable

class Screen(UserInterfaceElement):
    def __init__(self,image,colour):
        UserInterfaceElement.__init__(self,image,colour)
    
    def add_elements(self,map,menu):
        menu.rect.bottomleft = self.rect.bottomleft
        map.rect.topleft = self.rect.topleft
        self.elements = [map,menu]

# CHANGE - not updated and won't work
class KillCount(pygame.sprite.Sprite):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.gui = gui
        self.font = pygame.font.Font(pygame.font.get_default_font(),20)
        self.image = None
        self.rect = None

    def update(self):
        self.image = self.font.render(str(self.gui.state.kill_count), True, GREEN, BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.gui.menu_rect.bottomright

class GUI:
    def __init__(self,state,winsize=[700, 700]):
        self.state = state
        self.size = winsize
        self.display = pygame.display

        # Instantiate   
        menu_height = 40
        menu_surface = pygame.Surface((self.size[0],menu_height))
        map_surface = pygame.Surface((self.size[0],self.size[1]-menu_height))
        menu_box_surface = pygame.Surface((self.size[0],menu_height))
        self.screen = Screen(self.display.set_mode(self.size),BLACK)
        self.map = Map(map_surface,BLACK)
        self.menu = Menu(menu_surface,BLACK)
        self.menu_box = MenuBox(menu_box_surface,GREY)
        menu_box_items = [entity.Core((0,0)),entity.Turret((0,0)),entity.Wall((0,0)),entity.Spawn((0,0))]

        # Add elements to UI parent 
        self.menu_box.add_elements(menu_box_items)
        self.menu.add_elements(self.menu_box)
        self.map.add_elements(self.state.entity_group.get_group("draw"))
        self.screen.add_elements(self.map,self.menu)

    def draw(self):
        """Draws using the coordinate system of the surface being drawn onto"""

        self.screen.draw() # Recursion through depends

        self.display.update()