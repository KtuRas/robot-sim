#! /usr/bin/env python

import roslib
import rospy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

import numpy

x_max = 2.0
y_max = 1.0

d_counter = 0

cmd_x = 0.0
cmd_y = 0.0

d_switch = 0

def joy_callback(data):
    global x_max
    global y_max
    global d_counter
    global cmd_x
    global cmd_y
    global d_switch

    # print str(data.axes) + " " + str(data.buttons)
    if  data.buttons[0] and d_counter == 0:
        x_max += 0.5
        d_counter = 10
        if x_max > 5.0:
            x_max = 5.0

        print 'x_max: ', x_max
    elif data.buttons[1] and d_counter == 0:
        x_max -= 0.5
        d_counter = 10
        if x_max < 0:
            x_max = 0

        print 'x_max: ', x_max
    elif  data.buttons[2] and d_counter == 0:
        y_max += 0.5
        d_counter = 10
        if y_max > 5.0:
            y_max = 5.0

        print 'y_max: ', y_max
    elif data.buttons[3] and d_counter == 0:
        y_max -= 0.5
        d_counter = 10
        if y_max < 0:
            y_max = 0

        print 'y_max: ', y_max

    d_counter -= 1
    if d_counter < 0:
        d_counter = 0

    # print x_max, ' ', y_max

    cmd_x = data.axes[1] * x_max
    cmd_y = data.axes[3] * y_max

    d_switch = data.buttons[6]

if __name__ == '__main__':

    rospy.init_node("joy_cmd")
    rospy.Subscriber("joy", Joy, joy_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    cmd_data = Twist()

    while not rospy.is_shutdown():
        # print cmd_x ,' ' , cmd_y

        if d_switch:
            cmd_data.linear.x = cmd_x
            cmd_data.angular.z = cmd_y

            pub.publish(cmd_data)
        else:
            cmd_data.linear.x = 0
            cmd_data.angular.z = 0

            pub.publish(cmd_data)

        rospy.sleep(0.1)
