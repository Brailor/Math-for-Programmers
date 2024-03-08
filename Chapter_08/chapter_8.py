import matplotlib.pyplot as plt
import numpy as np

def average_flow_rate(v, t1,t2):
    return v(t2) - v(t1) / t2 - t1

def volume(t):
    return (t-4)**3 / 64 + 3.3

def flow_rate(t):
    return 3*(t-4)**2 / 64

# Exercise 8.2: Write a Python function secant_line(f,x1,x2) that takes a function f(x) and two values,
# x1 and x2, and that returns a new function representing a secant line over time.
# For instance, if you ran line = secant_line (f,x1,x2), then line(3) would give you the y value of the secant line at x = 3.
def secant_line(f, x1, x2):
    return lambda x: f(x1) + (x - x1) * ((f(x2) - f(x1)) / (x2 - x1))

line = secant_line(lambda x: x, 3, 10)
print(line(3))

def plot_function(f,tmin,tmax,tlabel=None,xlabel=None,axes=False, **kwargs):
    ts = np.linspace(tmin,tmax,1000)
    if tlabel:
        plt.xlabel(tlabel,fontsize=18)
    if xlabel:
        plt.ylabel(xlabel,fontsize=18)
    plt.plot(ts, [f(t) for t in ts], **kwargs)
    if axes:
        total_t = tmax-tmin
        plt.plot([tmin-total_t/10,tmax+total_t/10],[0,0],c='k',linewidth=1)
        plt.xlim(tmin-total_t/10,tmax+total_t/10)
        xmin, xmax = plt.ylim()
        plt.plot([0,0],[xmin,xmax],c='k',linewidth=1)
        plt.ylim(xmin,xmax)
# Exercise 8.3: Write a function that uses the code from the previous exercise to plot a secant line of a function f between two given points.
def plot_secant(f, x1, x2, color='k'):
    line = secant_line(f, x1, x2)
    plot_function(line, x1,x2, c=color)
    plt.plot([x1,x2], [f(x1), f(x2)], c=color)

plot_secant(lambda x: x+2, 0, 10)