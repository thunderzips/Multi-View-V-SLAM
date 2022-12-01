import rospy
from std_msgs.msg import Float64MultiArray, Float64
import matplotlib.pyplot as plt
from math import atan,tan,pi
import random

global posx
global posy
global posphi

global prev_line
global prev_intersection

prev_intersection = [0,0]


prev_line = [0,0,0]

posx = 0
posy = 0
posphi = 0

i = 0

cx = 400
cy = 400

scale = 100


rospy.init_node("mapper")


def map(landmark_loc):
    global posx
    global posy
    global posphi
    global prev_line
    global prev_intersection

    # m =atan(1/(cx-landmark_loc.data[0]))

    # m = tan((posphi)*pi/180-m+pi/2)

    m = tan(posphi)
    # m = tan(posphi*pi/180)
    # print(m,posphi)

    # if landmark_loc.data[0] >= cx:
    #     x1 = [-posx + i for i in x[:int(scale/2)]]
    # else:
    #     x1 = [-posx + i for i in x[int(scale/2):]]
    # x = [j/100 + posx for j in range(int(-scale/2),int(scale/2))]
        
    # y = [(m*(xi-posx)) + posy for xi in x]

    c = posy - m*posx



    if abs(posphi-prev_line[2]) <= 10 :
        intersection_x = (c-prev_line[1])/(prev_line[0]-m)
        intersection_y = m*intersection_x + c

        if ((posx-intersection_x)**2 + (posy-intersection_y)**2) >= 2 and ((posx-intersection_x)**2 + (posy-intersection_y)**2) <= 100 and (prev_intersection[0]-intersection_x)**2 + (prev_intersection[1]-intersection_y)**2 <= 9:
            plt.scatter(intersection_x,intersection_y,c='r')

        else :
            plt.scatter(intersection_x,intersection_y,c='b')

        prev_intersection = [intersection_x,intersection_y]

    print("runnig ",random.random())


    prev_line = [m,c,posphi]

    # y = [(m*(xi-posx) + posy) for xi in x]

    
    # plt.plot(x,y)
    plt.scatter(posx,posy,c='g')
    plt.pause(0.000000000000000000000000000000000001)

def update_posx(posx_obtained):
    global posx
    posx = float(posx_obtained.data)

def update_posy(posy_obtained):
    global posy
    posy = float(posy_obtained.data)

def update_posphi(posphi_obtained):
    global posphi
    posphi = float(posphi_obtained.data)


image_sub = rospy.Subscriber("landmark",Float64MultiArray,map)
posx_sub = rospy.Subscriber("posx",Float64,update_posx)
posy_sub = rospy.Subscriber("posy",Float64,update_posy)
posphi_sub = rospy.Subscriber("posphi",Float64,update_posphi)

rospy.spin()