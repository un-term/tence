import pygame

class EntityGroup:
    """All imported entities are being drawn"""
    def __init__(self, entity_list):
        self.state = None

        self.dict = {}

        default_groups = ["all","draw","remove","collision","sound","camera"]
        self._create_groups_from_list(default_groups)

        self.default_add_ent_group = ["all"]

        self.add_ent(entity_list)

    def add_ent(self, entity_list, group_list=["draw"]):
        #create groups
        self._create_groups_from_ent(entity_list)
        self._create_groups_from_list(group_list)
        #add entities to groups
        self._add_ent_to_default_group(entity_list)
        self._add_ent_to_own_group(entity_list)
        self._add_ent_from_list(entity_list,group_list)
        #ref
        self.link_ent_to_entity_group(entity_list)

    def _create_groups_from_ent(self, entity_list):
        for entity in entity_list:
            if not self.dict.get(entity.type):
                self.dict.update({entity.type:pygame.sprite.Group()})
        
    def _create_groups_from_list(self,group_list):
        for group in group_list:
            if not self.dict.get(group):
                self.dict.update({group:pygame.sprite.Group()})

    def _add_ent_to_default_group(self,entity_list):
        for entity in entity_list:
            for group in self.default_add_ent_group:
                if not entity in self.dict[group]:
                    self.dict[group].add(entity)

    def _add_ent_to_own_group(self,entity_list):
        for entity in entity_list:
            if not entity in self.dict[entity.type]:
                self.dict[entity.type].add(entity)

    def _add_ent_from_list(self,entity_list,group_list):
        for entity in entity_list:
            for group in group_list:
                if not entity in self.dict[group]:
                    self.dict[group].add(entity)

    def rm_ent_from_all_groups(self, group_list):
        """remove entities in this list of groups from all groups"""
        for group in group_list:
            for entity in self.dict[group]:
                entity.kill()

    def empty_this_group_only(self, group):
        """remove entities in this list of groups from all groups"""
        self.dict[group].empty()

    def link_ent_to_entity_group(self,entity_list):
        for entity in entity_list:
            entity.entity_group = self

    def get_group(self,group_name):
        if not group_name in self.dict:
            return None
        else:
            return self.dict[group_name]

    def find_overlap(self,group1,group2):
        overlap = []
        if self.get_group(group1) and self.get_group(group2):
            for entity_gp1 in self.get_group(group1):
                for entity_gp2 in self.get_group(group2):
                    if entity_gp1 == entity_gp2:
                        overlap.append(entity_gp1)
            return overlap
        else:
            return overlap

    def group_collision_detection(self, entity_group, target_group, collision_function):
        return pygame.sprite.groupcollide(entity_group, target_group, False, False, collided=collision_function)
