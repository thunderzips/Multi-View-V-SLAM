import rospy
from std_msgs.msg import Float64MultiArray, Float64
import matplotlib.pyplot as plt

global posx
global posy

posx = 0
posy = 0

i = 0

cx = 640
cy = 360

scale = 100000

x = [j/100 for j in range(int(-scale/2),int(scale/2))]

rospy.init_node("mapper")

def map(landmark_loc):
    global posx
    global posy

    m = 1/(cx-landmark_loc.data[0])

    if landmark_loc.data[0] >= cx:
        x1 = x[:int(scale/2)]
    else:
        x1 = x[int(scale/2):]
        
    y = [(m*xi + posy) for xi in x1]

    plt.plot(x1,y)
    plt.pause(0.000000000000000000000000000000000001)

def update_posx(posx_obtained):
    global posx
    posx = posx_obtained

def update_posy(posy_obtained):
    global posy
    posy = posy_obtained


image_sub = rospy.Subscriber("keypoints",Float64MultiArray,map)
posx_sub = rospy.Subscriber("posx",Float64,update_posx)
posy_sub = rospy.Subscriber("posy",Float64,update_posy)

rospy.spin()