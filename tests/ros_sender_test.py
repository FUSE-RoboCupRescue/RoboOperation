#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import serial
import time

# --- CONFIGURATION ---
PORT = '/dev/ttyACM0' 
BAUD = 115200
BUTTON_INDEX = 0  # Typically the 'A' or 'X' button depending on controller

class JoyToTeensy:
    def __init__(self):
        rospy.init_node('joy_to_teensy_bridge')
        
        # Initialize Serial
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=1)
            time.sleep(2) # Wait for Teensy reset
            rospy.loginfo("Connected to Teensy on %s", PORT)
        except Exception as e:
            rospy.logerr("Could not connect to Serial: %s", e)
            return

        # Subscribe to the joy topic coming from the Master PC
        self.sub = rospy.Subscriber("joy", Joy, self.joy_callback)
        rospy.loginfo("Bridge Node Ready. Press button %s to send command.", BUTTON_INDEX)

    def joy_callback(self, data):
        # data.buttons is a list. 1 = pressed, 0 = released
        if data.buttons[BUTTON_INDEX] == 1:
            rospy.loginfo("Button Pressed! Sending '1' to Teensy.")
            self.ser.write(b'1\n') # Send '1' and a newline
            
            # Read feedback from Teensy (optional)
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                rospy.loginfo("Teensy Response: %s", response)

if __name__ == '__main__':
    try:
        JoyToTeensy()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass