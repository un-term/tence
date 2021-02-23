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
        self.surface = None
        self.selectable = False

    def set_surface_rect(self,size,colour):
        self.surface = self._set_surface(size)
        if colour: self._set_surface_colour(self.surface,colour)
        self.rect = self._set_rect(size)

    def change_size(self,size):
        self.surface = self._set_surface(size)
        if self.colour: self._set_surface_colour(self.surface,self.colour)
        center = self.rect.center
        self.rect = self._set_rect(size)
        self.rect.center = center

    def change_position(self,rect_place,coord):
        rect_place = coord

    def _set_surface(self,size):
        return pygame.Surface(size)

    def _set_surface_colour(self,surface,colour):
        surface.fill(colour)
        
    def _set_rect(self,size):
        return pygame.Rect((0,0),size)

    def update(self):
        pass

    def draw(self):
        if self.colour:
            self.surface.fill(self.colour)
        for item in self.ui_children:
            self.surface.blit(item.surface,item.rect)
            try: item.draw()
            except: pass

    def click_select(self,mouse_pos, parent_rect, selected_list):
        mouse_pos = coord_sys_map_translation(parent_rect.topleft,mouse_pos)
        parent_rect = self.rect
        if self.rect.collidepoint(mouse_pos):
            if self.selectable: selected_list.append(self.__class__((0,0)))
            if not selected_list:
                for item in self.ui_children:
                    try: item.click_select(mouse_pos, parent_rect, selected_list)
                    except: pass

    def click_placement(self,mouse_pos, parent_rect, selected, target_rect, state):
        mouse_pos = coord_sys_map_translation(parent_rect.topleft,mouse_pos)
        parent_rect = self.rect
        if target_rect.collidepoint(mouse_pos):
            selected.position = mouse_pos
            print(selected, selected.position)
            state.entity_group.add_ent([selected])
        else:
            for item in self.ui_children:
                try: item.click_place(mouse_pos, parent_rect, selected, target_rect, state)
                except: pass     
