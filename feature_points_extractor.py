import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import math
import random

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

    rl_val = {True:'r',False:'l'}
    center = [np.shape(original_image)[1]/2,np.shape(original_image)[0]/2]

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

    return op, rl_val[list(np.array(p_landmark)-np.array(center))[0] > 0]

