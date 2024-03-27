import vectors
import math
from draw2d import *
t = 0
s = (0,0)
v = (1,0)
a = (0,0.2)

rounds = 100
dt = 1

positions = [s]
# for _ in range(rounds):
#     t += dt
#     s = vectors.add(s, vectors.scale(dt, v))
#     v = vectors.add(v, vectors.scale(dt, a))
    # positions.append(s)

# draw2d(Points2D(*positions))

# Exercise 9.2-Mini Project: Create a function that carries out Euler’s method automatically for a constantly accelerating object.
# You need to provide the function with an acceleration vector, initial velocity vector, initial position vector, and perhaps other parameters.
def euler(acc_vector, init_v_vector, init_pos_vector, steps, total_time):
    s = init_pos_vector
    v = init_v_vector
    positions = [s]
    dt = total_time / steps
    for _ in range(steps):
        s = vectors.add(s, vectors.scale(dt, v))
        v = vectors.add(v, vectors.scale(dt, acc_vector))
        positions.append(s)
    return positions

steps = 25
total_time = 10
new_pos = euler(a, v, s, steps, total_time)
print(f"Ex. 9.2:\n\t Original positions: {positions}, new positions: {new_pos}")

# Exercise 9.3-Mini Project: In the calculation of section 9.4, we under approximated the y-coordinate of position because we
# updated the y component of the velocity at the end of each time interval.
# Update the velocity at the beginning of each time interval and show that you over approximate the y position over time.
def euler_2(acc_vector, init_v_vector, init_pos_vector, steps, total_time):
    s = init_pos_vector
    v = init_v_vector
    positions = [s]
    dt = total_time / steps
    for _ in range(steps):
        v = vectors.add(v, vectors.scale(dt, acc_vector))
        s = vectors.add(s, vectors.scale(dt, v))
        positions.append(s)
    return positions
new_pos_2 = euler_2(a, v, s, steps, total_time)

# draw2d(
#     Points2D(*new_pos, color="red"),
#     Points2D(*new_pos_2, color="green"),
# )

# Exercise 9.4−Mini Project: Any projectile like a thrown baseball, a bullet, or an airborne snowboarder experiences
# the same acceleration vector: 9.81 m/s/s toward the earth.
# If we think of the x-axis of the plane as flat ground with the positive y-axis pointing upward,
# that amounts to an acceleration vector of (0, 9.81). 
# If a baseball is thrown from shoulder height at x = 0, we could say its initial position is (0, 1.5).
# Assume it’s thrown at an initial speed of 30 m/s at an angle of 20° up from the positive x direction and simulate its trajectory with Euler’s method.
# Approximately how far does the baseball go in the x direction before hitting the ground?
angle = 20 * (math.pi / 180)
v0 = ((30 * math.sin(angle)), (30 * math.cos(angle)))
print(v0)
path = euler((0, -9.81), v0, (0, 1.5), 25, 10)
# print(path)
draw2d(Points2D(*path, color="green"))