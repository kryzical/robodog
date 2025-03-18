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