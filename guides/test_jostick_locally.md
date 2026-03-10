3 terminals, 3 times

```
sudo docker run -it --rm --net=host --privileged \
  --device=/dev/input/js0:/dev/input/js0 \
  -e DISPLAY=$DISPLAY \
  -e ROS_MASTER_URI=http://localhost:11311 \
  -e ROS_HOSTNAME=localhost \
  -e ROS_IP=127.0.0.1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/deno/git/RoboOperation/rviz_configs/dual_camera.rviz:/dual_camera.rviz \
  ros_melodic_joy
```


then, in one

```
rosrun joy joy_node _dev:=/dev/input/js0 _autorepeat_rate:=60
```

and

```
```