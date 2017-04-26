from visual import *

scene = display(title='labyrinth')

r = 0.5
l = 12.0

ball = sphere(pos = vector(4 , 4 , r), radius = r, material = materials.rough, color = color.cyan)
board = box(pos = (0,0,-0.5), size = (l,l, 1.0), material = materials.wood, color = color.orange)
wall1 = box(pos = (l/2.0, 0, r), axis = (0, 1.0, 0), size = (l+0.5, 0.5, 3.0*r), material = materials.wood, color = color.orange)
wall2 = box(pos = (-l/2.0,0, r), axis = (0, 1.0, 0), size = (l+0.5, 0.5, 3.0*r), material = materials.wood, color = color.orange)
wall3 = box(pos = (0, l/2.0, r), axis = (1.0, 0, 0), size = (l+0.5, 0.5, 3.0*r), material = materials.wood, color = color.orange)
wall4 = box(pos = (0,-l/2.0, r), axis = (1.0, 0, 0), size = (l+0.5, 0.5, 3.0*r), material = materials.wood, color = color.orange)
wall5 = box(pos = (1, 0, r), axis = (1.0, 1.0 ,0), size = (l/2.0, 0.5, 3.0*r), material = materials.wood, color = color.orange)
cone1 = cone(pos=(5,2,0.1), axis=(0,0,-1), radius = 0.6, color = color.black)
#k=1 #magitude of velocity after collision / before collision
def wall_collide( b, w ):
    """ w is a wall (a box with a length and width)
        b is a ball (an object with a pos)
        returns True if b collides with w (in length or width)
        returns False otherwise
    """
    k = 0.8
    global velocity
    # w.pos is the center of the wall
    # b.pos is the position (center) of the ball
    perpen = rotate(w.axis, radians(90), vector(0,0,1))
    corner = [w.pos + norm(w.axis) * w.length/2.0 + norm(perpen) * w.height/2.0,
              w.pos - norm(w.axis) * w.length/2.0 + norm(perpen) * w.height/2.0, 
              w.pos + norm(w.axis) * w.length/2.0 - norm(perpen) * w.height/2.0, 
              w.pos - norm(w.axis) * w.length/2.0 - norm(perpen) * w.height/2.0]
    for i in xrange(len(corner)):
        corner[i].z = r
    length_vector = proj(vector(b.pos.x, b.pos.y, r) - vector(w.pos.x, w.pos.y, r), w.axis)
    width_vector = proj(vector(b.pos.x, b.pos.y, r) - vector(w.pos.x, w.pos.y, r), perpen)
    lega = mag(length_vector)                              
    legb = mag(width_vector)            
    if legb <= w.height/2.0 + r  and lega <= w.length/2.0: # w.height is along y axis, which is actually the width here
        collide_point = vector(w.pos.x, w.pos.y, r) + length_vector + w.height/2 * norm(b.pos - vector(w.pos.x, w.pos.y, r) - length_vector)
        velocity_parall = proj(velocity, w.axis)
        velocity_perpen = proj(velocity, perpen)
        #after collision
        velocity = velocity_parall - velocity_perpen * k
        ball.pos = collide_point + r * norm(ball.pos - collide_point)
    elif lega <= w.length/2.0 + r and legb <= w.height/2.0:
        collide_point = vector(w.pos.x, w.pos.y, r) + width_vector + w.length/2 * norm(b.pos - vector(w.pos.x, w.pos.y, r) - width_vector)
        velocity_parall = proj(velocity, perpen)
        velocity_perpen = proj(velocity, w.axis)
        #after collision
        velocity = velocity_parall - velocity_perpen * k
        ball.pos = collide_point + r * norm(ball.pos - collide_point)
    else:
        for i in xrange(4):
            if mag(ball.pos - corner[i]) <= r:
                perpen = ball.pos - corner[i]
                parall = rotate(perpen, radians(90), vector(0, 0, 1))
                velocity_parall = proj(velocity, parall)
                velocity_perpen = proj(velocity, perpen)
                # after collision
                velocity = velocity_parall - velocity_perpen * k
                ball.pos = corner[i] + r * norm(ball.pos - corner[i])


g = vector(0, 0, -9.8)
RATE = 60
dt = 1.0/(1.0*RATE)
alpha = 0
beta = 0
velocity = vector(0, 0, 0)
friction_coefficient = 0.03

while True:
    rate(RATE)
    # keyboard events
    if scene.kb.keys:
        k = scene.kb.getkey() # get keyboard info
        u = vector(0, 1, 0)   # the up vector
        f = vector(0, 0, -1)  # the forward vector
        v = norm(cross(u, f))  # v == norm of (up cross forward)

        if k in ['left', 'right', 'up', 'down']:
            twodeg = radians(2)
            if k == 'up' and alpha < 10:
                scene.forward = rotate(scene.forward, -twodeg, v)
                alpha += 2
                g = rotate(g, -twodeg, v)
            if k == 'down' and alpha > -10:
                scene.forward = rotate(scene.forward, twodeg, v)
                alpha -= 2
                g = rotate(g, twodeg, v)
            if k == 'left' and beta < 10:
                scene.forward = rotate(scene.forward, twodeg, u)
                beta += 2
                g = rotate(g, twodeg, u)
            if k == 'right' and beta > -10:
                scene.forward = rotate(scene.forward, -twodeg, u)
                beta -= 2
                g = rotate(g, -twodeg, u)
    if abs(velocity) > 0:
        friction = -norm(velocity) * abs(g.z) * friction_coefficient
    else:
        if abs(vector(g.x, g.y, 0)) <= abs(g.z) * friction_coefficient:
            friction = -vector(g.x, g.y, 0)
        else:
            friction = -norm(vector(g.x, g.y, 0)) * abs(g.z) * friction_coefficient

    g_component = vector(g.x, g.y, 0)
    accel = g_component + friction
    velocity += accel*dt
    ball.pos += velocity * dt

    walls = [wall1, wall2, wall3, wall4, wall5]
    for wall in walls:
        wall_collide(ball, wall)










        
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

