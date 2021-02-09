import pygame

from constants import *
from general_functions import *
import entity

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
        # self.rect.topleft = self.gui.screen.topleft

class MenuBox(pygame.sprite.Sprite):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.gui = gui
        self.size = self.gui.menu_rect.size
        self.image = pygame.Surface(self.size)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.left_menu_list = []

    def update(self):
        pass

    def add_left_menu_item(self,menu_item):
        menu_item.size = (30,30)
        offset = (5,0)
        if not self.left_menu_list: 
            menu_item.rect.midleft = vector_add(self.rect.midleft,offset)
        else: 
            menu_item.rect.midleft = vector_add(self.left_menu_list[-1].rect.midright,offset)
        self.left_menu_list.append(menu_item)

    def check_vertical_height(self,height1,height2): #CHANGE: include horizontal limit also
        if height1 <= height2:
            return True
        else:
            return False
    
    def select_entity(self,mouse_pos):
        mouse_pos = coord_sys_map_translation(self.gui.menu_rect.topleft,mouse_pos)
        entity = None
        for menu_entity in self.left_menu_list:
            if menu_entity.rect.collidepoint(mouse_pos):
                print(self.create_entity(menu_entity))
                entity = self.create_entity(menu_entity)

        if entity: return entity
        else : return None

    def create_entity(self,menu_entity):
        try: return menu_entity.__class__((0,0))
        except: raise Exception("Cannot instantiate class from menu selection")

class GUI:
    def __init__(self,state,winsize=[700, 700]):
        self.state = state
        self.size = winsize
        self.display = pygame.display
        self.screen = self.display.set_mode(self.size)
        self.screen_rect = self.screen.get_rect() 

        # self.ui_elements = ui_elements

        menu_height = 40
        self.menu = pygame.Surface((self.size[0],menu_height))
        self.menu_rect = self.menu.get_rect()
        self.menu_rect.bottomleft = self.screen_rect.bottomleft

        self.map = pygame.Surface((self.size[0],self.size[1]-menu_height))
        self.map_rect = self.map.get_rect()
        self.map_rect.bottomleft = self.menu_rect.topleft

        self.menu_box = MenuBox(self)
        self.menu_box.add_left_menu_item(entity.Core((0,0)))
        self.menu_box.add_left_menu_item(entity.Turret((0,0)))
        self.menu_box.add_left_menu_item(entity.Wall((0,0)))
        self.menu_box.add_left_menu_item(entity.Spawn((0,0)))

    def draw(self):
        """The coordinate system of the surface being drawn onto,
        is what is used"""
        self.map.fill(BLACK)
        self.state.entity_group.get_group("draw").draw(self.map)
        self.screen.blit(self.map,self.map_rect)

        # for element in self.element_group:
        #     self.menu.blit(element.image,element.rect)
            # self.element_group.draw(self.menu)
        # print(self.menu_rect.topleft)
        self.menu.fill(BLACK)
        for item in self.menu_box.left_menu_list:
            self.menu_box.image.blit(item.image,item.rect)

        self.menu.blit(self.menu_box.image,self.menu_box.rect)
        self.screen.blit(self.menu,self.menu_rect)

        self.display.update()
  
        #gui objects depend on others for position. Cannot stick into anoymous group