import time
from piper_sdk import C_PiperInterface
from utils import *


class XPiperController:

    def __init__(self):

        # Connect to Piper via CAN
        self.piper = C_PiperInterface("can0")
        self.piper.ConnectPort()

        # Enable the arm
        self.piper.EnableArm()

        self.joint_step = 0.1
        self.current_joint_state = [0., 0., 0., 0., 0., 0.]
        self.gripper_state = False  # False: closed, True: open

    def move(self, buttons, axes):

        if buttons[BUTTON_RT]:  # Gripper action

            if self.gripper_state:
                self.piper.GripperControl(0.0)     # close
            else:
                self.piper.GripperControl(0.04)    # open

            self.gripper_state = not self.gripper_state

            time.sleep(1)

        else:  # Arm action

            self.current_joint_state[0] += self.joint_step * axes[JOY_RIGHT_X]
            self.current_joint_state[1] += self.joint_step * axes[JOY_RIGHT_Y]
            self.current_joint_state[2] += self.joint_step * axes[JOY_LEFT_X]
            self.current_joint_state[3] += self.joint_step * axes[JOY_LEFT_Y]
            self.current_joint_state[4] += self.joint_step * axes[PAD_X]
            self.current_joint_state[5] += self.joint_step * axes[PAD_Y]

            # Send joint command
            self.piper.JointControl(*self.current_joint_state)

            time.sleep(0.05)
            