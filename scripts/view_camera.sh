#!/bin/bash

# Default ROS master IP (Raspberry Pi's IP)
DEFAULT_ROS_MASTER_IP="192.168.5.40"

# Help message
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -i, --ip IP_ADDRESS    ROS master IP address (default: $DEFAULT_ROS_MASTER_IP)"
    echo "  -h, --help            Show this help message"
}

# Parse command line arguments
ROS_MASTER_IP=$DEFAULT_ROS_MASTER_IP
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--ip)
            ROS_MASTER_IP="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')

# Run the container with proper ROS networking and X11 forwarding
docker run -it --rm \
    --name ros1_noetic_viz \
    --network=host \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="ROS_MASTER_URI=http://${ROS_MASTER_IP}:11311" \
    --env="ROS_IP=${LOCAL_IP}" \
    --env="ROS_HOSTNAME=${LOCAL_IP}" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$(pwd):/catkin_ws/src:rw" \
    ros1_noetic_dev \
    bash -c "source /opt/ros/noetic/setup.bash && roslaunch puppy_camera view_camera.launch"