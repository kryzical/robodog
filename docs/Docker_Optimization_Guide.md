# Docker Optimization Guide: From Dockerfile to Docker Compose

## Introduction

This guide helps developers transition from basic Dockerfile usage to more sophisticated container orchestration with Docker Compose. It also covers optimization techniques using BuildKit, multi-stage builds, and best practices for ROS 2 development.

## Why Use Docker Compose?

### Limitations of Using Just a Dockerfile

When working with a single Dockerfile:

- You need to manage container startup with complex `docker run` commands
- Dependencies between containers must be managed manually
- Network configuration is more difficult
- Environment variables need to be passed in each run command
- Volume mounting requires repeating the same options

### Benefits of Docker Compose

Docker Compose offers several advantages:

- **Declarative configuration**: Define your entire multi-container application in a YAML file
- **Container orchestration**: Manage multiple containers as a single service
- **Environment management**: Define environment variables in one place
- **Network management**: Automatic network creation and service discovery
- **Volume configuration**: Persistent data storage defined in the configuration
- **Resource limits**: Control CPU, memory usage per service
- **Dependency handling**: Start containers in the correct order

## Transitioning from Dockerfile to Docker Compose

### Basic Example

Here's how to transition from a `docker run` command to Docker Compose:

**Before (running with docker run):**
```bash
docker build -t my_ros_app .
docker run -it --rm \
  --privileged \
  --network=host \
  -v /dev/video0:/dev/video0 \
  -v $(pwd):/ros_ws/src \
  -e DISPLAY=$DISPLAY \
  my_ros_app bash
```

**After (docker-compose.yml):**
```yaml
version: '3'

services:
  ros_app:
    build: .
    image: my_ros_app
    privileged: true
    network_mode: host
    volumes:
      - /dev/video0:/dev/video0
      - ./:/ros_ws/src
    environment:
      - DISPLAY=${DISPLAY}
    command: bash
```

### ROS 2 Multi-Container Example

For ROS 2 applications, Docker Compose really shines when decomposing your system into microservices:

```yaml
version: '3'

services:
  # Base configuration that others can extend
  ros2_base:
    build:
      context: .
      dockerfile: Dockerfile
    image: my_ros2_project:humble
    network_mode: host
    environment:
      - ROS_DOMAIN_ID=42
    
  # Camera node
  camera:
    extends: ros2_base
    privileged: true
    devices:
      - /dev/video0:/dev/video0 
    volumes:
      - /dev/vchiq:/dev/vchiq
      - ./:/ros_ws/src
    environment:
      - DISPLAY=${DISPLAY}
    command: bash -c "source /opt/ros/humble/setup.bash && ros2 launch puppy_camera camera.launch.py"
    
  # Visualization
  rviz:
    extends: ros2_base
    volumes:
      - ./:/ros_ws/src
      - /tmp/.X11-unix:/tmp/.X11-unix
    environment:
      - DISPLAY=${DISPLAY}
    command: bash -c "source /opt/ros/humble/setup.bash && ros2 run rviz2 rviz2"
    depends_on:
      - camera
      
  # Development shell
  dev:
    extends: ros2_base
    volumes:
      - ./:/ros_ws/src
    command: bash
```

## BuildKit Optimizations

Docker BuildKit is a next-generation builder with many performance improvements and advanced features.

### Enabling BuildKit

In your shell:
```bash
export DOCKER_BUILDKIT=1
```

In your docker-compose.yml:
```yaml
version: '3'
services:
  myapp:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - BUILDKIT_INLINE_CACHE=1
```

### BuildKit Features

1. **Parallel Building**: BuildKit can execute multiple build stages in parallel
2. **Improved Caching**: More intelligent caching of build steps
3. **Mount Options**: More efficient file handling during builds
4. **Build Secrets**: Securely use credentials during build without embedding them

### Using BuildKit Syntax in Dockerfiles

Modern BuildKit features can be enabled with the syntax directive:
```dockerfile
# syntax=docker/dockerfile:1.4

FROM ros:humble-ros-base

# Mount cache for apt packages
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y python3-pip

# Example of using secrets (for private repos)
RUN --mount=type=secret,id=github_token \
    echo "Using secrets for authenticated operations"
```

## Multi-Stage Builds

Multi-stage builds allow you to use multiple FROM statements in your Dockerfile, with each creating a stage. You can selectively copy artifacts from one stage to another, leaving behind everything you don't need.

### Basic Example

```dockerfile
# Build stage
FROM ros:humble-ros-base AS builder

WORKDIR /ros_ws/src
COPY . .

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions

# Build the workspace
RUN . /opt/ros/humble/setup.sh && \
    cd /ros_ws && \
    colcon build

# Runtime stage
FROM ros:humble-ros-core

# Copy the built artifacts
COPY --from=builder /ros_ws/install /ros_ws/install

# Set up environment
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
    echo "source /ros_ws/install/setup.bash" >> ~/.bashrc

CMD ["bash"]
```

## Space Optimization Techniques

### 1. Layer Optimization

Combine related commands to reduce the number of layers:

```dockerfile
# Bad: Many layers
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
RUN rm -rf /var/lib/apt/lists/*

# Good: Single layer
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 2. Use .dockerignore

Create a `.dockerignore` file to exclude files not needed in the build:

```
.git
*.log
build/
install/
log/
```

### 3. Clean Up in the Same Layer

Always clean up in the same RUN command:

```dockerfile
RUN apt-get update && apt-get install -y \
    some-package \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
```

### 4. Use --no-install-recommends

Avoid installing recommended but not required packages:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-name
```

## Efficient ROS 2 Development with Docker Compose

### Development Workflow

1. **Initial Setup**:
```bash
docker-compose build
```

2. **Run Development Container**:
```bash
docker-compose run --rm dev
```

3. **Launch Specific Components**:
```bash
docker-compose up camera rviz
```

4. **View Logs**:
```bash
docker-compose logs -f camera
```

5. **Rebuild After Changes**:
```bash
docker-compose build --no-cache
```

### Debugging Techniques

1. **Interactive Debug Session**:
```bash
docker-compose run --rm dev bash
```

2. **Run with ROS 2 CLI Tools**:
Inside container:
```bash
ros2 topic list
ros2 node list
ros2 topic echo /camera/image_raw
```

3. **Checking ROS 2 Node Graph**:
```bash
docker-compose exec dev ros2 node info /camera_publisher
```

## Advanced Docker Compose Features

### 1. Profiles for Different Configurations

```yaml
services:
  camera:
    profiles: ["hardware", "all"]
    # camera config...
    
  simulation:
    profiles: ["sim", "all"]
    # simulation config...
```

Run with specific profile:
```bash
docker-compose --profile hardware up
```

### 2. Healthchecks

```yaml
services:
  my_service:
    healthcheck:
      test: ["CMD", "ros2", "topic", "list"]
      interval: 10s
      timeout: 5s
      retries: 3
```

### 3. Resource Limits

```yaml
services:
  compute_intensive_node:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Conclusion

Transitioning from a basic Dockerfile to Docker Compose offers significant benefits for ROS 2 developers, especially for multi-node applications. By incorporating BuildKit, multi-stage builds, and proper image optimization techniques, you can create a more efficient, maintainable, and easier-to-use development environment.

The learning curve is worth it - Docker Compose simplifies complex container configurations and allows you to focus more on ROS 2 development and less on container management. 