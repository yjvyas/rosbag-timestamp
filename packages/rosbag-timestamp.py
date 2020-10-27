#!/usr/bin/env python3

import os
import rospy
import rosbag
import numpy as np
from std_msgs.msg import Int32, String
from sensor_msgs.msg import CompressedImage
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
from cv_bridge import CvBridge
from datetime import datetime
import cv2

if __name__ == '__main__':
    # create the node
    filepath = os.environ['ROSBAG_FILEPATH']

    print('File is {}'.format(filepath))

    bag = rosbag.Bag(filepath)
    filepath_new = filepath[:-4] + '_processed.bag'
    print('New file is {}'.format(filepath_new))
    bag_new = rosbag.Bag(filepath_new, 'w')
    message_times = {}
    bridge = CvBridge()

    for topic, msg, t in bag.read_messages():
        topic_details = topic.split('/')
        if topic_details[2:] == ['camera_node','image','compressed']:
            cv_image = bridge.compressed_imgmsg_to_cv2(msg)
            image_tsmp = datetime.fromtimestamp(rospy.Time(msg.header.stamp.secs, msg.header.stamp.nsecs).to_time())
            cv2.putText(cv_image, image_tsmp.isoformat(), (5, 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA )
            img_msg = bridge.cv2_to_compressed_imgmsg(cv_image)
            bag_new.write(topic, img_msg, msg.header.stamp)
        else:
            bag_new.write(topic, msg, msg.header.stamp if msg._has_header else t)
    
    bag_new.close()