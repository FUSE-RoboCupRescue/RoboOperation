import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time
import utils import *


class XPiperController(Node):

    def __init__(self):
        super().__init__('xpiper_controller')

        # Arm trajectory publisher
        self.arm_pub = self.create_publisher(
            JointTrajectory,
            '/xpiper_arm_controller/joint_trajectory',
            10
        )

        # Gripper trajectory publisher
        self.gripper_pub = self.create_publisher(
            JointTrajectory,
            '/xpiper_gripper_controller/joint_trajectory',
            10
        )

        self.joint_step = 0.1
        self.current_joint_state = [0., 0., 0., 0., 0., 0.]
        self.gripper_state = False  # False: closed; True: open

    def move(self, buttons, axes):

        if buttons[BUTTON_RT]:  # Gripper action
            msg = JointTrajectory()
            msg.joint_names = ['gripper_joint']

            point = JointTrajectoryPoint()
            point.positions = [0.0] if self.gripper_state else [0.04]
            self.gripper_state = not self.gripper_state

            point.time_from_start.sec = 1

            msg.points.append(point)

            self.gripper_pub.publish(msg)

            time.sleep(2)

        else:  # Arm action
            msg = JointTrajectory()

            msg.joint_names = [
                'joint1',
                'joint2',
                'joint3',
                'joint4',
                'joint5',
                'joint6'
            ]
            duration = 1

            self.current_joint_state[0] += self.joint_step * axes[JOY_RIGHT_X]
            self.current_joint_state[1] += self.joint_step * axes[JOY_RIGHT_Y]
            self.current_joint_state[2] += self.joint_step * axes[JOY_LEFT_X]
            self.current_joint_state[3] += self.joint_step * axes[JOY_LEFT_X]
            self.current_joint_state[4] += self.joint_step * axes[PAD_UP]
            self.current_joint_state[5] += self.joint_step * axes[PAD_RIGHT]

            point = JointTrajectoryPoint()
            point.positions = self.current_joint_state
            point.time_from_start.sec = duration

            msg.points.append(point)

            self.arm_pub.publish(msg)

            time.sleep(duration + 1)
