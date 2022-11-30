from cv_bridge import CvBridge
import cv2
import rospy
from sensor_msgs.msg import Image





rospy.init_node('image_converter', anonymous=True)




cap = cv2.VideoCapture('test_video.mp4')

# image_pub = rospy.Publisher("image_topic",Image,queue_size=10)
image_pub = rospy.Publisher("camera_feed",Image,queue_size=10)
bridge = CvBridge()



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("exiting....")
        break
    
    image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
    print("publishing")
    # cv2.imshow("publisher",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()