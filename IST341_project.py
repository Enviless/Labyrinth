from visual import *
import math

scene = display(title='labyrinth', x=100, y=0, width=800, height=800)

r = 0.5  # centimeter
l = 30   

ball = sphere(pos = vector(l/2.0-r-0.5 , 10 , r), radius = r, material = materials.rough, color = color.cyan)

class Hole:
    def __init__(self, pos, r):
        self.pos = vector(pos[0], pos[1], 0)
        self.r = r
        self.graph = shapes.circle(pos=pos, radius=r)

hole1 = Hole((10.0,-10.0),0.8)
hole2 = Hole((-10,10), 0.8)
holes = [hole1, hole2]

rt = shapes.rectangle(pos=(0,0), width=l, height=l)
straight = [(0,0,0),(0,0,-0.5)]
sp = rt
for hole in holes:
    sp -= hole.graph
board = extrusion(pos=straight, shape=sp, material = materials.wood, color = color.orange)

wall1 = box(pos = (l/2.0, 0, 1.5*r), axis = (0, 1.0, 0), size = (l+1, 1, 3.0*r), material = materials.wood, color = color.orange)
wall2 = box(pos = (-l/2.0,0, 1.5*r), axis = (0, 1.0, 0), size = (l+1, 1, 3.0*r), material = materials.wood, color = color.orange)
wall3 = box(pos = (0, l/2.0, 1.5*r), axis = (1.0, 0, 0), size = (l+1, 1, 3.0*r), material = materials.wood, color = color.orange)
wall4 = box(pos = (0,-l/2.0, 1.5*r), axis = (1.0, 0, 0), size = (l+1, 1, 3.0*r), material = materials.wood, color = color.orange)
wall5 = box(pos = (1, 0, 1.5*r), axis = (1.0, 1.0 ,0), size = (l/2.0, 1, 3.0*r), material = materials.wood, color = color.orange)
walls = [wall1, wall2, wall3, wall4, wall5]


def wall_collide( b, w ):
    """ w is a wall (a box with a length and width)
        b is a ball (an object with a pos)
        returns True if b collides with w (in length or width)
        returns False otherwise
    """
    k = 0.7 #k=1 #magitude of velocity after collision / before collision
    global velocity
    # w.pos is the center of the wall
    # b.pos is the position (center) of the ball
    perpen = rotate(w.axis, radians(90), vector(0,0,1))
    corner = [w.pos + norm(w.axis) * w.length/2.0 + norm(perpen) * w.height/2.0,
              w.pos - norm(w.axis) * w.length/2.0 + norm(perpen) * w.height/2.0, 
              w.pos + norm(w.axis) * w.length/2.0 - norm(perpen) * w.height/2.0, 
              w.pos - norm(w.axis) * w.length/2.0 - norm(perpen) * w.height/2.0]
    for i in xrange(len(corner)):
        corner[i].z = b.pos.z
    length_vector = proj(b.pos - vector(w.pos.x, w.pos.y, b.pos.z), w.axis)
    width_vector = proj(b.pos - vector(w.pos.x, w.pos.y, b.pos.z), perpen)
    lega = mag(length_vector)                              
    legb = mag(width_vector)            
    if legb <= w.height/2.0 + b.radius  and lega <= w.length/2.0: # w.height is along y axis, which is actually the width here
        collide_point = vector(w.pos.x, w.pos.y, b.pos.z) + length_vector + w.height/2 * norm(b.pos - vector(w.pos.x, w.pos.y, b.pos.z) - length_vector)
        velocity_parall = proj(velocity, w.axis)
        velocity_perpen = proj(velocity, perpen)
        #after collision
        velocity = velocity_parall - velocity_perpen * k
        b.pos = collide_point + b.radius * norm(b.pos - collide_point)
    elif lega <= w.length/2.0 + b.radius and legb <= w.height/2.0:
        collide_point = vector(w.pos.x, w.pos.y, b.pos.z) + width_vector + w.length/2 * norm(b.pos - vector(w.pos.x, w.pos.y, b.pos.z) - width_vector)
        velocity_parall = proj(velocity, perpen)
        velocity_perpen = proj(velocity, w.axis)
        #after collision
        velocity = velocity_parall - velocity_perpen * k
        b.pos = collide_point + b.radius * norm(b.pos - collide_point)
    else:
        for i in xrange(4):
            if mag(b.pos - corner[i]) <= r:
                perpen = b.pos - corner[i]
                parall = rotate(perpen, radians(90), vector(0, 0, 1))
                velocity_parall = proj(velocity, parall)
                velocity_perpen = proj(velocity, perpen)
                # after collision
                velocity = velocity_parall - velocity_perpen * k
                b.pos = corner[i] + b.radius * norm(b.pos - corner[i])

