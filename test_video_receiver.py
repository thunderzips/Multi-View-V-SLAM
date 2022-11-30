import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node("sss")


bridge = CvBridge()


def display_cv2(data):
    print("receiving")
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
      cv2.imshow("received",cv_image)
      cv2.waitKey(3)

    except CvBridgeError as e:
      print(e)
    # cv_image = bridge.imgmsg_to_cv2(data, "bgr8")


image_sub = rospy.Subscriber("image_topic",Image,display_cv2)


rospy.spin()