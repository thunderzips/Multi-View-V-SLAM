import rospy
from std_msgs.msg import Float64MultiArray, Float64, Int16
import matplotlib.pyplot as plt
from math import atan,tan,pi,sin,cos
import random
import numpy as np
from scipy import linalg
import time

global posx
global posy
global posphi
global previous_P
global previous_p
global previous_l
global feature_change


global odom_file
global points_file

odom_file = open("odom.txt","w+")
# points_file = open("points.txt","w+")


previous_P = np.zeros((3,4))
previous_p = np.zeros(3)
previous_l = [0,0]
posx = 0
posy = 0
posphi = 0

global l_points

l_points = [[[0,0],0]]

feature_change = 0

i = 0

cx = 400
cy = 400

scale = 100


rospy.init_node("mapper")


def LinearTriangulation(P1,  point1,P2, point2):
 
    P = [P1,P2]
    p = [np.append(point1,1),np.append(point2,1)]

    A = []
    
    sign = [-1,1]
    
    for i in range(len(P)):
        for j in range(len(p)):
            A.append(p[i]*P[i][2,:]*sign[1-j] + P[i][1-j,:]*sign[j])

    A = np.array(A)
    A = A.reshape((4,4))

    H = A.T @ A
    
    U, S, V_T = linalg.svd(H, full_matrices = False)
 
    v = V_T[3,3]

    r = V_T[3,:3]
    
    r = r/v

    return r



def map(landmark_loc):

    global odom_file
    global points_file


    global posx
    global posy
    global posphi

    global previous_l
    global previous_P
    global previous_p

    global feature_change

    global l_points


    f = 400
    cu = 400
    cv = 400

    c = np.array([posx,posy,0])

    rz = np.array([[cos(posphi),-sin(posphi),0], [sin(posphi),cos(posphi),0], [0,0,1]])
    t = np.matmul(rz,c)

    #In homogeneous notation
    rzt = np.array([[rz[0,0],rz[0,1],rz[0,2],t[0]],[rz[1,0],rz[1,1],rz[1,2],t[1]],[rz[2,0],rz[2,1],rz[2,2],t[2]],[0,0,0,1]])
    
    #Computing the projection matrix
    k = np.array([[f,0,cu],[0,f,cv],[0,0,1]])
    F = np.array([[0,1,0,1],[0,0,-1,1],[1,0,0,1]]) ##For difference in coordinate represenation of UE4
    temp = np.matmul(F,rzt)
    P = np.matmul(k,temp)
    p = list(landmark_loc.data)
    p.append(1)
    p = np.array(p)


    l = LinearTriangulation(P,p,previous_P,previous_p)
    l = l[:2]

    l = [l[0]-posx,l[1]-posy]

    if feature_change == 0:
        w = l_points[-1][1]
        l[0] = (l[0]+w*previous_l[0])/(w+1)
        l[1] = (l[1]+w*previous_l[1])/(w+1)

        l_points = l_points[:-1]

        if abs(l[0]) <= 1000 and abs(l[1]) <= 1000:
            l_points.append([l,w+1])
    else:
        l_points[-1][1] = 0
        if abs(l[0]) <= 1000 and abs(l[1]) <= 1000:

            l_points.append([l,0])


    


    if (l[0]-previous_l[0])**2 + (l[1]-previous_l[1])**2 <= 50:#((posx-l[0])**2 + (posy-l[1])**2)*0.1:
        # print(l)
        # plt.scatter(l[0],l[1])
        odom_file.write(str(posx)+" "+str(posy)+" "+str(posphi)+" "+str(time.time())+" "+str(l[0])+" "+str(l[1])+"\n")
        # l_points.append(l)

    else:
        odom_file.write(str(posx)+" "+str(posy)+" "+str(posphi)+" "+str(time.time())+" NA"+"\n")



    previous_l = l
    previous_P = P
    previous_p = p


    # print("runnig ",random.random())

    plt.clf()

    for i in l_points:
        plt.scatter(i[0][0],i[0][1])

    # plt.scatter(posx,posy,c='g')
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

def update_feature_change(posphi_obtained):
    global feature_change
    feature_change = float(posphi_obtained.data)


image_sub = rospy.Subscriber("landmark",Float64MultiArray,map)
posx_sub = rospy.Subscriber("posx",Float64,update_posx)
posy_sub = rospy.Subscriber("posy",Float64,update_posy)
posphi_sub = rospy.Subscriber("posphi",Float64,update_posphi)
feature_change_sub = rospy.Subscriber("feature_change",Int16,update_feature_change)

rospy.spin()