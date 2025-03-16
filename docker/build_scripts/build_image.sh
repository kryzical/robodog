#!/bin/bash

echo "Building Docker image for RoboDog..."
docker build -t ros1_noetic_dev .

echo "Image built successfully."
echo "You can now run the container using one of the provided scripts:"
echo "  ./run_container.sh             - Standard run with X11 forwarding"
echo "  ./run_container_headless.sh    - Headless mode (no GUI)"
echo "  ./run_container_gui.sh         - GUI mode for visualization"
