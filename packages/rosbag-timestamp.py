#!/usr/bin/env python3

import os
import rospy
import rosbag
import numpy as np
from std_msgs.msg import Int32, String
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from cv_bridge import CvBridge


if __name__ == '__main__':
    # create the node
    filepath = os.environ['ROSBAG_FILEPATH']

    print('File is {}'.format(filepath))

    bag = rosbag.Bag(filepath)
    file_new = filepath[:-4] + '_processed.bag'
    print('New file is {}'.format(file_new))

    message_times = {}
    for topic, msg, t in bag.read_messages():
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(image_message, desired_encoding='passthrough')
        image_message = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
    
    print(message_times.keys())