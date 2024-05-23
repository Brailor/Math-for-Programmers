import math
import vectors

B = 0.0004
C = 0.0005
v = 20
g = -9.81

def secant_slope(f, xmin, xmax):
    return (f(xmax) - f(xmin)) / (xmax - xmin)

def approx_derivative(f,x,dx=1e-6):
    return secant_slope(f, x-dx, x+dx)

def approx_gradient(f,x0,y0,dx=1e-6):
    partial_x = approx_derivative(lambda x: f(x,y0), x0, dx)
    partial_y = approx_derivative(lambda y: f(x0,y), y0, dx)
    return (partial_x, partial_y)

def landing_distance_gradient(theta,phi):
   return approx_gradient(landing_distance, theta, phi)

def gradient_ascent(f, x_start, y_start, tolerance=1e-6):
    x = x_start
    y = y_start
    gradient = approx_gradient(f, x, y)
    while vectors.length(gradient) > tolerance:
        x += gradient[0]
        y += gradient[1]
        gradient = approx_gradient(f, x, y)
    return x,y

def gradient_ascent_points(f, x_start, y_start, tolerance=1e-6):
    x = x_start
    y = y_start
    gradient = approx_gradient(f, x, y)
    xs,ys = [x],[y]
    while vectors.length(gradient) > tolerance:
        x += gradient[0]
        y += gradient[1]
        gradient = approx_gradient(f, x, y)

        xs.append(x)
        ys.append(y)
    return xs,ys


def velocity_components(speed, theta, phi):
    vx = speed * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    vy = speed * math.cos(theta * math.pi / 180) * math.sin(phi * math.pi / 180)
    vz = speed * math.sin(theta * math.pi / 180)

    return vx,vy,vz

def landing_distance(theta, phi):
    vx, vy, vz = velocity_components(v, theta, phi)
    v_xy = math.sqrt(vx ** 2 + vy ** 2)
    a = (g/2) - B * vx ** 2 + C * vy ** 2
    b = vz
    landing_time = -b/a
    landing_distance = v_xy * landing_time

    return landing_distance


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

def flat_ground(x,y):
    return 0
def trajectory_3d(theta, phi, speed=20, height=0, dt=0.01, g=-9.81, elevation=flat_ground):
    vx,vy,vz = velocity_components(speed, theta, phi)
    t,x,y,z = 0,0,0,height
    ts,xs,ys,zs = [t],[x],[y],[z]

    while z >= elevation(x,y):
        t += dt
        vz += g * dt
        x += vx * dt 
        y += vy * dt
        z += vz * dt 
        ts.append(t)
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return (ts,xs,ys,zs)


def ridge(x, y):
    return (x**2 - 5*y**2) / 2500