def hole_edge_colide(b, h):
    k = 0.7
    global velocity
    proj_hole_to_ball_x_y = vector(b.pos.x, b.pos.y ,0) - h.pos
    colide_point = h.pos + h.r * norm(proj_hole_to_ball_x_y)
    colide_point_to_ball_center = b.pos - colide_point
    hole_tangent = rotate(proj_hole_to_ball_x_y, radians(90), vector(0, 0, 1))
    u = - norm(cross(colide_point_to_ball_center, hole_tangent))
    v_xx = proj(velocity, u)
    v_yy = proj(velocity, hole_tangent)
    v_zz = proj(velocity, colide_point_to_ball_center)
    if mag(proj_hole_to_ball_x_y) <= h.r:
        if mag(colide_point - b.pos) <= b.radius:
            v_zz = - v_zz
            velocity = v_xx + v_yy + v_zz
            b.pos = colide_point + b.radius * norm(colide_point_to_ball_center)
        else:
            pass
            




g = vector(0, 0, -20)
RATE = 200
dt = 1.0/(1.0*RATE)
alpha = 0
beta = 0
velocity = vector(0, 0, 0)
friction_coefficient = 0.003

while ball.pos.z >= (-5) * ball.radius:
    rate(RATE)
    # keyboard events
    if scene.kb.keys:
        k = scene.kb.getkey() # get keyboard info
        u = vector(0, 1, 0)   # the up vector
        f = vector(0, 0, -1)  # the forward vector
        v = norm(cross(u, f))  # v == norm of (up cross forward)

        if k in ['left', 'right', 'up', 'down']:
            deg = radians(2)
            if k == 'up' and alpha < 10:
                scene.forward = rotate(scene.forward, -deg, v)
                alpha += 2
                g = rotate(g, -deg, v)
            if k == 'down' and alpha > -10:
                scene.forward = rotate(scene.forward, deg, v)
                alpha -= 2
                g = rotate(g, deg, v)
            if k == 'left' and beta < 10:
                scene.forward = rotate(scene.forward, deg, u)
                beta += 2
                g = rotate(g, deg, u)
            if k == 'right' and beta > -10:
                scene.forward = rotate(scene.forward, -deg, u)
                beta -= 2
                g = rotate(g, -deg, u)
    if mag(velocity) > 0:
        friction = -norm(velocity) * abs(g.z) * friction_coefficient
    else:
        if abs(vector(g.x, g.y, 0)) <= abs(g.z) * friction_coefficient:
            friction = -vector(g.x, g.y, 0)
        else:
            friction = -norm(vector(g.x, g.y, 0)) * abs(g.z) * friction_coefficient

    for hole in holes:
        proj_hole_to_ball_x_y = vector(ball.pos.x, ball.pos.y ,0) - hole.pos
        if mag(proj_hole_to_ball_x_y) <= hole.r:
            accel = g
            break
    else:
        g_component = vector(g.x, g.y, 0)
        accel = g_component + friction
    velocity += accel*dt
    ball.pos += velocity * dt
    if ball.pos.z > ball.radius:
        ball.pos.z = ball.radius

    for wall in walls:
        wall_collide(ball, wall)
    for hole in holes:
        hole_edge_colide(ball, hole)










        
# while(True):
    
#     rate(RATE)

#     # keyboard events
#     if scene.kb.keys: # event waiting to be processed?
#         k = scene.kb.getkey() # get keyboard info

#         u = scene.up      # the up vector
#         f = scene.forward # the forward vector
#         v = norm(cross( u, f ))  # v == norm of (up cross forward)

#         if k in '+=_-':    # zoom in and out
#             if k in '+=':  scene.range += vector(1,1,1)   # zoom in
#             if k in '-_':  scene.range -= vector(1,1,1)   # zoom out

#         if k in 'aswd':    # move the center
#             if k == 'a':  scene.center += v   # 1 unit in the direction of v
#             if k == 'd':  scene.center -= v   # 1 unit vs the direction of v
#             if k == 'w':  scene.center += u   # 1 unit in the direction of u (up)
#             if k == 's':  scene.center -= u   # 1 unit vs the direction of u (up)

#         if k in ['left','right','up','down']:  # rotate u and f around the celestial sphere
#             fivedeg = radians(5)  # fivedeg is 5 degrees in radians
#             if k == 'up':  
#                 scene.up = rotate( u, fivedeg, v )  # 1 fivedeg unit "further up"
#                 scene.forward = rotate( f, fivedeg, v )  # 1 fivedeg unit "further up"
#             if k == 'down':  
#                 scene.up = rotate( u, -fivedeg, v )  # 1 fivedeg unit "back down"
#                 scene.forward = rotate( f, -fivedeg, v )  # 1 fivedeg unit "further up"
#             if k == 'left':  scene.forward = rotate( f, -fivedeg, u )  # 1 fivedeg unit "to the left"
#             if k == 'right':  scene.forward = rotate( f, fivedeg, u )  # 1 fivedeg unit "to the right"

