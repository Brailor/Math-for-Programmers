import math

def trajectory(theta, speed=20, height=0, dt=0.01, g=-9.81):
    vx = speed * math.cos(theta * math.pi / 180)
    vz = speed * math.sin(theta * math.pi / 180)

    t,x,z = 0,0,height
    ts,xs,zs = [t], [x], [z]

    while z >= 0:
        t += dt
        vz += g * dt
        z += vz * dt
        x += vx * dt
        ts.append(t)
        xs.append(x)
        zs.append(z)
    return (ts,xs,zs)

def landing_position(trajectory_data):
    return trajectory_data[1][-1]

def heighest_point(trajectory_data):
    return max(trajectory_data[2])

def hang_time(trajectory_data):
    return trajectory_data[0][-1]