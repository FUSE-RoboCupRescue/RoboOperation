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

MAX_FLIPPER_VEL = 10
MAX_LINEAR_VEL = 25
MAX_ANGULAR_VEL = 25  # Should be in radians but stfu

def joy2string(buttons, axes):
    # This is just for the teensy!!!

    if buttons[BUTTON_B]: return "0 0 0 0 0 0"  # Emergency STOP!!!

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
    if abs(axes[JOY_LEFT_Y]) > 0.1 and abs(axes[JOY_RIGHT_X]) < 0.1:  # Linear movement
        track_right = MAX_LINEAR_VEL * axes[JOY_LEFT_Y]
        track_left = -1. * track_right
    elif abs(axes[JOY_LEFT_Y]) < 0.1 and abs(axes[JOY_RIGHT_X]) > 0.1:  # Rotational movement
        track_right = MAX_ANGULAR_VEL * axes[JOY_RIGHT_X]
        track_left = track_right
    else:
        track_right = 0
        track_left = 0

    track_right = int(track_right)
    track_left = int(track_left)
    flipper_front = int(flipper_front)
    flipper_back = int(flipper_back)

    out = f"{track_right} {track_left} {-flipper_front} {flipper_front} {flipper_back} {-flipper_back}"
    return out

def control_arm(buttons, axes):
    pass
