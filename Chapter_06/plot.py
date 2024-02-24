# plotting utility function for functions in this chapter
import numpy as np
import matplotlib.pyplot as plt

def plot(fs, xmin, xmax):
    xs = np.linspace(xmin,xmax,100)
    _, ax = plt.subplots()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    for f in fs:
        ys = [f(x) for x in xs]
        plt.plot(xs,ys)