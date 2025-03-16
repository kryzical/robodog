#!/bin/bash
# Unified container script for Puppy Robot project
# This replaces the separate run_container, run_container_gui, and run_container_headless scripts

# Set default values
CONTAINER_MODE="gui"  # Options: gui, headless, auto
ROS_DISTRO="humble"   # Default to ROS 2 Humble
IMAGE_NAME="puppy_robot"
CONTAINER_NAME=""
HOST_IP="$(hostname -I | awk '{print $1}')"
NETWORK_MODE="host"
USE_GPU=false
USE_DEVICES=false
MOUNT_WORKSPACE=true
DETACHED=false
EXTRA_ARGS=""

# Help function
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help                 Show this help message"
    echo "  -m, --mode <mode>          Container mode: gui, headless, auto (default: auto)"
    echo "  -r, --ros <distro>         ROS distribution: noetic, humble (default: humble)"
    echo "  -i, --image <name>         Docker image name (default: puppy_robot)"
    echo "  -n, --name <name>          Container name (default: auto-generated)"
    echo "  --ip <ip>                  Host IP address (default: auto-detected)"
    echo "  --network <mode>           Network mode: host, bridge (default: host)"
    echo "  -g, --gpu                  Enable GPU support"
    echo "  -d, --devices              Mount hardware devices (/dev/ttyAMA0, /dev/video0)"
    echo "  -w, --no-workspace         Don't mount workspace volume"
    echo "  --detach                   Run container in detached mode"
    echo "  -e, --extra <args>         Extra arguments for docker run"
    echo ""
    echo "Example:"
    echo "  $0 --mode gui --ros humble --name my_container --gpu"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        -m|--mode)
            CONTAINER_MODE="$2"
            shift 2
            ;;
        -r|--ros)
            ROS_DISTRO="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE_NAME="$2"
            shift 2
            ;;
        -n|--name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        --ip)
            HOST_IP="$2"
            shift 2
            ;;
        --network)
            NETWORK_MODE="$2"
            shift 2
            ;;
        -g|--gpu)
            USE_GPU=true
            shift
            ;;
        -d|--devices)
            USE_DEVICES=true
            shift
            ;;
        -w|--no-workspace)
            MOUNT_WORKSPACE=false
            shift
            ;;
        --detach)
            DETACHED=true
            shift
            ;;
        -e|--extra)
            EXTRA_ARGS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Set container name if not provided
if [ -z "$CONTAINER_NAME" ]; then
    CONTAINER_NAME="${ROS_DISTRO}_${IMAGE_NAME}_$(date +%s)"
fi

# Determine container mode if auto
if [ "$CONTAINER_MODE" = "auto" ]; then
    if [ -n "$DISPLAY" ]; then
        CONTAINER_MODE="gui"
    else
        CONTAINER_MODE="headless"
        echo "No display detected, using headless mode"
    fi
fi

# Validate mode
if [ "$CONTAINER_MODE" != "gui" ] && [ "$CONTAINER_MODE" != "headless" ]; then
    echo "Invalid mode: $CONTAINER_MODE"
    show_help
fi

# Set ROS environment variables
ROS_MASTER_URI="http://${HOST_IP}:11311"
ROS_IP="${HOST_IP}"
ROS_HOSTNAME="${HOST_IP}"

# Base docker command
DOCKER_CMD="docker run"

# Add detached or interactive flags
if [ "$DETACHED" = true ]; then
    DOCKER_CMD="$DOCKER_CMD -d"
else
    DOCKER_CMD="$DOCKER_CMD -it"
fi

# Add remove flag
DOCKER_CMD="$DOCKER_CMD --rm"

# Add container name
DOCKER_CMD="$DOCKER_CMD --name $CONTAINER_NAME"

# Add network settings
DOCKER_CMD="$DOCKER_CMD --network=$NETWORK_MODE"

# Add environment variables
DOCKER_CMD="$DOCKER_CMD -e ROS_MASTER_URI=$ROS_MASTER_URI -e ROS_IP=$ROS_IP -e ROS_HOSTNAME=$ROS_HOSTNAME"

# Add workspace volume if requested
if [ "$MOUNT_WORKSPACE" = true ]; then
    DOCKER_CMD="$DOCKER_CMD -v $(pwd):/ros_ws"
fi

# Add GUI support if needed
if [ "$CONTAINER_MODE" = "gui" ]; then
    DOCKER_CMD="$DOCKER_CMD -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix"
    
    # Check if we need to set X authority
    if [ -f "$XAUTHORITY" ]; then
        DOCKER_CMD="$DOCKER_CMD -v $XAUTHORITY:/root/.Xauthority:ro"
    fi
fi

# Add GPU support if requested
if [ "$USE_GPU" = true ]; then
    DOCKER_CMD="$DOCKER_CMD --gpus all"
fi

# Add device mounts if requested
if [ "$USE_DEVICES" = true ]; then
    # Add serial port for controller
    if [ -e "/dev/ttyAMA0" ]; then
        DOCKER_CMD="$DOCKER_CMD --device /dev/ttyAMA0"
    fi
    
    # Add camera device
    if [ -e "/dev/video0" ]; then
        DOCKER_CMD="$DOCKER_CMD --device /dev/video0"
    fi
fi

# Add any extra arguments
if [ -n "$EXTRA_ARGS" ]; then
    DOCKER_CMD="$DOCKER_CMD $EXTRA_ARGS"
fi

# Add image name
if [ "$ROS_DISTRO" = "noetic" ]; then
    DOCKER_CMD="$DOCKER_CMD ${IMAGE_NAME}:noetic"
else
    DOCKER_CMD="$DOCKER_CMD ${IMAGE_NAME}:${ROS_DISTRO}"
fi

# Print the command being executed
echo "Executing: $DOCKER_CMD"

# Execute the command
eval $DOCKER_CMD 