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

There are two ways to run the container:

#### Method 1: Using Docker Compose
```bash
cd puppy_description
docker-compose build
docker-compose up -d
docker-compose exec puppy_ros bash
```

#### Method 2: Using Docker directly
```bash
cd puppy_description
docker build -t puppy_ros .
docker run -it --network host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/ros_ws/src/puppy_description \
    puppy_ros bash
```

## Sourcing the ROS setup
Before running any ROS commands, make sure to source the ROS setup file:
```bash
source /opt/ros/noetic/setup.bash
source /ros_ws/devel/setup.bash
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

If using Docker Compose:
```bash
docker-compose down
```

If using Docker directly:
```bash
# Press Ctrl+C to exit the container
# Or in another terminal:
docker stop $(docker ps -q --filter ancestor=puppy_ros)
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
   cd puppy_description
   ```

3. Build and run the container (choose one method):

   Method 1 (Docker Compose):
   ```bash
   docker-compose build
   docker-compose up -d
   docker-compose exec puppy_ros bash
   ```

   Method 2 (Docker directly):
   ```bash
   docker build -t puppy_ros .
   docker run -it --network host \
       -e DISPLAY=$DISPLAY \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v $(pwd):/ros_ws/src/puppy_description \
       puppy_ros bash
   ```

4. Source the ROS setup files inside the container:
   ```bash
   source /opt/ros/noetic/setup.bash
   source /ros_ws/devel/setup.bash
   ```

5. Run the simulation:
   ```bash
   # Launch the robot model with RViz
   roslaunch puppy_description display.launch

   # Or launch with Gazebo simulation
   roslaunch puppy_description gazebo.launch
   ```
