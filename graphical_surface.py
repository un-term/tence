import pygame
from general_functions import *

class GraphicalSurface(pygame.sprite.Sprite):
    def __init__(self,parent):
        pygame.sprite.Sprite.__init__(self)
        # Takes class name 
        self.type = self.__class__.__name__.lower()
        self.ui_parent = parent
        self.ui_children = []
        self.colour = None
        self.rect = None
        self.camera_rect = None
        # Surface should be specified in the class that inherits from this one 
        # self.surface = None
        self.selectable = False

    def create_surface_and_rect(self, size, colour):
        # Surface
        self.surface = pygame.Surface(size)
        if colour:
            self.surface.fill(colour)
        # Rect
        if self.rect:
            self.rect = pygame.Rect(self.rect.topleft, size)
        else:
            self.rect = pygame.Rect((0,0), size)

    def change_colour(self, colour):
        self.surface.fill(colour)

    def update(self):
        pass

    def update_gui(self):
        for item in self.ui_children:
            item.update_gui()

    def draw(self):
        if self.colour:
            self.surface.fill(self.colour)
        for item in self.ui_children:
            self.surface.blit(item.surface,item.rect)
            # item.draw()
