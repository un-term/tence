import math

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

def pol2cart(V):
    r = V[0]
    phi = V[1]
    x = r * math.cos(phi)
    y = r * math.sin(phi)
    return(x, y)

def cart2pol(V):
    x = V[0]
    y = V[1]
    r = magnitude(V)
    phi = abs(math.atan(y/x))
    if x > 0 and y > 0:
        pass
    elif x < 0 and y > 0:
        phi = math.pi - phi
    elif x < 0 and y < 0:
        phi = math.pi + phi
    elif x > 0 and y < 0:
        phi = 2.0*math.pi - phi

    elif x == 0 and y > 0:
        phi = math.pi/2.0
    elif x == 0 and y < 0:
        phi = (3.0/2.0)*math.pi
    elif x == 0 and y == 0:
        raise ValueError("Undefined")
    return(r, phi)

def rad2deg(phi):
    return phi*(360.0/(2*math.pi))

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

def vector_abs(V):
    Vx = abs(V[0])
    Vy = abs(V[1])
    return(Vx,Vy)

def vector_vector_midpoint(V1,V2):
    """mindpoint between two vectors"""
    V_12 = vector_subtract(V2,V1)
    return vector_add(V1,vector_scalar_mult(V_12,0.5))

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

def coord_sys_map_translation(offset, V_g):
    """mapping global (g) to local (l)"""
    return vector_subtract(V_g,offset)

def sort_vector_small_big(V1,V2):
    """return smaller and then bigger vector along specified axis"""
    if V1[1]==V2[1]:
        if V1[0] < V2[0]:
            return V1,V2
        elif V1[0] > V2[0]:
            return V2,V1
        elif V1[0] == V2[0]:
            return V1,V2
    elif V1[0]==V2[0]:
        if V1[1] < V2[1]:
            return V1,V2
        elif V1[1] > V2[1]:
            return V2,V1
        elif V1[1] == V2[1]:
            return V1,V2
    else:
        raise Exception("Start and End coordinates are not on the required axis")

def snap_to_nearest_axis(start, end):
    diff_V = vector_abs(vector_subtract(start,end))
    if diff_V[0] < diff_V[1]:
        new_end = (start[0],end[1])
    else:
        new_end = (end[0],start[1])
    return new_end 

def gen_coords_from_range(start, end, spacing):
    """note: points created from and on start. 
            non-whole end spacings ignored"""
    end = snap_to_nearest_axis(start, end)
    (start,end) = sort_vector_small_big(start,end)
    point_list = []
    if start[1]==end[1]:
        y_const = start[1]
        for i in range(start[0],end[0],spacing):
            point_list.append((i,y_const))
    elif start[0]==end[0]:
        x_const = start[0]
        for i in range(start[1],end[1],spacing):
            point_list.append((x_const,i))
    else: 
        raise Exception("Start and End coordinates are not on the required axis")

    return point_list

def find_closest_vector(ref_vector,list_of_vectors):
        closest_vector = list_of_vectors[0]
        for vector in list_of_vectors[1:]:
            if magnitude(vector_subtract(ref_vector,vector)) < magnitude(vector_subtract(ref_vector,closest_vector)):
                closest_vector = vector
            else:
                pass
        return closest_vector
