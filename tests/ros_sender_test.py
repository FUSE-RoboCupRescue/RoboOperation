#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import serial
import time
from utils import joy2string

# --- CONFIGURATION ---
PORT = '/dev/ttyACM0'
BAUD = 115200
PUBLISH_RATE = 60  # Hz

class JoyToTeensy:
    def __init__(self):
        rospy.init_node('joy_to_teensy_bridge')

        # Initialize Serial
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=1)
            time.sleep(2)  # Wait for Teensy reset
            rospy.loginfo("Connected to Teensy on %s", PORT)
        except Exception as e:
            rospy.logerr("Could not connect to Serial: %s", e)
            return

        # State for joystick
        self.latest_buttons = []
        self.latest_axes = []

        # Subscribe to joystick
        self.sub = rospy.Subscriber("joy", Joy, self.joy_callback)
        rospy.loginfo("Bridge Node Ready.")

        # Start the loop
        self.loop()

    def joy_callback(self, data):
        # Always save the latest joystick state
        self.latest_buttons = data.buttons
        self.latest_axes = data.axes

    def loop(self):
        rate = rospy.Rate(PUBLISH_RATE)
        while not rospy.is_shutdown():
            if self.latest_buttons or self.latest_axes:
                msg = joy2string(self.latest_buttons, self.latest_axes)
                self.ser.write((msg + "\n").encode("utf-8"))
                rospy.loginfo("Sending message: %s", msg)
                response = self.ser.readline().decode('utf-8').strip()
                if response:
                    rospy.loginfo("Teensy Response: %s", response)
                else:
                    rospy.logwarn("No response from Teensy (timeout)")
            rate.sleep()

if __name__ == '__main__':
    try:
        JoyToTeensy()
    except rospy.ROSInterruptException:
        pass
