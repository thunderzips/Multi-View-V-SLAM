import math
global lines
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
