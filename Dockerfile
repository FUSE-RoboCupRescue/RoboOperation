FROM ros:melodic-robot
RUN apt-get update && apt-get install -y \
    ros-melodic-joy \
    ros-melodic-image-view \
    ros-melodic-rviz \
    joystick \
    evtest \
    && rm -rf /var/lib/apt/lists/*
ENV ROS_MASTER_URI=http://192.168.1.10:11311
ENV ROS_IP=192.168.1.20
CMD ["bash", "-c", "source /opt/ros/melodic/setup.bash && bash"]
