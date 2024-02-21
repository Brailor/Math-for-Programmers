from vectors import *
from functools import *
from teapot import load_triangles
from draw_model import draw_model
from math import *
from transforms import *
from random import *
from collections.abc import Iterable
from draw3d import *
from draw2d import *

# 3x3
B = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

# 1x3
v = ((3,), (-2,), (5,))
# v = (3, -2, 5)

cols = list(zip(*B))
print(cols)
def linear_combination(scalars, *vectors):
    # assert(len(scalars) == len(vectors))

    return reduce(lambda acc,curr: add(acc, scale(curr[0], curr[1])), zip(scalars, vectors), (0,0,0))
# print(linear_combination([1, 2, 3], (1,0,0), (0,1,0), (0,0,1)))

def mul_matrix_by_vector(matrix, vector):
    return linear_combination(vector, *zip(*matrix))

# print(mul_matrix_by_vector(B, v))

def get_dimension(a):
    rows = len(a)
    assert(rows != 0)
    cols = len(a[0])
    return (rows, cols)

def check_dimensions(a,b):
    _,a_cols = get_dimension(a)
    b_rows,_= get_dimension(b)
    can_multiply = a_cols == b_rows
    assert(can_multiply)
    return can_multiply

def matrix_multiply_by_vector(matrix, vector):
    # check_dimensions(matrix, vector)
    return tuple(dot(vector, row) for row in matrix)

def matrix_multiply_by_vector_2(matrix, vector):
    # check_dimensions(matrix, vector)
    return tuple(
        sum(vector_entry * matrix_entry for vector_entry,matrix_entry in zip(row, vector))
        for row in matrix
    )
# assert(mul_matrix_by_vector(B, v) == matrix_multiply_by_vector(B, v))
# assert(matrix_multiply_by_vector_2(B, v) == matrix_multiply_by_vector(B, v))

A = (
    (1,1,0),
    (1,0,1),
    (1,-1,1)
)
B = (
    (0,2,1),
    (0,1,0),
    (1,0,-1)
)
b_cols = list(zip(*B))
print(mul_matrix_by_vector(A,b_cols[0]))
print(mul_matrix_by_vector(A,b_cols[1]))
print(mul_matrix_by_vector(A,b_cols[2]))

def matrix_multiplication(a, b):
    # check_dimensions(a, b)
    return tuple(
        tuple(dot(row, col) for col in zip(*b))
        for row in a
    )

print(matrix_multiplication(A, B))
 
def get_rotation_matrix(t):
    seconds = t/1000
    return (
        (cos(seconds),0,-sin(seconds)),
        (0,1,0),
        (sin(seconds),0,cos(seconds))
    )
# draw_model(load_triangles(), get_matrix=get_rotation_matrix)
def to_column_vector(vector):
    result = []
    for v in vector:
        result.append((v,))
    return tuple(result)

# Exercise 5.1:
# Write a function infer_matrix(n, transformation) that takes a dimension (like 2 or 3)
# and a function that is a vector transformation assumed to be linear.
# It should return an n-by-n square matrix (an n -tuple of n -tuples of numbers, which is the matrix representing the linear transformation).
# Of course, the output is only meaningful if the input transformation is linear. Otherwise, it represents an entirely different function!
def infer_matrix(n, transformation):
    def sbv(i):
        return tuple(1 if i == j else 0 for j in range(1, n + 1) )
    standard_basis_vectors = [sbv(i) for i in range(1, n + 1)]
    cols = [transformation(v) for v in standard_basis_vectors]
    return tuple(zip(*cols))

# print(f"Ex. 5.1:\n\t {infer_matrix(3, rotate_z_by(pi/2))}")

# Exercise 5.3-Mini Project:
# Write a random_matrix function that generates matrices of a specified size with random whole number entries. Use the function to generate five pairs of 3-by−3 matrices.
# Multiply each of the pairs together by hand (for practice) and then check your work with the matrix_multiply function.
def random_matrix(n):
    def random_row():
        return tuple(randint(-10,10) for _ in range(1, n + 1))
    cols = [random_row() for i in range(1, n+1)]
    return tuple(zip(*cols))

