#!/usr/bin/env python
import rospy
import cv2
import os
import threading
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# --- CONFIGURATION ---
ROBOT_IP = "192.168.1.10"
CAMERAS = [
    {"index": 2, "topic": "/camera1/image_raw"},
    {"index": 5, "topic": "/camera2/image_raw"},
]
# ---------------------

def stream_camera(index, topic, bridge):
    pub = rospy.Publisher(topic, Image, queue_size=1)
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        rospy.logerr("Could not open camera at index %d", index)
        return

    rospy.loginfo("Publishing camera %d to %s", index, topic)
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            try:
                img_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
                img_msg.header.stamp = rospy.Time.now()
                pub.publish(img_msg)
            except Exception as e:
                rospy.logerr("Bridge error on camera %d: %s", index, e)
        rate.sleep()
    cap.release()

def main():
    os.environ['ROS_MASTER_URI'] = 'http://localhost:11311'
    os.environ['ROS_IP'] = ROBOT_IP
    rospy.init_node('dual_camera_publisher', anonymous=True)
    bridge = CvBridge()

    threads = []
    for cam in CAMERAS:
        t = threading.Thread(target=stream_camera, args=(cam["index"], cam["topic"], bridge))
        t.daemon = True
        t.start()
        threads.append(t)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass