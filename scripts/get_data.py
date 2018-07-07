#! /usr/bin/env python

import roslib
import rospy
import rosbag
from std_msgs.msg import Int32, String
from geometry_msgs.msg import Twist
import numpy as np
from numpy import inf

import csv

import cv2

bag = rosbag.Bag('my_files/bag-recod-2r.bag', 'r')

bag_name = bag.filename

topicNames = []

for topic, msg, t in bag.read_messages():
    if topic not in topicNames:
        topicNames.append(topic)

print topicNames

scan_values = []
frame_names = []
cmd_x = []
cmd_z = []

range_max = 0

for subtopic, msg, t in bag.read_messages(topicNames):
    if subtopic == '/scan':
        scan_values.append(list(msg.ranges))
        range_max = msg.range_max
    elif subtopic == '/frame_name':
        frame_names.append(msg.data)
    elif subtopic == '/cmd_vel':
        cmd_x.append(msg.linear.x)
        cmd_z.append(msg.angular.z)

np_scan = np.array(scan_values)
np_frame_name =  np.array(frame_names)
np_cmd_x = np.array(cmd_x)
np_cmd_y = np.array(cmd_z)

np_scan = np_scan / range_max

# print np_scan[25]

# print np_frame_name[1]

np_scan[np_scan == inf] = 1.0

# exit(0)

# for i in range(len(np_frame_name)):
#     # print np_frame_name[i]
#     img = cv2.imread('my_files/' + np_frame_name[i])
#
#     cv2.imshow('img', img)
#     cv2.waitKey(100)

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