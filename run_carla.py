import glob
import os
import sys
from weakref import ref
import carla
import random
import time
import numpy as np

import pygame
import pygame.camera
from pygame.locals import *


from cv_bridge import CvBridge
import cv2
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
from PIL import Image as im


global vehicle
global steer
global throt

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (sys.version_info.major,sys.version_info.minor,'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except:
    pass


rospy.init_node('carla_car', anonymous=True)
image_pub = rospy.Publisher("camera_feed",Image,queue_size=10)
posx_pub = rospy.Publisher("posx",Float64,queue_size=10)
posy_pub = rospy.Publisher("posy",Float64,queue_size=10)
bridge = CvBridge()



def compute_display(image, camera):

    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))

    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)

    image_pub.publish(bridge.cv2_to_imgmsg(array, "bgr8"))

    print('published image')


    camx = camera.get_transform().location.x
    camy = camera.get_transform().location.y
    camz = camera.get_transform().location.z
    
    posx_pub.publish(camx)
    posy_pub.publish(camy)




def main():
    global vehicle
    global steer
    global throts

    pygame.init()
    display_surface = pygame.display.set_mode((300,300))
    pygame.display.set_caption('Keyboard controls')
    clock = pygame.time.Clock()
    
    client = carla.Client('localhost',2000)
    client.set_timeout(20)

    world = client.load_world('Town02')

    bplib = world.get_blueprint_library()
    vehicle_bp = random.choice(bplib.filter('vehicle.bmw.*'))
    transform = carla.Transform(carla.Location(x=-5,y=250,z=5),carla.Rotation(yaw=270))

    vehicle = world.spawn_actor(vehicle_bp,transform)

    camera_bp = bplib.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x','800')
    camera_bp.set_attribute('image_size_y','800')
    camera_bp.set_attribute('fov','90')
   
    
    camera_transform = carla.Transform(carla.Location(x=0,z=2))
    camera = world.spawn_actor(camera_bp,camera_transform, attach_to=vehicle)
    
    map = world.get_map()

    camera.listen(lambda image: compute_display(image,camera))
    
    # vehicle.set_autopilot(True)

    while True:
        steer = 0
        throt = 0

        pygame.display.flip()
        keys=pygame.key.get_pressed()

        if keys[K_w]:
            throt = 0.7
            rev = False
            vehicle.apply_control(carla.VehicleControl(throttle=throt, steer=steer,reverse = rev))

        if keys[K_s]:
            throt = 0.4
            rev = True
            vehicle.apply_control(carla.VehicleControl(throttle=throt, steer=steer,reverse = rev))

        if keys[K_a]:
            steer = -0.5
            vehicle.apply_control(carla.VehicleControl(throttle=throt, steer=steer,reverse = rev))

        if keys[K_d]:
            steer = 0.5
            vehicle.apply_control(carla.VehicleControl(throttle=throt, steer=steer,reverse = rev))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
                

if __name__ == '__main__':
    main()