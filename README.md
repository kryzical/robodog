# ROS2 with Gazebo Garden Docker Setup

This setup provides a containerized environment for ROS2 Humble with Gazebo Garden simulation optimized for professional robotic development.

## Project Structure

```
.
├── puppy_ros2_ws/       # ROS2 workspace with robot code
│   └── src/             # Source files for your robot
├── docker/              # Docker configuration 
│   ├── Dockerfile       # Docker image configuration
│   └── docker-compose.yml # Docker Compose configuration
├── models/              # Directory for simulation model files
├── scripts/             # Helper scripts
│   ├── build.sh         # Build Docker container
│   ├── run.sh           # Start Gazebo simulation
│   ├── spawn.sh         # Spawn test models
│   ├── check_mesh.sh    # Check mesh files
│   └── cleanup.sh       # Stop and remove containers
└── README.md            # Project documentation
```

## Getting Started

1. Build the Docker container:
   ```
   ./scripts/build.sh
   ```

2. Start the Gazebo simulation:
   ```
   ./scripts/run.sh
   ```

3. In a separate terminal, spawn test models:
   ```
   ./scripts/spawn.sh box    # Spawn a red box
   ./scripts/spawn.sh mesh   # Spawn a mesh model
   ```

4. Check mesh files if you have issues with mesh loading:
   ```
   ./scripts/check_mesh.sh
   ```

5. Clean up when finished:
   ```
   ./scripts/cleanup.sh
   ```

## Professional Development

This setup is designed for professional robotics development with the following features:

- Clean separation between robot code and simulation environment
- Consistent Docker environment for reproducible development
- Gazebo Garden integration with ROS2 Humble
- Persistent workspace volume for efficient development
- Support for mesh visualization and simulation

## Mesh Loading

For mesh loading to work correctly:
- Mesh files should be in STL, OBJ, or DAE format
- Mesh files are automatically copied from ROS workspace to the simulation environment
- The SDF file references meshes using `file:///workspace/models/puppybot/meshes/filename.STL`

## Troubleshooting

If meshes don't appear:
1. Run `./scripts/check_mesh.sh` to verify files exist in the correct locations
2. Check the SDF file path in `/tmp/mesh.sdf`
3. Make sure X11 permissions are set with `xhost +local:docker` 