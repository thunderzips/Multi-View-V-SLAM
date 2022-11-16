import math
import mapper_2d

gx,gy = 10,10

m = []

x = [1,1,1,1,1,1]
y = [1,2,3,4,5,0]

for i in range(0,5):
    m.append((gy-y[i])/(gx-x[i]))


mapper_2d.init_line(1, 0, math.atan((gy-0)/(gx-1)))


for i in range(5):
    mapper_2d.mapper(x[i], y[i], math.atan(m[i]))

mapper_2d.mapper_plot(x,y)
