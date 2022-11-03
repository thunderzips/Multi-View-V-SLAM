##IN TEST FILE
# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# from std_msgs.msg import Int32


# rospy.init_node("test_sender")

# bridge = CvBridge()

# pub = rospy.Publisher("image",Image,queue_size=10)


# global servo_dir
# servo_dir = 0

# def show_image_cb(im):
#     try:
#         im = bridge.imgmsg_to_cv2(im, desired_encoding='passthrough')
#         cv2.imshow('frame', im)
#     except:
#         pass
    
# def dir_cb(direction):
#     global servo_dir
#     servo_dir = direction
#     print(servo_dir)

# rospy.Subscriber("image_with_features", Image, show_image_cb)
# rospy.Subscriber("servo_direction", Int32, dir_cb)

#in while loop

# frame = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
# pub.publish(frame)

##IN MAIN FILE

# import rospy
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# from std_msgs.msg import Int32

# rospy.init_node("feature_points_extract")

# bridge = CvBridge()


# global image_pub
# image_pub = rospy.Publisher('image_with_features',Image,queue_size=10)
# global dir_pub
# dir_pub = rospy.Publisher('servo_direction',Int32,queue_size=10)

#in cb function get_features

# print("Got image")

# original_face = bridge.imgmsg_to_cv2(original_face, desired_encoding='passthrough')

# global image_pub
# global dir_pub

# op = bridge.cv2_to_imgmsg(op, encoding="passthrough")
# image_pub.publish(op)
# dir_pub.publish(int(list(np.array(p_landmark)-np.array(center))[0]))

# rospy.Subscriber("image", Image, get_features_cb)

# rospy.spin()