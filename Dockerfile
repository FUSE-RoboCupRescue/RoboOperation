# Use the official ROS Melodic base
FROM ros:melodic-robot

# Install the core joystick driver and diagnostic tools
RUN apt-get update && apt-get install -y \
    ros-melodic-joy \
    joystick \
    evtest \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variables for your specific network
ENV ROS_MASTER_URI=http://192.168.1.10:11311
ENV ROS_IP=192.168.1.20

CMD ["bash"]
