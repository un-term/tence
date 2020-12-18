import math
import random

def round_sig(x, sig=5):
  return round(x, sig - int(math.floor(math.log10(abs(x))))-1)

def round_sig_vector(V,sig=5):
  Vx = round_sig(V[0],sig)
  Vy = round_sig(V[1],sig)
  return (Vx,Vy)

def round_vector(V,digits):
  Vx = round(V[0],digits)
  Vy = round(V[1],digits)
  return (Vx,Vy)

def pol2cart(r, phi):
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return(x, y)

def vector_add(v1,v2):
  v3_x = v1[0]+v2[0]
  v3_y = v1[1]+v2[1]
  return (v3_x,v3_y)

def vector_subtract(v1,v2):
  v3_x = v1[0]-v2[0]
  v3_y = v1[1]-v2[1]
  return (v3_x,v3_y)

def vector_scalar_mult(v,a):
  vx = v[0]*a
  vy = v[1]*a
  return(vx,vy)

def calc_const_velocity(mover, target, speed):
  """velocity vector between 2 positions with constant speed
    S - position vector, V - velocity vector
    m - mover, t - target
  """
  # position vector between mover & target
  S_mt = vector_subtract(target,mover)
  # distance between mover & target
  magS_mt = magnitude(S_mt)
  # direction from mover to target
  unitS_mt = unit_vector(S_mt)

  return vector_scalar_mult(unitS_mt,speed)

def new_position(position,velocity,time):
  """change in position over time with constant velocity"""
  vector_distance = vector_scalar_mult(velocity,time)
  return vector_add(position,vector_distance)

def magnitude(v):
  mag = math.sqrt(v[0]**2 + v[1]**2)
  return mag

def unit_vector(v):
  vmag = magnitude(v)
  unit_vx = v[0]/vmag
  unit_vy = v[1]/vmag
  return(unit_vx,unit_vy)

def grid_snap_vector(grid,V):
  rx = math.remainder(V[0],grid[0])
  ry = math.remainder(V[1],grid[1])
  return(V[0]-rx, V[1]-ry)

def remove_obj(obj,obj_list):
  """remove object from list of objects"""
  return obj_list.remove(obj)