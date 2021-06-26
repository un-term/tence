import pygame
import pygame.freetype
from constants import *
from general_functions import *
import entity
import graphical_surface

def resize_rect_and_surface(rect, surface, size):
    center = rect.center
    rect = pygame.Rect((0,0), size)
    rect.center = center
    surface = pygame.transform.scale(surface, size)
    return rect, surface


class SimpleStore:
    def __init__(self):
        self.shelf = None

    def change(self,value):
        self.shelf = value

class InterfaceSurface(graphical_surface.GraphicalSurface):
    def __init__(self,parent):
        graphical_surface.GraphicalSurface.__init__(self,parent)
        self.surface = None


class SelectionBox(InterfaceSurface):
    def __init__(self,parent,menu_height,selection_store):
        InterfaceSurface.__init__(self,parent)
        self.colour = BLACK
        size = (menu_height, menu_height)
        self.create_surface_and_rect(size, self.colour)
        self.rect.topright = (self.ui_parent.rect.topright[0], 0) # relative to parent
        self.store_surface = self.surface

        self.selection_store = selection_store # ref

    def update_gui(self):
        if self.selection_store.shelf:
            self.surface = self.selection_store.shelf.surface.copy()
            self.surface = pygame.transform.scale(self.surface, self.rect.size)  # fit surface to rect
        else:
            self.surface = self.store_surface 

        for item in self.ui_children:
            item.update_gui()


class MenuItem(InterfaceSurface):
    def __init__(self, parent, type, rect, surface):
        InterfaceSurface.__init__(self, parent)
        self.type = type
        self.rect = rect
        self.surface = surface
        self.selectable = True


class MenuBox(InterfaceSurface):
    def __init__(self,parent,menu_height):
        InterfaceSurface.__init__(self,parent)
        self.colour = GREY
        size = (self.ui_parent.rect.size[0]-menu_height,self.ui_parent.rect.size[1])
        self.create_surface_and_rect(size, self.colour)
        self.rect.topleft = (0,0) # relative to parent

        self.menu_entity_offset = 5
        self.menu_item_size = (30,30)

    def add_menu_entity(self,entity_menu_items):
        for count, item in enumerate(entity_menu_items):
            dist = self.menu_item_size[0] + self.menu_entity_offset
            coord_x = dist * (count+1) - 0.5*self.menu_item_size[0]
            rect, surface = resize_rect_and_surface(item.rect, item.surface, self.menu_item_size)
            menu_item = MenuItem(self, item.type, rect, surface)
            menu_item.rect.center = (coord_x, self.rect.center[1])
            self.ui_children.append(menu_item)

    def click(self,local_coord):
        found = None
        for item in self.ui_children:
            if item.rect.collidepoint(local_coord):
                found = item
        if found:
            return entity.factory(found.type, (0,0))
        else:
            return None


class Menu(InterfaceSurface):
    def __init__(self,parent,menu_height):
        InterfaceSurface.__init__(self,parent)
        self.menu_height = menu_height
        self.colour = BLACK
        size = (self.ui_parent.rect.size[0],self.menu_height)
        self.create_surface_and_rect(size, self.colour)
        self.rect.topleft = (0,self.ui_parent.rect.size[1] - self.menu_height) # relative to parent


class Screen(InterfaceSurface):
    def __init__(self,parent,display,size):
        InterfaceSurface.__init__(self,parent)

        self.colour = BLACK
        self.create_surface_and_rect(size, self.colour)
        self.surface = display.set_mode(size)


class EndGame(InterfaceSurface):
    def __init__(self ,parent, parent_rect):
        InterfaceSurface.__init__(self, parent)
        self.bg_colour = BLACK
        self.text_colour= GREEN

        # Font https://nerdparadise.com/programming/pygame/part5
        font = pygame.freetype.Font(None ,60)  # None - default system font
        self.surface, self.rect  = font.render("GAME OVER", self.text_colour, self.bg_colour) # text 
        self.rect.center = parent_rect.center

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

