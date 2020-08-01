#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
修改 topic 的名称
'''

import rosbag
import rospy
import getopt
import sys


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:", ["inputbag="])
    except getopt.GetoptError:
        print("usage: debag.py -i <inputbag>")
        sys.exit(2)

    inputbag = ""
    for opt, arg in opts:
        if opt in ("-i", "--inputbag"):
            inputbag = arg
    print('input file: ' + str(inputbag))
    outbag_name = "result.bag"
    outbag = rosbag.Bag(outbag_name, "w")
    with rosbag.Bag(inputbag) as bag:
        for topic, msg, t in bag.read_messages():
            if topic == "/imu0":
                outbag.write("/imu/data_raw", msg, t)
            else:
                outbag.write(topic, msg, t)
    outbag.close()


if __name__ == "__main__":
    main(sys.argv[1:])