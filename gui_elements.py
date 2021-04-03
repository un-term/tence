import pygame

from constants import *
from general_functions import *
import entity
import graphical_surface


class SimpleStore:
    def __init__(self):
        self.shelf = None

    def change(self,value):
        self.shelf = value


class SelectionBox(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height,selection_store):
        graphical_surface.GraphicalSurface.__init__(self,parent)
        
        self.colour = BLACK
        self.size = (menu_height, menu_height)
        self.set_surface_rect(self.size, self.colour)
        self.rect.topright = (self.ui_parent.rect.topright[0], 0) # relative to parent
        self.store_surface = self.surface

        self.selection_store = selection_store # ref

    def update_gui(self):
        if self.selection_store.shelf:
            self.surface = self.selection_store.shelf.surface.copy()
            self.change_size(self.size)
        else:
            self.surface = self.store_surface 

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
            dist = self.menu_item_size[0] + self.menu_entity_offset
            coord_x = dist * (count+1) - 0.5*self.menu_item_size[0]
            item.position = (coord_x,self.rect.center[1])
            item.change_size(self.menu_item_size)
            item.selectable = True

            self.ui_children.append(item)

    def click(self,local_coord):
        found = None
        for item in self.ui_children:
            if item.rect.collidepoint(local_coord):
                found = item
        if found:
            return found.__class__((0,0))
        else:
            return None


class Menu(graphical_surface.GraphicalSurface):
    def __init__(self,parent,menu_height):
        graphical_surface.GraphicalSurface.__init__(self,parent)

        self.menu_height = menu_height
        self.colour = BLACK
        self.size = (self.ui_parent.size[0],self.menu_height)
        self.set_surface_rect(self.size,self.colour)
        self.rect.topleft = (0,self.ui_parent.size[1] - self.menu_height) # relative to parent


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

class Camera(graphical_surface.GraphicalSurface):
    '''Straddling both coordinate systems'''
    def __init__(self, parent, state, size):
        graphical_surface.GraphicalSurface.__init__(self, parent)
        self.state = state
        self.colour = BLACK
        self.size = size
        self.surface = None
        self.rect = None
        # Coordinate systems
        self.map_rect = None
        # self.camera_rect = None

    def specific_setup(self, camera_map_center):
        '''Does not use base class methods'''
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)
        # map coordinatey system
        self.map_rect = pygame.Rect((0,0), self.size)
        self.map_rect.center = camera_map_center
        # screen coordinate system
        self.rect = pygame.Rect((0,0), self.size)

    def capture(self):
        '''Clear children and then add entities that are within collision box'''
        ''' CHANGE - check if camera position has changed'''
        self.ui_children.clear()
        for ent in self.state.entity_group.get_group("draw"):
            if ent.rect.colliderect(self.map_rect):
                ent.camera_rect = ent.rect.copy()
                ent.camera_rect.center = self.translate_map_vector_to_camera_vector(ent.rect.center)
                self.ui_children.append(ent)

    def translate_map_vector_to_camera_vector(self, map_V):
        '''map vectors from map origin (x,y)
           camera vectors from top left corner (x,-y)'''
        return vector_subtract(map_V, self.map_rect.topleft)

    def translate_camera_vector_to_map_vector(self, camera_V):
        return vector_add(camera_V, self.map_rect.topleft)

    def draw(self):
        '''Overloading base class draw method'''
        self.surface.fill(self.colour)
        for ent in self.ui_children:
            self.surface.blit(ent.surface, ent.camera_rect)

    def add_entity(self, entity_group):
        self.ui_children = entity_group

    def add_selection(self, state, selection, local_mouse_pos):
        selection.position = local_mouse_pos
        state.entity_group.add_ent([selection])


