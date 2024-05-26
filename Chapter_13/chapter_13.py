import math
import numpy as np 

def make_sinusoid(amplitude, frequency):
    return lambda t: amplitude * math.sin(2 * math.pi * frequency * t)

def sample(f, start, end, count):
    mapf = np.vectorize(f)
    seq = np.arange(start, end, (end - start) / count)
    values = mapf(seq)
    return values.astype(np.int16)

def const(x):
    return 1

def fourier_series(a0, a, b):
    def aux(t):
        cos_terms = [an * math.cos(2 * math.pi * (n + 1) * t) for (n, an) in enumerate(a)]
        sin_terms = [bn * math.sin(2 * math.pi * (n + 1) * t) for (n, bn) in enumerate(b)]
        result = a0 * const(t) + sum(cos_terms) + sum(sin_terms)
        return result
    return aux

def inner_product(f, g, N=1000):
    dt = 1 / N
    return 2 * sum([f(t) * g(t) * dt for t in np.arange(0, 1, dt)])

def s(n):
    return lambda t: math.sin(2 * math.pi * n * t)

def c(n):
    return lambda t: math.cos(2 * math.pi * n * t)

def const_2(n):
    return 1 / math.sqrt(2)