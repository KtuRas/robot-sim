#! /usr/bin/env python

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# The GPU id to use, usually either "0" or "1"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

# need for roslaunch 
import time
time.sleep(5)

import keras
from keras.models import Sequential, model_from_json

import numpy as np
from numpy import inf
import cv2

import roslib
import rospy
import rosbag
from std_msgs.msg import Int32, String
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

import signal
import sys

isExit = False

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')

	global isExit

	isExit = True

signal.signal(signal.SIGINT, signal_handler)

is_frame_changed = 0
is_lidar_changed = 0

scan_data = np.array([])
image_data = np.array([])

def set_lidar_changed(p_val):
    global is_lidar_changed
    is_lidar_changed = p_val

def set_image_changed(p_val):
    global is_frame_changed
    is_frame_changed = p_val

def callback(data):
    global scan_data

    if(is_lidar_changed == 0):
        np_scan = np.array(data.ranges)
        scan_data = np.concatenate((np_scan[0:60], np_scan[-61:-1]), axis=0)
        scan_data[np.isinf(scan_data)] = 1.0
        set_lidar_changed(1)

def image_callback(ros_data):
    global image_data

    if(is_frame_changed == 0):
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image_data = cv2.resize(image_np, (500, 500))
        image_data = image_data[250:500,:]
        set_image_changed(1)


model_path = "my_files"

if(len(sys.argv) > 1):
    model_path = str(sys.argv[1])
    print "***************model path**************"
    print model_path
    print "***************************************"

if __name__ == '__main__':

    rospy.init_node('predict_node')
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.Subscriber("/camera/rgb/image_raw/compressed",  CompressedImage, image_callback,  queue_size = 1)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    json_file = open(model_path + '/my_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_path +  "/my_model.h5")

    loaded_model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(lr=0.0001), metrics=["accuracy"])

    cmd_data = Twist()

    while not rospy.is_shutdown():

        if (is_frame_changed == 1) and (is_lidar_changed == 1):

            # print scan_data

            # cv2.imshow('image', image_data)
            # cv2.waitKey(10)

            image_data = image_data.astype('float32')
            image_data = (image_data / 127.5) - 1.0
            image_data = np.reshape(image_data, [1, 250, 500, 3])
            scan_data = np.reshape(scan_data, [1, 120])

            cmd_pre =  loaded_model.predict([image_data, scan_data])

            # cmd_pre[0] -= 1.0

            print cmd_pre[0]

            cmd_data.linear.x = 0.2
            cmd_data.angular.z = cmd_pre[0]
            
            pub.publish(cmd_data)

            set_lidar_changed(0)
            set_image_changed(0)

	if isExit: break

    cmd_data.linear.x = 0
    cmd_data.angular.z = 0

    pub.publish(cmd_data)
