# Docker Scripts

This directory contains scripts for Docker operations in the Puppy Robot project.

## Available Scripts

- `run_docker_compose.sh` - Main script for running Docker Compose services
- `clean_docker.sh` - Script for cleaning Docker resources (images, containers, volumes)
- `container.sh` - Unified script for running Docker containers (replaces all run_container* scripts)
- `get-docker.sh` - Script for installing Docker on the system

## Usage

### Docker Compose

To use Docker Compose for managing services:

```bash
# Build all services
./run_docker_compose.sh -b

# Run a specific service
./run_docker_compose.sh -s camera_node

# Run in detached mode
./run_docker_compose.sh -s controller -d

# Stop all services
./run_docker_compose.sh down
```

### Running Containers Directly

The unified container script provides flexible options for running Docker containers:

```bash
# Run with GUI support (default)
./container.sh --ros humble --name my_container

# Run in headless mode
./container.sh --mode headless --ros humble

# Run with hardware devices mounted
./container.sh --devices --ros humble

# Run with custom image name
./container.sh --image custom_image --ros humble

# Run in detached mode
./container.sh --detach --ros humble
```

See all available options:

```bash
./container.sh --help
```

### Cleaning Docker Resources

To clean up Docker resources and free disk space:

```bash
./clean_docker.sh
```

This script:
- Stops and removes all containers
- Removes unused images
- Removes unused volumes
- Cleans up build cache
- Prunes Docker networks

## Creating Symlinks

For convenience, a symlink to `run_docker_compose.sh` is created in the project root:

```bash
# Create symlink
ln -sf docker/scripts/run_docker_compose.sh ./run_compose.sh

# Use the symlink
./run_compose.sh -b -s camera_node
``` 