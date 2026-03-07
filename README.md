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



sudo docker build -t ros_melodic_joy .

## joystick connection and test

run the docker file

```
sudo docker run -it --rm --net=host --privileged --device=/dev/input/js0:/dev/input/js0 ros_melodic_joy
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


on the jeston

```
export ROS_MASTER_URI=http://192.168.1.10:11311
export ROS_IP=192.168.1.10
roscore
```


in another terminal
```
rostopic echo /joy
```