class GUI:
    def __init__(self, state, winsize=(700, 700)):
        self.state = state
        # self.camera = camera
        self.size = winsize
        self.display = pygame.display
        menu_height = 40

        # self.selected_list = []
        self.selection_store = SimpleStore()
        self.start_wall_V = None
        self.ui_elements = {}

        # Instantiate surfaces
        self.ui_elements["screen"] = Screen(None, self.display, self.size)
        # Camera setup
        camera_size = (self.size[0], self.size[1] - menu_height)
        self.ui_elements["camera"] = Camera(self.ui_elements["screen"], self.state, camera_size)
        self.ui_elements["camera"].specific_setup((100,100))  # Center camera around origin

        self.ui_elements["menu"] = Menu(self.ui_elements["screen"],menu_height)
        self.ui_elements["menu_box"] = MenuBox(self.ui_elements["menu"],menu_height)
        self.ui_elements["selection_box"] = SelectionBox(self.ui_elements["menu"],menu_height,self.selection_store)
        entity_menu_items = [entity.Core((0,0)),entity.Turret((0,0)),entity.Wall((0,0)),entity.Spawn((0,0))]
        self.ui_elements["menu_box"].add_menu_entity(entity_menu_items)

        # populate ui_children
        for item in self.ui_elements.values():
            if item.ui_parent:
                item.ui_parent.ui_children.append(item)

    def update(self):
        self.ui_elements["screen"].update_gui()  # Recursion
        pass

    def draw(self):

        self.ui_elements["camera"].capture()
        self.ui_elements["screen"].draw()  # Recursion through depends

        self.display.update()

    def click(self,mouse_pos):
        coord_store = SimpleStore()
        print(mouse_pos)

        screen = self.ui_elements["screen"]
        camera = self.ui_elements["camera"]
        menu = self.ui_elements["menu"]
        menu_box = self.ui_elements["menu_box"]

        # Selection - placement
        if camera.rect.collidepoint(mouse_pos):
            if self.selection_store.shelf:
                if self.selection_store.shelf.type == "wall":
                    if not self.start_wall_V:
                        self.start_wall_V = camera.translate_camera_vector_to_map_vector(mouse_pos)
                    else:
                        wall = entity.Wall((0,0))
                        end_wall_V = camera.translate_camera_vector_to_map_vector(mouse_pos)
                        print(self.start_wall_V, end_wall_V)
                        point_list = gen_coords_from_range(self.start_wall_V,end_wall_V,spacing=wall.size[0])
                        for point in point_list:
                            self.state.entity_group.add_ent([entity.Wall(point)])
                        self.selection_store.change(None)
                        self.start_wall_V = None

                else:
                    mouse_pos = camera.translate_camera_vector_to_map_vector(mouse_pos)
                    # mouse_pos = coord_sys_map_translation(camera.rect.topleft, mouse_pos)
                    camera.add_selection(self.state, self.selection_store.shelf, mouse_pos)
                    self.selection_store.change(None)


        # Selection - store
        elif menu.rect.collidepoint(mouse_pos):
            self.get_local_coord_from_target(mouse_pos, screen, menu_box, coord_store)
            if coord_store.shelf:
                self.selection_store.change(menu_box.click(coord_store.shelf))

    def get_local_coord_from_target(self, mouse_pos, parent, target, coord_store):
        '''Recursive function. Moves down through surfaces until target
        surface'''
        mouse_pos = coord_sys_map_translation(parent.rect.topleft, mouse_pos)
        if parent.rect == target.rect and target.rect.collidepoint(mouse_pos):
            coord_store.change(mouse_pos)
        else:
            for item in parent.ui_children:
                try:
                    self.get_local_coord_from_target(mouse_pos, item, target, coord_store)
                except:
                    print("recusrive function call error")

    def move_camera(self, direction):
        if direction == "down":
            self.ui_elements["camera"].map_rect.center = vector_add(self.ui_elements["camera"].map_rect.center, (0,10))
        elif direction == "up":
            self.ui_elements["camera"].map_rect.center = vector_add(self.ui_elements["camera"].map_rect.center, (0,-10))
        elif direction == "right":
            self.ui_elements["camera"].map_rect.center = vector_add(self.ui_elements["camera"].map_rect.center, (10,0))
        elif direction == "left":
            self.ui_elements["camera"].map_rect.center = vector_add(self.ui_elements["camera"].map_rect.center, (-10,0))
