import pygame

from constants import *
from general_functions import *
import entity
import graphical_surface


class SelectionBox(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height,selected_list):
        graphical_surface.GraphicalSurface.__init__(self,parent)
        
        self.colour = BLACK
        self.size = (menu_height,menu_height)
        self.set_surface_rect(self.size,self.colour)
        self.rect.topright = (self.ui_parent.rect.topright[0],0) # relative to parent
        self.store_surface = self.surface

        self.selected_list = selected_list # ref

    def update_gui(self):
        if self.selected_list:
            self.surface = self.selected_list[0].surface.copy()
            self.change_size(self.size)
        else: self.surface = self.store_surface 

        for item in self.ui_children:
            item.update_gui()


class MenuBox(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height):
        graphical_surface.GraphicalSurface.__init__(self,parent)

        self.colour = GREY
        self.size = (self.ui_parent.size[0]-menu_height,self.ui_parent.size[1])
        self.set_surface_rect(self.size,self.colour)
        self.rect.topleft = (0,0) # relative to parent

        self.menu_entity_offset = 5
        self.menu_item_size = (30,30)

    def add_menu_entity(self,entity_menu_items):
        for count, item in enumerate(entity_menu_items):
            # print(item)
            dist = self.menu_item_size[0] + self.menu_entity_offset
            coord_x = dist * (count+1) - 0.5*self.menu_item_size[0]
            # print("Coord: ", (coord_x,self.menu_item_size[1]/2.0))
            # print(item.rect.midright)
            item.position = (coord_x,self.rect.center[1])
            item.change_size(self.menu_item_size)
            item.selectable = True

            self.ui_children.append(item)  


class Menu(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height):
        graphical_surface.GraphicalSurface.__init__(self,parent)

        self.menu_height = menu_height
        self.colour = BLACK
        self.size = (self.ui_parent.size[0],self.menu_height)
        self.set_surface_rect(self.size,self.colour)
        self.rect.topleft = (0,self.ui_parent.size[1] - self.menu_height) # relative to parent


class Map(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height):
        graphical_surface.GraphicalSurface.__init__(self,parent)

        self.menu_height = menu_height
        self.colour = BLACK
        self.size = (self.ui_parent.size[0],self.ui_parent.size[1] - self.menu_height)
        self.set_surface_rect(self.size,self.colour)
        self.rect.topleft = self.ui_parent.rect.topleft # relative to parent

    def add_entity(self,entity_group):
        self.ui_children = entity_group


class Screen(graphical_surface.GraphicalSurface):
    def __init__(self,parent,display,size):
        graphical_surface.GraphicalSurface.__init__(self,parent)

        self.colour = BLACK
        self.size = size
        self.set_surface_rect(self.size,self.colour)
        self.surface = display.set_mode(size) # Overwrite surface

        
# CHANGE - not updated and won't work
# class KillCount(pygame.sprite.Sprite):
#     def __init__(self,gui):
#         # Call the parent class (Sprite) constructor
#         pygame.sprite.Sprite.__init__(self)
#         self.gui = gui
#         self.font = pygame.font.Font(pygame.font.get_default_font(),20)
#         self.image = None
#         self.rect = None

#     def update(self):
#         self.image = self.font.render(str(self.gui.state.kill_count), True, GREEN, BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.bottomright = self.gui.menu_rect.bottomright

class GUI:
    def __init__(self,state,winsize=(700, 700)):
        self.state = state
        self.size = winsize
        self.display = pygame.display

        self.selected_list = []

        # Instantiate surfaces
        self.screen = Screen(None,self.display,self.size)
        menu_height=40
        self.map = Map(self.screen,menu_height)
        self.map.add_entity(self.state.entity_group.get_group("draw"))
        menu = Menu(self.screen,menu_height)
        menu_box = MenuBox(menu,menu_height)
        selection_box = SelectionBox(menu,menu_height,self.selected_list)
        entity_menu_items = [entity.Core((0,0)),entity.Turret((0,0)),entity.Wall((0,0)),entity.Spawn((0,0))]
        menu_box.add_menu_entity(entity_menu_items)

        ui_element_list = [self.screen,self.map,menu,menu_box,selection_box]
        # populate ui_children
        for item in ui_element_list:
            if item.ui_parent:
                item.ui_parent.ui_children.append(item)

    def update(self):
        self.screen.update_gui()

    def draw(self):
        """Draws using the coordinate system of the surface being drawn onto"""

        self.screen.draw() # Recursion through depends

        self.display.update()

    def click(self,mouse_pos):
        if self.selected_list:
            self.screen.click_placement(mouse_pos,self.screen.rect,self.selected_list[0],self.map.rect,self.state)
            self.selected_list.clear()
        else:
            self.screen.click_select(mouse_pos,self.screen.rect,self.selected_list)