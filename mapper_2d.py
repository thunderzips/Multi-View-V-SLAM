from matplotlib import pyplot as plt
import numpy as np
import math

lines = []

def mapper(x, y, theta):
    m1 = lines[-1][0]  
    c1 = lines[-1][1]
    m2 = float(math.tan(theta))
    c2 = y - x*m2
    X = (c1 - c2)/(m2 - m1)
    Y = m2*X + c2
    lines.append([m2, c2])
    
    return X, Y

def init_line(x, y, theta):
    m = float(math.tan(theta))
    c = y - x*m
    lines.append([m, c])
    
def mapper_plot(x1,y1):
    x = np.linspace(-5, 15, 100)
    while(lines):
        m, c = lines.pop()
        y = m * x + c
        plt.plot(x, y)
    plt.scatter(x1,y1)
    plt.scatter(10,10,c='r')
    plt.show()
