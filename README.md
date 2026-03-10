# Connect Master PC to Jetson

first identify the ethernet port and it's connection name

```
ip addr show
nmcli connection show
```

then on the master PC assign a ipv4 adress, e.g. 192.168.1.20

```
sudo nmcli con mod "WIRED_CON_NAME" ipv4.addresses 192.168.1.20/24 ipv4.method manual

sudo nmcli con up "WIRED_CON_NAME"
```

Do the same on te Jetson with a differen IP, e.g. 192.168.1.10

```
sudo nmcli con mod "WIRED_CON_NAME" ipv4.addresses 192.168.1.10/24 ipv4.method manual

sudo nmcli con up "WIRED_CON_NAME"

```





## joystick connection and test

build the docker file

```
sudo docker build -t ros_melodic_joy .
```

run the docker file


```
sudo docker run -it --rm --net=host --privileged --device=/dev/input/js0:/dev/input/js0 ros_melodic_joy
```

or with display 

```
sudo docker run -it --rm --net=host --privileged \
  --device=/dev/input/js0:/dev/input/js0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ros_melodic_joy
```

```
sudo docker run -it --rm --net=host --privileged \
  --device=/dev/input/js0:/dev/input/js0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/deno/git/RoboOperation/rviz_configs/dual_camera.rviz:/dual_camera.rviz \
  ros_melodic_joy
```

check your joystick id 

```
ls -l /dev/input/js0
```


```
test it in docker 
jstest /dev/input/js0
```


if the test went through

```
rosrun joy joy_node _dev:=/dev/input/js0
```


on the jetson

```
export ROS_MASTER_URI=http://192.168.1.10:11311
export ROS_IP=192.168.1.10
roscore
```


in another terminal
```
rostopic echo /joy
```

# Image Gui

after following the previous steps, run on the robot

```
python3
```
on robot


afterwards, in the docker container of pc run


```
rviz -d /dual_camera.rviz
```

or to just view one img


```
rosrun image_view image_view image:=/camera/image_raw
``` 

# TMUX for quasi-pleasent ROS usage

## Tmux: Quick 2x2 Grid Guide

Follow these steps to split your terminal into 4 equal panes (ideal for ROS nodes, logs, and teleop).

### The Step-by-Step Command Sequence

1.  **Open tmux**: Type `tmux` in your terminal.
2.  **First Split (Side-by-Side)**: Press `Ctrl` + `b`, then `%`. 
    * *Result: You now have 2 vertical columns.*
3.  **Split the Right Pane**: Press `Ctrl` + `b`, then `"`. 
    * *Result: The right side is now split into two rows.*
4.  **Move Focus to the Left**: Press `Ctrl` + `b`, then `Left Arrow`.
5.  **Split the Left Pane**: Press `Ctrl` + `b`, then `"`.
    * *Result: You now have a perfect 4-pane grid.*

---

### Essential Navigation
* **Switch Panes:** `Ctrl` + `b` + `Arrow Keys`
* **Toggle Fullscreen (Zoom):** `Ctrl` + `b` + `z` (Repeat to shrink back)
* **Cycle Layouts:** `Ctrl` + `b` + `Spacebar` (Useful if the 2x2 gets messy)
* **Close Pane:** Type `exit` or `Ctrl` + `d`

# regarding  teensy

ls /dev/ttyACM*



