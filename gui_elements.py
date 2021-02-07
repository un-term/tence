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
        if self.check_vertical_height(menu_item.size[1],self.size[1]):
            offset = (5,0)
            if not self.left_menu_list:
                menu_item.rect.midleft = vector_add(self.rect.midleft,offset)
                self.left_menu_list.append(menu_item)
            else:
                menu_item.rect.midleft = vector_add(self.left_menu_list[-1],offset)
                self.left_menu_list.append(menu_item)

    def check_vertical_height(self,height1,height2): #CHANGE: include horizontal limit also
        if height1 <= height2:
            return True
        else:
            return False

class MenuCore(entity.Core):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__((0,0))
        # self.gui = gui
        self.size = (30,30)
        self.image = pygame.Surface(self.size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # self.rect.bottomleft = vector_add(self.gui.menu_rect.bottomleft,(5,-5))

    def update(self):
        pass
        # self.rect.topleft = self.gui.screen.topleft

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

        # self.element_group = pygame.sprite.OrderedUpdates()# CHANGE: name to menu

        # self.element_group.add(MenuBox(self))
        self.menu_box = MenuBox(self)
        self.menu_box.add_left_menu_item(MenuCore())
        # self.element_group.add(KillCount(self))
        # self.element_group.add(MenuCore(self))

    def draw(self):
        self.display.update()
        self.screen.fill(BLACK)
        self.state.entity_group.get_group("draw").draw(self.map)
        self.screen.blit(self.map,self.map_rect)

        # for element in self.element_group:
        #     self.menu.blit(element.image,element.rect)
            # self.element_group.draw(self.menu)
        # print(self.menu_rect.topleft)
        for item in self.menu_box.left_menu_list:
            self.menu_box.image.blit(item.image,item.rect)

        self.menu.blit(self.menu_box.image,self.menu_box.rect)
        self.screen.blit(self.menu,self.menu_rect)
        
        #gui objects depend on others for position. Cannot stick into anoymous group