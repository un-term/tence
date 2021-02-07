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
        self.rect.bottomright = self.menu_rect.bottomright
        # self.rect.topleft = self.gui.screen.topleft

class MenuBox(pygame.sprite.Sprite):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.gui = gui
        self.size = (self.gui.size[0],40)
        self.image = pygame.Surface(self.size)
        self.image.fill(GREY)
        self.rect = self.gui.self.menu_rect
        self.rect.bottomleft = self.gui.menu_rect.bottomleft

    def update(self):
        pass

class MenuCore(entity.Core):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        super().__init__((0,0))
        self.gui = gui
        self.size = (30,30)
        self.image = pygame.Surface(self.size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = vector_add(self.gui.rect.bottomleft,(5,-5))

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
        self.menu_rect.bottomleft == self.screen_rect.bottomleft

        self.map = pygame.Surface((self.size[0],self.size[1]-menu_height))
        self.map_rect = self.map.get_rect()
        self.map_rect.bottomleft == self.menu_rect.topleft

        self.element_group = pygame.sprite.OrderedUpdates()

        self.element_group.add(MenuBox(self))
        self.element_group.add(KillCount(self))
        self.element_group.add(MenuCore(self))