import cv2
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import Image


rospy.init_node("camera_viewer_static")

bridge = CvBridge()

def disp_static(static_image):

    static_image = bridge.imgmsg_to_cv2(static_image, "bgr8")

    cv2.imshow("static_camera",static_image)
    cv2.waitKey(1)



static_image_sub = rospy.Subscriber("static_camera_feed",Image,disp_static)


rospy.spin()