import pygame
from general_functions import *

class GraphicalSurface(pygame.sprite.Sprite):
    def __init__(self,parent):
        pygame.sprite.Sprite.__init__(self)
        # breakpoint()
        self.ui_parent = parent
        self.ui_children = []
        self.size = None
        self.colour = None
        self.rect = None
        self.camera_rect = None
        self.surface = None
        self.selectable = False
        self.type = self.__class__.__name__.lower()

    def set_surface_rect(self,size,colour):
        self.surface = self._set_surface(size)
        if colour: self._set_surface_colour(self.surface,colour)
        self.rect = self._set_rect(size)

    def change_size(self,size):
        self.surface = pygame.transform.smoothscale(self.surface,size)
        D_size = vector_subtract(size,self.rect.size)
        self.rect.inflate_ip(D_size)

    def _set_surface(self,size):
        return pygame.Surface(size)

    def _set_surface_colour(self,surface,colour):
        surface.fill(colour)
        
    def _set_rect(self,size):
        if self.rect:
            return pygame.Rect(self.rect.topleft, size)
        else:
            return pygame.Rect((0,0), size)

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
            item.draw()
