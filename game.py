#!/usr/bin/env python

import pygame
import math
import random
#import pygame as pygame

WINSIZE = [640, 480]
white = (255, 240, 200)
black = (20, 20, 40)
red =   (255,   0,   0)
BLUE = (0,0,255)
DEEPSKYBLUE = (0,191,255)
YELLOW = (255,255,0)

def pol2cart(r, phi):
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return(x, y)

def vector_add(v1,v2):
  v3_x = v1[0]+v2[0]
  v3_y = v1[1]+v2[1]
  return (v3_x,v3_y)

def magnitude(v):
  mag = math.sqrt(v[0]**2 + v[1]**2)
  return mag

class Screen:
  def __init__(self,size):
    self.grid_size = 10

class Turret(pygame.sprite.Sprite):
  # Constructor
  def __init__(self,position,ammo,range,damage):
    # Call the parent class (Sprite) constructor
    pygame.sprite.Sprite.__init__(self)  

    self.radius = 100 # shoot range - circle collision detection
    self.ammo = ammo
    self.reloading = 0
    self.damage = damage
    self.head_angle = 0
    self.angle_speed = math.pi/12 # degree/frame
    self.laser_list = []

    # body
    self.image = pygame.Surface((30,30))
    self.image.fill(DEEPSKYBLUE)
    # Fetch the rectangle object that has the dimensions of the image
    # Update the position of this object by setting the values of rect.x and rect.y
    self.rect = self.image.get_rect()
    self.rect.center = position

    # scanner
    self.scan_line_start = self.rect.center
    self.scan_line_end = (self.rect.center[0],self.rect.center[1]+self.radius)
    self.image.fill(DEEPSKYBLUE)

  def update(self,line_list):
    # self._scan(line_list)
    self.reloading = 0

  # def _scan(self,line_list, baddie_group_in_range):
  # def _scan(self,line_list):
  #   print("updating scan")
  #   self.head_angle += math.pi/24
  #   print(self.head_angle)

  #   self.Vg_scan_line = vector_add(pol2cart(self.radius,self.head_angle),self.position)

  #   line_list.append(Line(YELLOW,self.position,self.Vg_scan_line))

  #   if self.head_angle > 2*math.pi:
  #     self.head_angle -= 2*math.pi

  def shoot(self,baddie,line_list):
    if not self.reloading:
      if self.ammo > 0:
        #create rect along firing line
        # self.ammo-=1 #CHANGE - commented to testing
        # print("shoot!")
        baddie.health -= self.damage
        self.laser_list.append(Line(red,self.rect.center,baddie.rect.center)) #CHANGE - remove dead baddie from lists
      # CHANGE - add laser list to each turret object
    # else:
      # print("Out of ammo")

class Baddie(pygame.sprite.Sprite):
  def __init__(self, health,position):
    pygame.sprite.Sprite.__init__(self)  

    self.health = health

    self.image = pygame.Surface((10,10))
    self.image.fill(white)
    self.radius = 10 # range - circle collision detection
    self.rect = self.image.get_rect()
    self.rect.center = position
    self.speed = 5 # pixes per second
    self.velocity = ()

  def calculate_velocity(self,turret):
    V_bt = vector_add(turret.rect.center,self.rect.center)
    m_V_bt = magnitude(V_bt)
    self.velocity = (self.speed*(V_bt[0]/m_V_bt),self.speed*(V_bt[1]/m_V_bt))

  def move(self,time):
    self.rect.center = vector_add(self.rect.center,(self.velocity[0]*time,self.velocity[1]*time))


class Line:
  def __init__(self,colour, start, end):
    self.colour = colour
    self.start = start
    self.end = end

  # def draw(self, surface):
  #   pygame.draw.line(surface,self.colour,self.start,self.end)

class RenderLines:
  def __init__(self):
    self.lines_list = []
  def storelines(self,line_list):
    self.lines_list = line_list
  def draw(self, surface):
    for line in self.lines_list:
      pygame.draw.line(surface,line.colour,line.start,line.end)

class Events:
  def __init__(self):
    self.done = 0
    self.create = 0
  # def eventCheck:
  #   if mousepressed:
  #     createBaddie
  
  def mouse_press(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        self.done = 1
        break
        
      mouse_buttons = pygame.mouse.get_pressed()
      if mouse_buttons[0] is True:
        print("mouse button 1 pressed")
        # self.create = 1
        return 1


def main():
  screen = pygame.display.set_mode(WINSIZE)
  pygame.display.set_caption("black")
  screen.fill(black)
  clock = pygame.time.Clock()

  baddie_list = []
  turret_list = []
  line_list = []
  # baddie = baddie(1,(300,300))
  baddie_list.append( Baddie(1,(300,300)) )
  baddie_list.append( Baddie(2,(200,300)) )
  baddie_list.append( Baddie(2,(175,200)) )
  baddie_list.append( Baddie(2,(50,75)) )
  baddie_list.append( Baddie(2,(100,50)) )
  turret_list.append( Turret((100,100),5,300,2) )

  baddiesprites = pygame.sprite.Group(baddie_list)
  turretsprites = pygame.sprite.Group(turret_list)
  # allsprites = pygame.sprite.RenderPlain(baddie_list,turret_list)
  allsprites = pygame.sprite.RenderPlain(baddiesprites,turretsprites)

  # print(pygame.sprite.spritecollide(turret_list[0],baddiesprites, False, pygame.sprite.collide_circle))

  # allsprites.reoffset(baddie_list[0])
  events = Events()
  # events.spawnBaddie(allsprites)
  # checkFireTargets(allsprites.sprites(), turret_list, line_list)
  alllines = RenderLines()
  alllines.storelines(line_list)



  initial = 1
  # main game loop
  events.done = 0
  hit_list = []
  time_passed = 0
  while not events.done:

    pygame.display.update()
    # Multiple turrets
    # Check targets and shoot!
    # hit_dict = pygame.sprite.groupcollide(turretsprites,baddiesprites, False, False, pygame.sprite.collide_circle)
    # for turretKey in hit_dict:
    #   for baddieValue in hit_dict[turretKey]:
    #     turretKey.shoot(baddieValue,line_list)
    
    # One turret
    # Check targets and shoot!
    # if not initial:
    #   if destroy:
    #     allsprites.remove(destroy)
    #     initial = 0
    # destroy = []

    if hit_list:
      print("Remove: ", hit_list[0])
      hit_list[0].kill()
      # baddiesprites.kill(hit_list[0])
      print("Remove: ", hit_list[0])

    # hit_list = pygame.sprite.spritecollide(turret_list[0],baddiesprites, False, pygame.sprite.collide_circle)
    if hit_list:
      print("Hit!")

    for baddie in hit_list:
      turret_list[0].shoot(baddie,line_list)

    # create baddie on mouse press
    if events.mouse_press():
      mouse_pos = pygame.mouse.get_pos()
      new_baddie = Baddie(2,mouse_pos)
      new_baddie.add(allsprites,baddiesprites)

    # loop through turret group and and loop through lines to draw
    time_passed_seconds = time_passed/1000
    allsprites.update(line_list)
    # allsprites.remove(destroy)
    
    # Move all baddies toward turret
    for baddie in baddiesprites:
      baddie.calculate_velocity(turret_list[0])
      baddie.move(time_passed_seconds)

    # screen.blit(background, (0, 0))
    screen.fill(black)
    allsprites.draw(screen)
    alllines.draw(screen)

    # for line in line_list:
    #   line.draw(screen)
    time_passed = clock.tick(60)
  pygame.quit()


# if python says run, then we should run
if __name__ == "__main__":
  main()
#     
