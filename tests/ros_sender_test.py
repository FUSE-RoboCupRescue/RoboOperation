#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import serial
import time
from utils import *

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
        self.mode = 0  # 0: tank, 1: arm

        # Subscribe to joystick
        self.sub = rospy.Subscriber("joy", Joy, self.joy_callback)
        rospy.loginfo("Bridge Node Ready.")
        # self.arm_ctrl = XPiperController()

        # Start the loop
        self.loop()

    def joy_callback(self, data):
        # Always save the latest joystick state
        self.latest_buttons = data.buttons
        self.latest_axes = data.axes

    def send_tracks_command(self, msg):
        self.ser.write((msg + "\n").encode("utf-8"))
        rospy.loginfo("Sending message: %s", msg)
        response = self.ser.readline().decode('utf-8').strip()
        if response:
            rospy.loginfo("Teensy Response: %s", response)
        else:
            rospy.logwarn("No response from Teensy (timeout)")

    def loop(self):
        rate = rospy.Rate(PUBLISH_RATE)
        while not rospy.is_shutdown():
            if self.latest_buttons or self.latest_axes:
                
                # Change control mode
                if self.latest_buttons[BUTTON_X]:
                    self.send_tracks_command("0 0 0 0 0 0")
                    self.mode = 0
                
                elif self.latest_buttons[BUTTON_Y]:
                    self.send_tracks_command("0 0 0 0 0 0")
                    self.mode = 1
                
                # Control robot
                if self.mode == 0:
                    msg = joy2string(self.latest_buttons, self.latest_axes)
                    self.send_tracks_command(msg)
                
                elif self.mode == 1:
                    # self.arm_ctrl.move(self.latest_buttons, self.latest_axes)
                    pass

                else:
                    self.send_tracks_command("0 0 0 0 0 0")
                
            rate.sleep()

if __name__ == '__main__':
    try:
        JoyToTeensy()
    except rospy.ROSInterruptException:
        pass
