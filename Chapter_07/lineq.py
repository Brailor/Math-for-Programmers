import numpy as np
import vectors

def intersection(u1,u2,v1,v2):
    a1,b1,c1 = standard_form(u1,u2)
    a2,b2,c2 = standard_form(v1,v2)
    m = np.array(((a1,b1), (a2,b2)))
    c = np.array((c1,c2))
    return np.linalg.solve(m, c)

def do_segments_intersect(s1,s2):
    u1,u2 = s1
    v1,v2 = s2 
    d1,d2 = vectors.distance(*s1),vectors.distance(*s2)
    try:
        x,y = intersection(u1,u2,v1,v2)

        return (
            vectors.distance(u1, (x,y)) <= d1 and
            vectors.distance(u2, (x,y)) <= d1 and
            vectors.distance(v1, (x,y)) <= d2 and
            vectors.distance(v2, (x,y)) <= d2
        )
    except np.linalg.linalg.LinAlgError:
        return False

# Exercise 7.11: Write a Python function standard_form that takes two vectors v1 and v2 and finds the line ax + by = c passing through both of them.
# Specifically, it should output the tuple of constants (a, b, c).
def standard_form(v1,v2):
    x1,y1 = v1
    x2,y2 = v2 
    a = (y2 - y1)
    b = (x1 - x2)
    c = (y2 * x1) - (x2 * y1) 
    return (a,b,c)

# Exercise 7.12-Mini Project: For each of the four distance checks in do _segments_intersect,
# find a pair of line segments that fail one of the checks but pass the other three checks.
def segment_check(s1,s2):
    u1,u2 = s1
    v1,v2 = s2 
    d1,d2 = vectors.distance(*s1),vectors.distance(*s2)
    x,y = intersection(u1,u2,v1,v2)
    return [
        vectors.distance(u1, (x,y)) <= d1,
        vectors.distance(u2, (x,y)) <= d1,
        vectors.distance(v1, (x,y)) <= d2,
        vectors.distance(v2, (x,y)) <= d2
    ]

# Exercise 7.19−Mini Project: Write a Python function that takes three 3D points as inputs 
# and returns the standard form equation of the plane that they lie in.
# For instance, if the standard form equation is ax + by + cz = d, the function could return the tuple (a, b, c, d).
# Hint: Differences of any pairs of the three vectors are parallel to the plane, so cross products of the differences are perpendicular.
def standard_form_3d(v1,v2,v3):
    diff1 = vectors.subtract(v3, v1)
    diff2 = vectors.subtract(v2, v1)
    a,b,c = vectors.cross(diff1, diff2)
    d = vectors.dot(v1, (a, b, c))
    return (a,b,c,d)


# Exercise 7.27: How can you write the vector (5, 5) as a linear combination of (10, 1) (3, 2)?
M1 = np.array(
    (
    (10, 1),
    (3, 2)
    )
)
D1 = np.array((5,5))
res = np.linalg.solve(M1, D1)
print(f"Ex. 7.27:\n\t {res}")
# Exercise 7.28: Write the vector (3, 0, 6, 9) as a linear combination of the vectors (0, 0, 1, 1), (0, −2, −1, −1), (1, −2, 0, 2), and (0, 0, −2, 1).
M2 = np.array((
    (0, 0,1,0),
    (0,-2,-2,0),
    (1,-1,0,-2),
    (1,-1,2,1)
))
D2 = np.array((3,0,6,9))
res = np.linalg.solve(M2, D2)

print(f"Ex. 7.28:\n\t {res}")