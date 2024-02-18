from vectors import *
from teapot import load_triangles
from draw_model import *
from random import *
from itertools import *
from functools import *

def scale2(v):
    return scale(2.0, v)

original_triangles = load_triangles()
scaled_triangles = [
    [scale2(vertex) for vertex in triangle]
    for triangle in original_triangles
]
print(f"Original first triangle: {original_triangles[0]}\nScaled first triangle: {scaled_triangles[0]}")

# draw_model(scaled_triangles)

def translate_to_left(v):
    return add((-1,0,0), v)

scaled_triangles = [
    [translate_to_left(vertex) for vertex in triangle]
    for triangle in original_triangles
]
# draw_model(scaled_triangles)

def compose(f1, f2):
    return lambda i: f1(f2(i))

# TODO: add n function support for compose, so compose(fn1, fn2, fn3, ...fnN) -> fnN(...fn3(..))

scale2_then_translate = compose(scale2, translate_to_left)

scaled_triangles = [
    [scale2_then_translate(vertex) for vertex in triangle]
    for triangle in original_triangles
]

# draw_model(scaled_triangles)
def polygon_map(transformation, polygons):
    return [
        [transformation(vertex) for vertex in polygon]
        for polygon in polygons
    ] 

def scale_by(scalar):
    return lambda v: scale(scalar, v)

def translate_by(translation_vector):
    return lambda v: add(translation_vector, v)


def rotate_2d(rotation_angle, vector):
    length,angle = to_polar(vector)
    return to_cartesian((length, angle + rotation_angle))

def rotate_z_by(rotation_angle):
    def rotate(vector):
        x,y,z = vector
        new_x,new_y = rotate_2d(rotation_angle, (x,y))
        return (new_x, new_y, z)

    return rotate 

def rotate_x_by(rotation_angle):
    def rotate(vector):
        x,y,z = vector
        new_y,new_z= rotate_2d(rotation_angle, (y, z))
        return (x, new_y, new_z)

    return rotate 

def rotate_y_by(rotation_angle):
    def rotate(vector):
        x,y,z = vector
        new_x,new_z= rotate_2d(rotation_angle, (x, z))
        return (new_x, y, new_z)

    return rotate 

# draw_model(polygon_map(compose(scale_by(0.7), rotate_z_by(pi / 4.)), original_triangles))
# draw_model(polygon_map(rotate_x_by(pi / 4.), original_triangles))
# draw_model(polygon_map(translate_by((0,0,-20)), original_triangles))

# Exercise 4.3-Mini Project: What happens to the teapot when you scale every vector by a scalar between 0 and 1? What happens when you scale it by a factor of −1?
# A: between 0-1 -> if 1 then nothing changes, otherwise the teapot gets smaller as we approach to 0, reaching 0 the teapot will be gone
# A: factor of -1 -> the teapot will be flipped, and the transformation will still occur
# draw_model(polygon_map(scale_by(-2), original_triangles))

# Exercise 4.4: First apply translate1left to the teapot and then apply scale2. How is the result different from the opposite order of composition? Why?
# draw_model()
a = list(chain.from_iterable([
        polygon_map(compose(scale_by(2), translate_by((1,0,0))), original_triangles),
        polygon_map(compose(translate_by((1,0,0)), scale_by(2)), original_triangles)
    ]
))
# draw_model(
#     a,
#     display=(1024, 1024)
# )

# Exercise 4.6: Modify the compose(f,g) function to compose(*args), which takes several functions as arguments and returns a new function that is their composition.
def compose_any(*args):
    def fn(arg):
        args_list = list(args)
        args_list.reverse()
        return reduce(lambda res,fn: fn(res), args_list, arg)

    return fn

trans = compose_any(translate_by((1,0,0)), translate_by((0,1,0)), translate_by((0,0,1)))
print(trans((0,0,0)))
def prepend(string):
   def new_function(input):
       return string + input
   return new_function

f = compose_any(prepend("P"), prepend("y"), prepend("t"))
print(f("hon"))


def add_nums(x, y):
    return x + y
# Exercise 4.7: Write a curry2(f) function that takes a Python function f(x,y) with two arguments and returns a curried version.
# For instance, once you write g = curry2(f), the two expressions f(x,y) and g(x)(y) should return the same result.
def curry2(f):
    def fn1(x):
        def fn2(y):
            return f(x,y)
        return fn2
    return fn1
g = curry2(add_nums)
print(f"Ex. 4.7: \n\tcurried version = {g(5)(10)}\n\tnormal version = {add_nums(5, 10)}")

# Exercise 4.9: Write a function stretch_x(scalar,vector) that scales the target vector by the given factor but only in the x direction. 
# Also write a curried version stretch_x_by so that stretch_x_by(scalar)(vector) returns the same result.
def stretch_x(scalar, vector):
    x,y,z = vector
    return (x * scalar, y, z)

def stretch_x_by(scalar):
    def stretch(vector):
        return stretch_x(scalar, vector)
    return stretch

print(f"Ex. 4.9: \n\toriginal version = {stretch_x(2, (2, 1, 3))}\n\tcurried version = {stretch_x_by(2)((2,1,3))}")

u = (4,9)
v = (1,1)
# draw2d.draw2d()
def S(vec):
    x,y = vec
    return (x * x, y * y)

# T(sv) = sT(v)
print(f"S(u) = {S(u)}, S(v) = {S(v)}\nS(u + v) = {S(add(u, v))}, S(u) + S(v) = {add(S(u), S(v))}")
print(f"S(su) = {S(scale(0.5, u))}, sS(v) = {scale(0.5, S(u))}")
