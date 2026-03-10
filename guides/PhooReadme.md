## roscore on the master (jetson)
```
mux start roscore
```


another terminal **this is the important one where everything happens**


Start the robocup tmuxinator session
```
mux start robocup
```

you will get 4 windows, 2 docker containers and 2 ssh connections to the jetson. sadly, you have password verify in the docker. you can swap terminal widowns with CTRL+B and the ARROW_KEYS afterwards.

### joystick control

in one docker window run:

```
rosrun joy joy_node _dev:=/dev/input/js0
```

on the jetson we have 2 python environments, firstly the global python environment (the joystick interface needs this) and the environment for the realsenses  , run:

```
conda deactivate
python3 RoboOperation/scripts/joystick_interface
```

### camera feed stream

in the ssh run 

```
conda activte ...
python3 RoboOperation/scripts/camera_interace.py
```

in the docker window (you will have to close it and reopen again)
```
rviz -d /dual_camera.rviz
```

