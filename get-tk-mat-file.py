#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
将录制的imu数据bag文件，转换为imu-tk使用的mat文件
'''


import rosbag
import rospy
import getopt
import sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:t:", ["inputbag=", "topic="])
    except getopt.GetoptError:
        print("usage: get-tk-mat-file.py -i <inputbag> -t <topicname>")
        sys.exit(2)

    inputbag = ""
    topicname = ""
    for opt, arg in opts:
        if opt in ("-i", "--inputbag"):
            inputbag = arg
        if opt in ("-t", "--topic"):
            topicname = arg
    print('open file: ' + str(inputbag))

    counter = 0
    accfile = open('acc.mat', 'w')
    gyrfile = open('gyr.mat', 'w')
    with rosbag.Bag(inputbag) as bag:
        for topic, msg, t in bag.read_messages():
            if topic == topicname:
                counter += 1
                time_stamp = msg.header.stamp.to_nsec() / 1e9
                ax = msg.linear_acceleration.x
                ay = msg.linear_acceleration.y
                az = msg.linear_acceleration.z
                gx = msg.angular_velocity.x
                gy = msg.angular_velocity.y
                gz = msg.angular_velocity.z

                accstr = '   ' + str(time_stamp) + \
                         '   ' + str(ax) + \
                         '   ' + str(ay) + \
                         '   ' + str(az) + '\n'
                gyrstr = '   ' + str(time_stamp) + \
                         '   ' + str(gx) + \
                         '   ' + str(gy) + \
                         '   ' + str(gz) + '\n'
                accfile.write(accstr)
                gyrfile.write(gyrstr)
    print('catch ' + str(counter) + ' message')
    accfile.close()
    gyrfile.close()
    print('finished')


if __name__ == "__main__":
    main(sys.argv[1:])