first = ((7,9,5),(4,9,-8),(2,1,2))
second = ((10,-3,-6),(4,-7,-2),(8,-4,-2))
# first_pair = [random_matrix(3) for _ in range(5)]
# second_pair = [random_matrix(3) for _ in range(5)]
# pairs = list(zip(first_pair,second_pair))
print(f"Ex. 5.3:\n\t {matrix_multiplication(first, second)}")
print(f"Ex. 5.4:\n\t {matrix_multiplication(second, first)}")
# for k, pair in enumerate(pairs):
#     print(f"#{k} pair: {pair}")

# Exercise 5.6: Apply the matrix ((2,1,1),(1,2,1),(1,1,2)) to all the vectors defining the teapot. What happens to the teapot and why?

# draw_model(load_triangles(), get_matrix=lambda t: ((2,1,1),(1,2,1),(1,1,2)))

# Exercise 5.10: Once again, let’s use the two matrices(A,B) from section 5.1.3:
# Write a function compose_a_b that executes the composition of the linear transformation for A and the linear transformation for B. 
# Then use the infer _matrix function from a previous exercise in this section to show that infer_matrix(3, compose_a_b) is the same as the matrix product AB.
A = (
    (1,1,0),
    (1,0,1),
    (1,-1,1)
)
B = (
    (0,2,1),
    (0,1,0),
    (1,0,-1)
)
def transform_matrix_by(matrix):
    return lambda v: matrix_multiply_by_vector(matrix, v)

transform_a = transform_matrix_by(A)
transform_b = transform_matrix_by(B)
compose_a_b = compose(transform_a, transform_b)

# print(f"Ex. 5.10:\n\tWith infer_matrix: {infer_matrix(3, compose_a_b)}\n\tWith matrix multiplication: {matrix_multiplication(A,B)}")

# Exercise 5.11-Mini Project: Find two, 2-by−2 matrices, neither of which is the identity matrix I2, but whose product is the identity matrix.
# The identity matrix for 2D is: 
# (
#  (1, 0)
#  (0, 1)
# )
# (2 0)    (0.5 1)
# ( )    (0)
print("Ex. 5.11: The composition of 90 and 270 degree rotation will give back the identity matrix")


# Exercise 5.12: We can multiply a square matrix by itself any number of times. We can then think of successive matrix multiplications as “raising a matrix to a power.”
# For a square matrix A, we can write AA as A2 ; we can write AAA as A3 ; and so on. Write a matrix_power(power,matrix) function that raises a matrix to the specified (whole number) power
def matrix_power(power, matrix):
    result = matrix
    for _ in range(1, power):
        result = matrix_multiplication(result, matrix)
    return result

print(f"Ex. 5.12:\n\t{matrix_power(3, A)}")

c = (((-1,-1,0),(-2,1,2),(1,0,-1)))
d = ((1,),(1,),(1,))

# print(matrix_multiplication(c, d))
# print(matrix_multiply_by_vector_2(c,(1,1,1)))

# Exercise 5.15
# three_by_two = ((1,2),(3,4),(5,6))
# four_by_five = ((1,2,3,4,5),(6,7,8,9,10),(11,12,13,14,15),(16,17,18,19,20)) 
# print(f"Ex. 5.15:\n\t {matrix_multiplication(three_by_two, four_by_five)}")

# Exercise 5.18: Write a function that turns a column vector into a row vector, or vice versa.
# Flipping a matrix on its side like this is called transposition and the resulting matrix is called the transpose of the original.
# row vector = ((1, 2, 3),) dimensions = 3x1
# column vector = ((1,), (2,), (3,)) dimensions = 1x3
def transpose(matrix):
   return tuple(zip(*matrix))

print(f"Ex. 5.18:\n\t row-vector = {transpose(((1,2,3),))}, column-vector = {transpose(((1,),(2,),(3,)))}")

# Exercise 5.22: Show by example that the infer_matrix function from a previous exercise can create matrices 
# for linear functions whose inputs and outputs have different dimensions.
def project_to_2d_by_z(v):
    projection = ((1,0,0), (0, 1, 0))
    return matrix_multiply_by_vector(projection, v)

# print(to_column_vector((1,2,3)))

print(f"Ex. 5.22: \n\t {infer_matrix(3, project_to_2d_by_z )}")
dino_vectors = [(6,4), (3,1), (1,2), (-1,5), (-2,5), (-3,4), (-4,4),
   (-5,3), (-5,2), (-2,2), (-5,1), (-4,0), (-2,1), (-1,0), (0,-3),
   (-1,-4), (1,-4), (2,-3), (1,-2), (3,-1), (5,1)
]
def polygon_segments_3d(points,color='blue'):
   count = len(points)
   return [Segment3D(points[i], points[(i+1) % count],color=color) for i in range(0,count)]

