import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time

BUTTON_X = 0
BUTTON_A = 1
BUTTON_B = 2
BUTTON_Y = 3
BUTTON_LB = 4
BUTTON_RB = 5
BUTTON_LT = 6
BUTTON_RT = 7
JOY_LEFT_X = 0
JOY_LEFT_Y = 1
JOY_RIGHT_X = 2
JOY_RIGHT_Y = 3
# This needs to be checked...
PAD_UP = 4
PAD_RIGHT = 5
PAD_DOWN = 6
PAD_LEFT = 7

MAX_FLIPPER_VEL = 40
MAX_LINEAR_VEL = 50
MAX_ANGULAR_VEL = 50  # Should be in radians but stfu


def joy2string(buttons, axes):
    # This is just for the teensy!!!

    if buttons[BUTTON_B]: return "0 0 0 0 0 0 0"  # Emergency STOP!!!

    # Front flippers
    if buttons[BUTTON_RB] and not buttons[BUTTON_RT]:  # Move up
        flipper_front = MAX_FLIPPER_VEL
    elif not buttons[BUTTON_RB] and buttons[BUTTON_RT]:  # Move down
        flipper_front = -1. * MAX_FLIPPER_VEL
    else:
        flipper_front = 0

    # Back flippers
    if buttons[BUTTON_LB] and not buttons[BUTTON_LT]:  # Move up
        flipper_back = MAX_FLIPPER_VEL
    elif not buttons[BUTTON_LB] and buttons[BUTTON_LT]:  # Move down
        flipper_back = -1. * MAX_FLIPPER_VEL
    else:
        flipper_back = 0

    # Tank tracks
    if abs(axes[JOY_LEFT_Y]) > 0.1 and abs(axes[JOY_RIGHT_X]) < 0.1:  # Left Joystick Active
        # Linear movement
        track_right = MAX_LINEAR_VEL * axes[JOY_LEFT_Y]
        track_left = -1. * track_right
    elif abs(axes[JOY_LEFT_Y]) < 0.1 and abs(axes[JOY_RIGHT_X]) > 0.1:  # Right Joystick Active
        # Rotational movement
        track_right = MAX_ANGULAR_VEL * axes[JOY_RIGHT_X]
        track_left = track_right
        
        ############ Remove this later ############
        if axes[JOY_RIGHT_X] > 0:
            track_right *= 0
        else:
            track_left *= 0
        ###########################################
            
    elif abs(axes[JOY_LEFT_Y]) > 0.1 and abs(axes[JOY_RIGHT_X]) > 0.1:  # Both Joysticks Active
        # Ackermann Modus
        track_right = MAX_LINEAR_VEL * axes[JOY_LEFT_Y]
        track_left = -1. * track_right
        
        if axes[JOY_RIGHT_X] > 0:
            track_right *= 0.5 * (1 - axes[JOY_RIGHT_X])
        elif axes[JOY_RIGHT_X] < 0:
            track_left *= 0.5 * (1 + axes[JOY_RIGHT_X])
    else:
        track_right = 0
        track_left = 0
        
    # Light
    light_switch = 1 if buttons[BUTTON_A] else 0

    track_right = int(track_right)
    track_left = int(track_left)
    flipper_front = int(flipper_front)
    flipper_back = int(flipper_back)

    out = f"{track_right} {track_left} {-flipper_front} {flipper_front} {flipper_back} {-flipper_back} {light_switch}"
    return out


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
