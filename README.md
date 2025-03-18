# Puppy Robot ROS1 Noetic Container

This repository contains a Docker setup for simulating the Puppy robot in ROS1 Noetic.

## Prerequisites

- Docker
- Docker Compose
- X11 for GUI applications (for visualization)

## Setup

### 1. Allow X11 connections (Linux)

```bash
xhost +local:docker
```

### 2. Build and run the container

make sure you are in puppy_description
```bash
docker-compose build
docker-compose up -d
```

### 3. Enter the container

```bash
docker-compose exec puppy_ros bash
```

## Sourcing the ROS setup
Before running any ROS commands, make sure to source the ROS setup file:
```bash
source /opt/ros/noetic/setup.bash
source /catkin_ws/devel/setup.bash
```

## Running the simulation

Once inside the container, you can run the simulation using:

```bash
# Launch the robot model with RViz
roslaunch puppy_description display.launch

# Or launch with Gazebo simulation
roslaunch puppy_description gazebo.launch
```

## Development

The `puppy_description` package is mounted as a volume, so any changes you make to the files on your host machine will be reflected inside the container.

## Stopping the container

```bash
docker-compose down
```

## Executing commands inside the container
To execute commands inside the running container, use:
```bash
docker-compose exec puppy_ros bash
```

## Troubleshooting

If you encounter issues with Docker Compose, ensure you have version 1.29.2 or later installed. You can check your Docker Compose version with the following command:
```bash
docker-compose --version
```

If you need to update Docker Compose, follow the instructions [here](https://docs.docker.com/compose/install/).

If you encounter issues with the Docker system, you can clean it up by removing all stopped containers, unused networks, and dangling images with the following command:
```bash
docker system prune -a -f
```

## Running the project
To run the project, follow these steps:

1. Allow X11 connections (Linux):
   ```bash
   xhost +local:docker
   ```

2. Navigate to the `puppy_description` directory:
   ```bash
   cd /home/brian/ros1_test/puppy_testing/ros1_puppy_ws/src/puppy_description
   ```

3. Build and run the container:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. Enter the container:
   ```bash
   docker-compose exec puppy_ros bash
   ```

5. Source the ROS setup files inside the container:
   ```bash
   source /opt/ros/noetic/setup.bash
   source devel/setup.bash
   ```

6. Build the workspace inside the container:
   ```bash
   cd /ros_ws
   catkin_make
   source devel/setup.bash
   ```

7. Run the simulation:
   ```bash
   # Launch the robot model with RViz
   roslaunch puppy_description display.launch

   # Or launch with Gazebo simulation
   roslaunch puppy_description gazebo.launch
   ```
