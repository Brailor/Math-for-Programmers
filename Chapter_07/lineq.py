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
