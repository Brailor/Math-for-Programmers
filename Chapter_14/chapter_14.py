import vectors


def secant_slope(f,xmin,xmax):
    return (f(xmax) - f(xmin)) / (xmax - xmin)
def approx_derivative(f,x,dx=1e-6):
    return secant_slope(f, x-dx, x+dx)

def approx_gradient(f,x0,y0,dx=1e-6):
    partial_x = approx_derivative(lambda x: f(x,y0), x0, dx)
    partial_y = approx_derivative(lambda y: f(x0,y), y0, dx)
    return (partial_x, partial_y)


def gradient_ascent(f, x_start, y_start, tolerance=1e-6):
    x = x_start
    y = y_start
    gradient = approx_gradient(f, x, y)
    while vectors.length(gradient) > tolerance:
        x += 0.1 * gradient[0]
        y += 0.1 * gradient[1]
        gradient = approx_gradient(f, x, y)
    return x,y

def gradient_descent(f, x_start, y_start, tolerance=1e-6):
    x = x_start
    y = y_start
    gradient = approx_gradient(f, x, y)
    while vectors.length(gradient) > tolerance:
        x -= 0.01 * gradient[0]
        y -= 0.01 * gradient[1]
        gradient = approx_gradient(f, x, y)
    return x,y
def gradient_ascent_points(f, x_start, y_start, tolerance=1e-6):
    x = x_start
    y = y_start
    gradient = approx_gradient(f, x, y)
    xs,ys = [x],[y]
    while vectors.length(gradient) > tolerance:
        x += gradient[0]
        y += gradient[1]
        gradient = approx_gradient(f, x, y)

        xs.append(x)
        ys.append(y)
    return xs,ys

