import cv2
import numpy as np
import math
import random
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray, Int16, Float64


Kp = 0.05


rospy.init_node("feature_points_extractor")

image_pub = rospy.Publisher("image_with_features",Image,queue_size=1)
dir_pub = rospy.Publisher("servo_direction",Float64,queue_size=10)
keypoints_pub = rospy.Publisher("keypoints",Float64MultiArray,queue_size=10)
landmark_pub = rospy.Publisher("landmark",Float64MultiArray,queue_size=10)


bridge = CvBridge()

global orb
orb = cv2.ORB_create()

global init
init = "no"

global landmark
global p_landmark

p_landmark = [0,0]
landmark = random.randint(0,20)

def get_distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def get_features(original_image):

    rate = rospy.Rate(10)


    original_image = bridge.imgmsg_to_cv2(original_image, "bgr8")

    print("runnig ",random.random())


    rl_val = {True:1,False:-1}
    center = [np.shape(original_image)[1]/2,np.shape(original_image)[0]/2]
    # print("center = ",center)
    # center = 400,400
    global init
    global landmark
    global p_landmark

    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    original_keypoints, original_descriptor = orb.detectAndCompute(gray_image, None)
    keypoints_without_size = np.copy(original_image)

    op=cv2.drawKeypoints(original_image, original_keypoints, keypoints_without_size, color = (0, 255, 0))
    key_points_loc = []

    for i in original_keypoints:
        key_points_loc.append(i.pt)

    key_points_loc_ros = Float64MultiArray()
    key_points_loc_ros.data = key_points_loc


    try:
        if not init == 'done':
            p_landmark = key_points_loc[landmark]
            init = 'done'

        dists = []

        for i in range(len(key_points_loc)):
            dists.append(get_distance(key_points_loc[i],p_landmark))

        m = min(dists)
        landmark = dists.index(m)
        p_landmark = list(key_points_loc[landmark])

        cv2.circle(op, (int(key_points_loc[landmark][0]),int(key_points_loc[landmark][1])), 10, color= (0,0,255), thickness=6, lineType=8, shift=0)
    except:
        pass

    # return op, rl_val[list(np.array(p_landmark)-np.array(center))[0] > 0]

    cv2.imshow("final",op)
    cv2.waitKey(1)

    landmark_loc_ros = Float64MultiArray()
    landmark_loc_ros.data = key_points_loc[landmark]

    image_pub.publish(bridge.cv2_to_imgmsg(op, "bgr8"))
    # keypoints_pub.publish(key_points_loc_ros)
    
    dir_pub.publish(Kp*list(np.array(p_landmark)-np.array(center))[0])
    landmark_pub.publish(landmark_loc_ros)


image_sub = rospy.Subscriber("camera_feed",Image,get_features)

rospy.spin()