from random import uniform
from math import isclose
from datetime import *
from chapter_6 import *

def random_scalar():
   return uniform(-10,10)


def random_float_vec2():
   return (random_scalar(), random_scalar())

def random_float_vec3():
   return (random_scalar(), random_scalar(), random_scalar())
   
def random_vec2():
   return Vec2(random_scalar(),random_scalar())

def random_vec3():
   return Vec3(random_scalar(),random_scalar(), random_scalar())

def random_car_for_sale():
    def random_datetime():
       return datetime(int(uniform(2005, 2024)), int(uniform(1,12)), int(uniform(1,28)), int(uniform(1,23)))
    year = random_datetime()
    post_date = random_datetime()
    return CarForSale(year.year, uniform(1000, 1000 * 160), uniform(5000, 65000), post_date)

def approx_equal_v2(v1:Vec2,v2:Vec2):
   return isclose(v1.x, v2.x) and isclose(v1.y, v2.y)
def approx_equal_v3(v1:Vec3,v2:Vec3):
   return isclose(v1.x, v2.x) and isclose(v1.y, v2.y) and isclose(v1.z, v2.z)

def test(zero,eq,a,b,u,v,w):
    assert eq(u + v, v + u)
    assert eq(u + (v + w), (u + v) + w)
    assert eq(a * (b * v), (a * b) * v)
    assert eq(1 * v, v)
    assert eq((a + b) * v, a * v + b * v)
    assert eq(a * v + a * w, a * (v + w))
    assert eq(zero + v, v)
    assert eq(v * 0, zero)
    assert eq(-v + v, zero)

for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w  = random_vec2(), random_vec2(), random_vec2()
    test(Vec2.zero(), approx_equal_v2,a,b,u,v,w)

# Exercise 6.4: Write unit tests to show that the addition and scalar multiplication operations for Vec3 satisfy the vector space properties.
for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w  = random_vec3(), random_vec3(), random_vec3()
    test(Vec3.zero(), approx_equal_v3,a,b,u,v,w)

# Exercise 6.5: Add unit tests to check that 0 + v = v, 0 · v = 0, and -v + v = 0 for any vector v,
# where again 0 is the number zero and 0 is the zero vector.

# Exercise 6.8: Run the vector space unit tests with float values for u, v, and w, rather than with objects inheriting from the Vector class.
# This demonstrates that real numbers are indeed vectors.
for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w  = random_float_vec3()
    test(0, isclose ,a,b,u,v,w)

for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w = random_float_vec3()
    test(0, isclose, a,b,u,v,w)

# Exercise 6.9−Mini Project: Run the vector space unit tests for CarForSale to show its objects form a vector space (ignoring their textual attributes).

def car_same(c1: CarForSale,c2:CarForSale):
    return c1 == c2
for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w = random_car_for_sale(), random_car_for_sale(), random_car_for_sale()
    test(CarForSale.zero(), car_same, a,b,u,v,w)

# Exercise 6.11-Mini Project: Testing equality of functions is difficult. Do your best to write a function to test whether two functions are equal.
f = Function(lambda x: x)
g = Function(lambda x: x)

def random_function():
    r = int(uniform(-10, 10))
    return Function(lambda x: x + r )

def functions_same_approx(f,g):
    results = []
    for _ in range(0, 10):
        i = uniform(-10, 10)
        results.append(isclose(f(i), g(i)))
    return all(results)

for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w = random_function(), random_function(), random_function()
    test(Function.zero(), functions_same_approx, a,b,u,v,w)


# Exercise 6.16: Unit test the Matrix5_by_3 class to demonstrate that it obeys the defining properties of a vector space.
def random_5_by_3_matrix():
    return Matrix_5_x_3(random_matrix(5,3))

def random_matrix(rows,cols):
    return tuple(
            tuple(uniform(-10, 10) for _ in range(0, cols))
            for _ in range(0, rows)
    )
    

def approx_equal_matrix_5_by_3(m1,m2):
   return all([
       isclose(m1.matrix[i][j],m2.matrix[i][j]) 
       for j in range(0,3)
       for i in range(0,5)
   ])
   
for _ in range(100):
    a,b = random_scalar(),random_scalar()
    u, v, w = random_5_by_3_matrix(), random_5_by_3_matrix(), random_5_by_3_matrix() 
    test(Matrix_5_x_3.zero(),approx_equal_matrix_5_by_3, a,b,u,v,w)