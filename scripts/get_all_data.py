#! /usr/bin/env python

import roslib
import rospy
import rosbag
from std_msgs.msg import Int32, String
from geometry_msgs.msg import Twist
import numpy as np
from numpy import inf

import cv2
import csv

bag1 = rosbag.Bag('my_files/bag-recod-2r.bag', 'r')
bag2 = rosbag.Bag('my_files/bag-recod-2l.bag', 'r')

scan_values = []
frame_names = []
cmd_x = []
cmd_z = []

range_max = 0

def get_data_from_bag(pBag, pDir):
    global scan_values, frame_names, cmd_x, cmd_z, range_max

    topicNames = []

    for topic, msg, t in pBag.read_messages():
        if topic not in topicNames:
            topicNames.append(topic)

    for subtopic, msg, t in pBag.read_messages(topicNames):
        if subtopic == '/scan':
            scan_values.append(list(msg.ranges))
            range_max = msg.range_max
        elif subtopic == '/frame_name':
            index1 = msg.data.find('/')
            imgName = msg.data[index1:]
            imgName = "imgs_" + pDir + imgName
            # print imgName
            frame_names.append(imgName)
        elif subtopic == '/cmd_vel':
            cmd_x.append(msg.linear.x)
            cmd_z.append(msg.angular.z)

get_data_from_bag(bag1, 'r')
get_data_from_bag(bag2, 'l')

np_scan = np.array(scan_values)
np_frame_name =  np.array(frame_names)
np_cmd_x = np.array(cmd_x)
np_cmd_y = np.array(cmd_z)

np_scan = np_scan / range_max

np_scan[np_scan == inf] = 1.0

np.save('my_files/np_scan', np_scan)
np.save('my_files/np_frame_name', np_frame_name)
np.save('my_files/np_cmd_x', np_cmd_x)
np.save('my_files/np_cmd_y', np_cmd_y)


myData = [['frame_name', 'scan', 'cmd_x', 'cmd_z']]

for i in range(len(np_frame_name)):
    myData.append([np_frame_name[i], np_scan[i], np_cmd_x[i], np_cmd_y[i]])

with open('my_files/data.csv', 'w') as File:
    writer = csv.writer(File)
    writer.writerows(myData)