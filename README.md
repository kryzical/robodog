# RoboDog Simulation

This project provides a simple way to run a robot dog simulation in Gazebo using Docker. It includes scripts for launching and stopping the simulation, as well as different model files for the robot.

## Project Structure

```
robodog/
├── config/                    # Configuration files
│   └── launch-with-robot.sh   # Main robot launch script used inside container
├── docker/                    # Docker configuration files
│   ├── config/                # Docker configuration backups
│   └── docker-compose.yml     # Docker Compose configuration
├── launch/                    # Launch scripts used inside the container
├── models/                    # Model files
│   └── sdf/                   # SDF model files for direct use in Gazebo
│       ├── puppy_white_body.sdf  # Permanent SDF with white body, black legs/camera
│       └── puppy_custom.sdf      # Custom SDF robot model with dog-like features
├── puppy_ros2_ws/             # ROS 2 workspace containing the robot description package
└── scripts/                   # User scripts
    ├── model-selector.sh      # Script to select which robot model to use
    ├── start-robot.sh         # Script to start the simulation
    └── stop-robot.sh          # Script to stop the simulation
```

## Quick Start

To launch the robot simulation:

```bash
./scripts/start-robot.sh
```

To stop the robot simulation:

```bash
./scripts/stop-robot.sh
```

To select which robot model to use:

```bash
./scripts/model-selector.sh
```

## Robot Models

The project includes multiple robot models:

1. **URDF/XACRO Robot Model**: The original robot model defined in the `puppy_ros2_ws/src/puppy_description/urdf/` directory. This model is used by ROS 2 for control and simulation.

2. **Permanent SDF Model**: A pre-generated SDF file (`models/sdf/puppy_white_body.sdf`) converted from the URDF with a white body and black legs/camera. This is used by default when launching the simulation.

3. **Custom SDF Model**: A manually created SDF file (`models/sdf/puppy_custom.sdf`) with dog-like features.

## Configuration

The launch script in `config/launch-with-robot.sh` prioritizes loading robot models in the following order:

1. The permanent SDF file if available (`puppy_permanent.sdf`)
2. A custom robot SDF file if available (`puppy_robot.sdf`)
3. The URDF/XACRO files, which are processed and converted to SDF

## Development Workflow

To modify the robot appearance or behavior:

1. Edit the URDF/XACRO files in `puppy_ros2_ws/src/puppy_description/urdf/`
2. Launch the simulation to see the changes
3. If you want to save the current model as a permanent SDF file, use the launch script which will automatically create it

## Docker Configuration

The Docker configuration in this project is set up to provide:

1. X11 forwarding for GUI applications
2. Volume mounting of relevant directories
3. A container environment with all necessary dependencies

All Docker-related files are in the `docker/` directory, with the main configuration in `docker-compose.yml`.

## Advanced Usage

### Modifying Launch Scripts

If you need to modify how the robot is launched inside the container:

1. Edit the `config/launch-with-robot.sh` script
2. Restart the simulation for changes to take effect

### Working with ROS 2

To work with ROS 2 directly:

1. Enter the container: `docker exec -it puppy_gazebo bash`
2. Source the ROS 2 workspace: `source /workspace/puppy_ros2_ws/install/setup.bash`
3. Use ROS 2 commands as needed

## Troubleshooting

If the robot doesn't appear in the simulation:
- Check that the Docker container is running (`docker ps`)
- Verify that Gazebo is running inside the container (`docker exec -it puppy_gazebo ps aux | grep gz`)
- Check the logs for any errors (`docker logs puppy_gazebo`)

## License

This project is for educational purposes.
