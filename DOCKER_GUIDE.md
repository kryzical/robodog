# Docker Configuration Guide for PuppyPi Robot

This guide explains the Docker setup for the PuppyPi robot simulation.

## Docker Configuration Files

The project uses the following Docker-related files:

1. **Dockerfile**: Defines the base image with ROS Noetic and all required packages
2. **docker-compose.yml**: Configures multiple services for different use cases
3. **run_robot.sh**: A convenience script to run the simulation in different modes

## Launch Modes

The project supports three launch modes:

### 1. Simulation Mode (Default)

Launches the robot in Gazebo simulation with controllers and standing pose:

```bash
./run_robot.sh simulation
# or simply
./run_robot.sh
```

### 2. Development Mode

Opens an interactive shell for development and debugging:

```bash
./run_robot.sh dev
```

Inside the container, you can manually run:
```bash
# Launch the Gazebo simulation
roslaunch puppy_description gazebo.launch

# Or run RViz visualization
roslaunch puppy_description display.launch

# Or any other ROS commands
rostopic list
rosnode list
```

### 3. RViz Visualization Mode

Launches only the RViz visualization (lighter weight, no physics simulation):

```bash
./run_robot.sh rviz
```

## Directory Structure

The Docker configuration mounts directories as follows:

- `./puppy_description` → `/ros_ws/src/puppy_description` (inside container)
- `/tmp/.X11-unix` → `/tmp/.X11-unix` (for GUI forwarding)

## Customizing the Docker Setup

### Changing ROS Packages

To add more ROS packages to the Docker image, edit the Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y \
    ros-noetic-desktop-full \
    ros-noetic-gazebo-ros-control \
    # Add new packages here
    ros-noetic-your-package-name \
    && rm -rf /var/lib/apt/lists/*
```

### Modifying Launch Parameters

To modify how the robot is launched, you can edit the command in docker-compose.yml:

```yaml
command: bash -c "cd /ros_ws && catkin config --extend /opt/ros/noetic && catkin build && source /opt/ros/noetic/setup.bash && source /ros_ws/devel/setup.bash && roslaunch puppy_description gazebo.launch your_param:=value"
```

### Adding Data Persistence

To keep persistent data across container restarts, add a named volume:

```yaml
volumes:
  - ./puppy_description:/ros_ws/src/puppy_description
  - robot_data:/ros_ws/data
  - /tmp/.X11-unix:/tmp/.X11-unix:rw

# At the bottom of the file
volumes:
  robot_data:
```

## Troubleshooting

### GUI Display Issues

If you encounter issues with the GUI display:

1. Ensure X11 forwarding is enabled:
   ```bash
   xhost +local:docker
   ```

2. Try running with the `--privileged` flag:
   ```yaml
   # In docker-compose.yml
   privileged: true
   ```

### Build Errors

If you encounter build errors:

1. Try rebuilding with no cache:
   ```bash
   docker-compose build --no-cache
   ```

2. Check available disk space:
   ```bash
   docker system df
   ```

3. Clean Docker system:
   ```bash
   docker system prune -a
   ```

## Advanced Usage

### Running on Different Hosts

To run on a different host machine, you'll need to configure the environment variables accordingly:

```bash
DISPLAY=:0 ./run_robot.sh
```

### Using NVIDIA GPU Acceleration

For NVIDIA GPU acceleration, add the following to your docker-compose.yml services:

```yaml
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all
  - NVIDIA_DRIVER_CAPABILITIES=all
```

And install the NVIDIA Docker runtime on your host system.