dino_3d = [(x,y,1) for x,y in dino_vectors]
rotate_and_translate = ((0,-1,3),(1,0,1),(0,0,1))
dino_3d_translated_and_rotated = [mul_matrix_by_vector(rotate_and_translate, vec) for vec in dino_3d]
# draw3d(
#    Points3D(*dino_3d, color='blue'),
#    *polygon_segments_3d(dino_3d),
#    Points3D(*dino_3d_translated_and_rotated, color='green'),
#    *polygon_segments_3d(dino_3d_translated_and_rotated, color='green'),
# )

def translate_3d(translation):
    def new_function(target):
        a,b,c = translation
        x,y,z = target
        matrix = ((1,0,0,a),(0,1,0,b),(0,0,1,c),(0,0,0,1))
        vector = (x,y,z,1)
        x_out, y_out, z_out, _ = multiply_matrix_vector(matrix,vector)
        return (x_out,y_out,z_out)
    return new_function

# draw_model(polygon_map(translate_3d((2,2,-3)), load_triangles()))

# Exercise 5.26: Show that the 3D “magic” matrix transformation does not work
# if you move a 2D figure such as the dinosaur we have been using to the plane z = 2. 
# What happens instead?
dino_3d = [(x,y,1) for x,y in dino_vectors]
# dino_3d = [(x,y,2) for x,y in dino_vectors]
rotate_and_translate = ((1,0,3),(0,1,1),(0,0,1))
dino_3d_translated_and_rotated = [mul_matrix_by_vector(rotate_and_translate, vec) for vec in dino_3d]
# draw2d(
    # Polygon2D(*dino_vectors, color='blue'),
    # Polygon2D(*[(x,y) for x,y,_ in dino_3d_translated_and_rotated], color='red')
    # )

# Exercise 5.27: Come up with a matrix to translate the dinosaur by −2 units in the x direction and −2 units in the y direction.
# Execute the transformation and show the result.
t2 = ((1,0,-2),(0,1,-2),(0,0,1))
d_t2 = [mul_matrix_by_vector(t2, vec) for vec in dino_3d]
# draw2d(
#     Polygon2D(*dino_vectors, color='blue'),
#     Polygon2D(*[(x,y) for x,y,_ in d_t2], color='red')
    # )
# Exercise 5.29−Mini Project: Find a 3×3 matrix that rotates a 2D figure in the plane z = 1 by 45°,
# decreases its size by a factor of 2, and translates it by the vector (2, 2).
# Demonstrate that it works by applying it to the vertices of the dinosaur.
# 
# how to rotate by 45? to rotate a matrix by 90 we transpose it
v = (5, 5)
v_rot = mul_matrix_by_vector(((-1,0),(0,1)),v)
r = ((1,0,0),(0,1,0),(0,0,1))
seconds = pi/4
compose_a_b
m = ((cos(seconds),-sin(seconds), 0),(sin(seconds),cos(seconds), 0), (0,0,1))
m2 = ((0.5,0,0),(0,0.5,0), (0,0,1))
m3 = ((1,0,2),(0,1,2),(0,0,1))
m_mul = matrix_multiplication(m2,m)
((a,b,_),(c,d,_),(_,_,_)) = m_mul
print(a,b,c,d)
m_mul2 = ((a,b,2), (c,d,2), (0,0,1))
d3d_t3 = [mul_matrix_by_vector(m_mul, v) for v in dino_3d]
d3d_t4 = [mul_matrix_by_vector(m_mul2, v) for v in dino_3d]
d2d_t3 = [(x,y) for x,y,_ in d3d_t3]
d2d_t4 = [(x,y) for x,y,_ in d3d_t4]
print(f"og: {d2d_t3[1]}, rotated: {rotate2d(pi/4,d2d_t3[1])}")
# print(f"length of og: {length(d2d_t3[1])}, length of rotated: {length(rotate2d(pi/4,d2d_t3[1]))}")
draw2d(
    Polygon2D(*dino_vectors, color="red"),
      Polygon2D(*d2d_t4, color="blue"),
    )