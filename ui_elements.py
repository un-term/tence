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
        # self.rect.topleft = self.gui.screen.topleft

class CoreHealth(pygame.sprite.Sprite):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.gui = gui
        self.font = pygame.font.Font(pygame.font.get_default_font(),20)
        self.image = None
        self.rect = None

    def update(self):
        core = self.gui.state.entity_group.get_group("core").sprites()[0] #show 1 core only
        self.image = self.font.render(str(int(core.health)), True, RED, BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottomright = self.gui.rect.bottomright

class MenuBox(pygame.sprite.Sprite):
    def __init__(self,gui):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.gui = gui
        self.size = (self.gui.size[0],40)
        self.image = pygame.Surface(self.size)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.gui.rect.bottomleft

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