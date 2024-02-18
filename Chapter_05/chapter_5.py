from vectors import *
from functools import *
from teapot import load_triangles
from draw_model import draw_model
from math import *
from transforms import *
from random import *

B = (
    (0, 2, 1),
    (0, 1, 0),
    (1, 0, -1)
)

v = (3, -2, 5)

cols = list(zip(*B))
print(cols)
def linear_combination(scalars, *vectors):
    assert(len(scalars) == len(vectors))

    return reduce(lambda acc,curr: add(acc, scale(curr[0], curr[1])), zip(scalars, vectors), (0,0,0))
# print(linear_combination([1, 2, 3], (1,0,0), (0,1,0), (0,0,1)))

def mul_matrix_by_vector(matrix, vector):
    return linear_combination(vector, *zip(*matrix))

# print(mul_matrix_by_vector(B, v))

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
    return [
        tuple(dot(row, col) for col in zip(*b))
        for row in a
    ]
print(matrix_multiplication(A, B))
 
def get_rotation_matrix(t):
    seconds = t/1000
    return (
        (cos(seconds),0,-sin(seconds)),
        (0,1,0),
        (sin(seconds),0,cos(seconds))
    )
# draw_model(load_triangles(), get_matrix=get_rotation_matrix)

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

print(f"Ex. 5.1:\n\t {infer_matrix(3, rotate_z_by(pi/2))}")

# Exercise 5.3-Mini Project:
# Write a random_matrix function that generates matrices of a specified size with random whole number entries. Use the function to generate five pairs of 3-by−3 matrices.
# Multiply each of the pairs together by hand (for practice) and then check your work with the matrix_multiply function.
def random_matrix(n):
    def random_row():
        return tuple(randint(-10,10) for j in range(1, n + 1))
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
    return lambda v: mul_matrix_by_vector(matrix, v)

transform_a = transform_matrix_by(A)
transform_b = transform_matrix_by(B)
compose_a_b = compose(transform_a, transform_b)

print(f"Ex. 5.10:\n\tWith infer_matrix: {infer_matrix(3, compose_a_b)}\n\tWith matrix multiplication: {matrix_multiplication(A,B)}")

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