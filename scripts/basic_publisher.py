#!/usr/bin/env python

import rospy
from std_msgs.msg import String


def publishString():
    pub = rospy.Publisher("StringPublisher", String, queue_size=1000)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        hello_str = "hello world"
        pub.publish(hello_str)
        rospy.loginfo(hello_str)
        rate.sleep()

if __name__ == "__main__":
    try:
        publishString()
    except rospy.ROSInterruptException:
        pass