class Camera(InterfaceSurface):
    '''Straddling both coordinate systems'''
    def __init__(self, parent, state, size):
        InterfaceSurface.__init__(self, parent)
        self.state = state
        self.colour = BLACK
        self.size = size
        self.map_size = self.size
        self.surface = None
        self.rect = None
        self.draw_list = []
        # map coordinatey system
        self.map_rect = None
        # self.camera_rect = None
        self.zoom_level = 1

    def specific_setup(self, camera_map_center):
        '''Does not use base class methods'''
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.colour)
        self.map_rect = pygame.Rect((0,0), self.map_size)
        self.map_rect.center = camera_map_center
        # screen coordinate system
        self.rect = pygame.Rect((0,0), self.size)

    def change_size(self, new_size):
        '''Change camera map size'''
        self.surface = pygame.transform.scale(self.surface, new_size)
        # Keep camera centered on current position
        center = self.map_rect.center
        D_size = vector_subtract(new_size, self.map_rect.size)
        self.map_rect.inflate_ip(D_size)
        self.map_rect.center = center
        
    def draw(self):
        '''Overloading base class draw method
        Copies surface and rects for drawing'''
        # Draw entities
        self.draw_list.clear()
        map_ents = self.map_capture("draw")
        self.draw_list.extend(self.convert_map_ents_to_camera(map_ents))
        self.surface.fill(self.colour)
        for rect_surf in self.draw_list:  # tuple
            self.surface.blit(rect_surf[1], rect_surf[0])
        # Draw special effects
        if self.state.entity_group.get_group("special_effects"):
            self.draw_list.clear()
            map_effects = self.map_capture("special_effects")
            self.draw_list.extend(self.convert_map_ents_to_camera(map_effects))
            for rect_surf in self.draw_list:  # tuple
                self.surface.blit(rect_surf[1], rect_surf[0])
        
    def map_capture(self, group_name):
        '''Scale map_rect for zooom'''
        center = self.map_rect.center
        zoom_size = vector_scalar_mult(self.map_rect.size, 1.0/self.zoom_level)
        map_sprite = pygame.sprite.Sprite()
        map_sprite.rect = pygame.Rect((0,0), zoom_size)
        map_sprite.image = None
        map_sprite.rect.center = center
        return pygame.sprite.spritecollide(map_sprite, self.state.entity_group.get_group(group_name), False, pygame.sprite.collide_rect)

    def convert_map_ents_to_camera(self, map_ents):
        '''Camera movement and zoom
           See notes for explanation'''
        camera_rect_surface = []
        for ent in map_ents:
            ent_position = ent.position # Cannot copy rect since it uses integers
            ent_size = ent.rect.size
            ent_surface = ent.surface.copy()
            
            # zoom to centre of camera
            ent_position = vector_subtract(ent_position, self.map_rect.center)

            # Scale position vector and size according to zoom factor
            ent_size = vector_scalar_mult(ent_size, self.zoom_level)
            ent_rect = pygame.Rect((0,0), ent_size)
            ent_position = vector_scalar_mult(ent_position, self.zoom_level)
            ent_surface = pygame.transform.scale(ent_surface, vector_convert_to_integer(ent_size))

            # Adjust for blitting on camera screen (topleft)
            ent_position = vector_add(self.rect.center, ent_position)

            ent_rect.center = ent_position
            camera_rect_surface.append((ent_rect, ent_surface))
        # self.zoom_level = 1
        return camera_rect_surface

    # def translate_map_vector_to_camera_vector(self, map_V):
    #     '''map vectors from map origin (x,y)
    #        camera vectors from top left corner (x,-y)'''
    #     return vector_subtract(map_V, self.map_rect.topleft)

    def translate_camera_vector_to_map_vector(self, ctl_ze):
        '''e - entity
           ctl - camera top left
           cc - camera center
           m - map origin
           z - scaled'''
        cc_ze = vector_subtract(ctl_ze, self.rect.center) # camera_V is mouse_pos
        cc_e = vector_scalar_mult(cc_ze, 1.0/self.zoom_level)
        m_e = vector_add(self.map_rect.center, cc_e)
        return vector_convert_to_integer(m_e)

    def add_selection(self, state, selection, local_mouse_pos):
        selection.position = local_mouse_pos
        state.entity_group.add_ent([selection])

    def move(self, movement):
        self.map_rect.move_ip(movement)

    def zoom(self, factor):
        zoom_level = self.zoom_level + factor
        if zoom_level > 0:
            self.zoom_level = zoom_level


class GUI:
    def __init__(self, display, state, camera_size=(700, 700)):
        self.state = state
        # self.camera = camera
        menu_height = 40
        self.size = (camera_size[0], camera_size[1] + menu_height)
        self.display = display

        # self.selected_list = []
        self.selection_store = SimpleStore()
        self.start_wall_V = None
        self.ui_elements = {} # > python 3.7 dict ordering from order added

        # Instantiate surfaces
        self.ui_elements["screen"] = Screen(None, self.display, self.size)
        # Camera setup
        camera_size = (self.size[0], self.size[1] - menu_height)
        self.ui_elements["camera"] = Camera(self.ui_elements["screen"], self.state, camera_size)
        self.ui_elements["camera"].specific_setup((0,0))  # Center camera around origin

        self.ui_elements["menu"] = Menu(self.ui_elements["screen"],menu_height)
        self.ui_elements["menu_box"] = MenuBox(self.ui_elements["menu"],menu_height)
        self.ui_elements["selection_box"] = SelectionBox(self.ui_elements["menu"],menu_height,self.selection_store)
        entity_menu_items = [entity.Turret((0,0)),entity.Wall((0,0))]
        self.ui_elements["menu_box"].add_menu_entity(entity_menu_items)

        # populate ui_children
        for item in self.ui_elements.values():
            if item.ui_parent:
                item.ui_parent.ui_children.append(item)

    def update(self):
        self.ui_elements["screen"].update_gui()  # Recursion
        self.special_effects_update()
        pass

    def draw(self):
        for item in self.ui_elements.values():
            item.draw()
        self.display.update()

    def click(self,mouse_pos):
        coord_store = SimpleStore()

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
                        point_list = gen_coords_from_range(self.start_wall_V,end_wall_V,spacing=wall.rect.size[0])
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

    def move_camera(self, movement):
        self.ui_elements["camera"].move(movement)

    def zoom_camera(self, factor):
        self.ui_elements["camera"].zoom(factor)

    def display_game_over(self):
        screen = self.ui_elements["screen"]
        end_game = EndGame(screen, screen.rect)
        screen.ui_children.clear()
        screen.ui_children.append(end_game)
        screen.draw()
        self.display.update()

    def special_effects_update(self):
        se_group = self.state.entity_group.get_group("special_effects")
        if se_group:
            for effect in se_group:
                time_elapsed = self.state.total_time - effect.created_timestamp
                if time_elapsed > effect.alive_duration:
                    effect.kill()
