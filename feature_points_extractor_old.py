import cv2
import numpy as np
from sklearn.cluster import KMeans, k_means
import matplotlib.pyplot as plt
import copy
import time
import math
import random

global orb
orb = cv2.ORB_create()

# global prev_max_size
# prev_max_size = 0

# global max_key_point
# max_key_point = 0

global init
init = "no"

global landmark
global p_landmark

p_landmark = [0,0]
landmark = 10

def get_distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)




def get_features(original_face):



    # l_b=np.array([0,230,170])# lower hsv bound for red
    # u_b=np.array([255,255,220])# upper hsv bound to red




    # global prev_max_size
    # global max_key_point
    global init
    global landmark
    global p_landmark
    # original_face = cv2.imread('road1.png')
    gray_face = cv2.cvtColor(original_face, cv2.COLOR_BGR2GRAY)

    # gray_face =  cv2.imread('road1.png', 0) 
    # query_face_gray =  cv2.imread('road1.png', 0) 




    original_keypoints, original_descriptor = orb.detectAndCompute(gray_face, None)
    keypoints_without_size = np.copy(original_face)
    # keypoints_with_size = np.copy(original_face)

    op=cv2.drawKeypoints(original_face, original_keypoints, keypoints_without_size, color = (0, 255, 0))
    # op=cv2.drawKeypoints(original_face, original_keypoints, keypoints_with_size, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # op = copy.copy(original_face)
    key_points_loc = []

    for i in original_keypoints:
        key_points_loc.append(i.pt)

    x = []
    y = []
    for i in range(len(key_points_loc)):
        x.append(key_points_loc[i][0])
        y.append(key_points_loc[i][1])

        ###K-means clustering

    # paint_kp = True
    # try:

    #     k = 4
    #     kmeans = KMeans(n_clusters=k)
    #     kmeans.fit(key_points_loc)

    #     kmeans1 = copy.deepcopy(kmeans)

    #     by_cluster = {}

    #     for i in range(k):
    #         by_cluster[i] = []

    #     for i in range(len(key_points_loc)):
    #         by_cluster[kmeans.labels_[i]].append([key_points_loc[i][0],key_points_loc[i][1]])

    #     cluster_centers = []
    #     for i in range(k):
    #         c1,c2 = 0,0
    #         l = by_cluster[i]
    #         for j in range(len(l)):
    #             # print(j)
    #             c1 += l[j][0]
    #             c2 += l[j][1]
    #         c1 = c1/len(l)
    #         c2 = c2/len(l)
    #         cluster_centers.append([c1,c2])
    # except:
    #     pass

    # try:
        

    #     # max_size = 0
        
    #     # max_list = []

    #     # for i in range(len(key_points_loc)):
    #     #     if original_keypoints[i].size > max_size:
    #     #         max_size = original_keypoints[i].size
    #     #         max_key_point_temp = i

    #     # for i in range(len(key_points_loc)):
    #     #     if original_keypoints[i].size == max_size:
    #     #         max_list.append(i)
    #     # print(max_list)

    #     # flag = 0

    #     # for i in max_list:
    #     #     dist = get_distance(key_points_loc[max_key_point],key_points_loc[i])
    #     #     if dist<10 and dist>0:
    #     #         print(dist)
    #     #         prev_max_size = max_size
    #     #         max_key_point = i
    #     #         flag = 1
    #     #         break
    #     # prev_max_size = max_size
        
    #     # if flag == 1:

    #     pass
    # except:
    #     pass
    
    try:
        if not init == 'done':
            p_landmark = key_points_loc[landmark]
            init = 'done'

        dists = []

        for i in range(len(key_points_loc)):
            dists.append(get_distance(key_points_loc[i],p_landmark))
            # print(key_points_loc[i],p_landmark)

        m = min(dists)
        landmark = dists.index(m)
        p_landmark = key_points_loc[landmark]
        print(landmark,m)
        # print(key_points_loc[landmark],p_landmark)
        # print(dists[:10])

        cv2.circle(op, (int(key_points_loc[landmark][0]),int(key_points_loc[landmark][1])), 10, color= (0,0,255), thickness=6, lineType=8, shift=0)
    except:
        pass



   


    
    

    return op
    # cv2.imshow("features",op)
    # cv2.waitKey()