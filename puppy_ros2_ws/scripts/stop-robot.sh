#!/bin/bash

# Script to stop the robot simulation and clean up resources

# Move to the project root directory (assuming scripts is one level down from root)
cd "$(dirname "$0")/.." || exit

# Stop the robot simulation
echo "Stopping robot simulation..."
docker stop puppy_gazebo
docker rm puppy_gazebo

# Clean up any other containers that might be hanging around
echo "Cleaning up any other containers..."
cd docker && docker compose down 2>/dev/null
cd ..

echo "Cleanup complete!" 