import pygame

class EntityGroup:
  """all imported entities are being drawn"""
  def __init__(self,game_ref):
    self.game = game_ref
    
    self.dict = {}

    default_groups = ["all","draw","remove"]
    self._create_groups_from_list(default_groups)

    self.default_add_ent_group = ["all"]
    # self.add_ent(entity_list)

  def add_ent(self, entity_list, group_list=["draw"]):
    #create groups
    self._create_groups_from_ent(entity_list)
    self._create_groups_from_list(group_list)
    #add entities to groups
    self._add_ent_to_default_group(entity_list)
    self._add_ent_to_own_group(entity_list)
    self._add_ent_from_list(entity_list,group_list)
    #ref
    self.link_ent_to_entity_group(self.dict["all"])

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

  def remove_ent_from_group(self, group_list):
    """remove entities in this list of groups from all groups"""
    for group in group_list:
      for entity in self.dict[group]:
        entity.kill()

  def link_ent_to_game(self,entity_list):
    for entity in entity_list:
      entity.game = self.game

  def get_group(self,group_name):
    group = self.dict[group_name]

    if group is None:
        raise TypeError("group does not exist")
    # elif not group:
    #   raise KeyError(group_name)
    else:
      return group

  # def __len__(self):
  #   return len(self.dict)

  # def __getitem__(self, key): # x[key]
  #   """change - introduce more checks"""
  #   found = self.dict[key]
  #   if found is None:
  #       raise TypeError('not indexable')
  #   elif not found:
  #     raise KeyError(key)
  #   else:
  #     return self.dict[key]
    # found = dict[key]
  
  # def __setitem__(self, key, value): # x[key] = value
  #   if self.dict is None:
  #     raise TypeError('not indexable')
    
  #   self.dict[key] = value
