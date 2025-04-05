#!/bin/bash

# Script to spawn test models in the running Gazebo simulation

# Make sure the container is running
if ! docker ps | grep -q gazebo_garden; then
  echo "Error: gazebo_garden container is not running. Please start it with ./scripts/run.sh"
  exit 1
fi

# Select which model to spawn
if [ "$1" == "box" ] || [ "$1" == "" ]; then
  echo "Spawning red box model..."
  MODEL="box.sdf"
  NAME="red_box"
  POSITION="x: 0, y: 0, z: 0.5"
elif [ "$1" == "mesh" ]; then
  echo "Spawning mesh model..."
  MODEL="mesh.sdf"
  NAME="mesh_model"
  POSITION="x: 0, y: 0, z: 0"
elif [ "$1" == "debug" ]; then
  echo "Creating a debugging mesh model with different scales..."
  # Create a debug model with multiple scales
  docker exec -it gazebo_garden bash -c "
    mkdir -p /tmp/debug_meshes
    cat > /tmp/debug_model.sdf << EOF
<?xml version=\"1.0\" ?>
<sdf version=\"1.6\">
  <model name=\"debug_mesh_model\">
    <link name=\"link1\">
      <pose>0 0 0 0 0 0</pose>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///tmp/puppybot_models/meshes/base_link.STL</uri>
            <scale>0.001 0.001 0.001</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>
EOF
  "
  echo "Spawning debug mesh model..."
  docker exec -it gazebo_garden bash -c "
    source /opt/ros/humble/setup.bash && \
    gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory \
    --reptype ignition.msgs.Boolean --timeout 1000 \
    --req 'sdf_filename: \"/tmp/debug_model.sdf\", name: \"debug_mesh\", pose: {position: {x: 0, y: 0, z: 0}}'
  "
  echo "Debug model spawned. Check the Gazebo window."
  exit 0
elif [ "$1" == "primitive" ]; then
  # Create and spawn a primitive sphere model for testing
  echo "Creating and spawning a primitive model (sphere)..."
  docker exec -it gazebo_garden bash -c "
    cat > /tmp/sphere.sdf << EOF
<?xml version=\"1.0\" ?>
<sdf version=\"1.6\">
  <model name=\"test_sphere\">
    <link name=\"link\">
      <visual name=\"visual\">
        <geometry>
          <sphere>
            <radius>0.5</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0 1 0 1</ambient>
          <diffuse>0 1 0 1</diffuse>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <sphere>
            <radius>0.5</radius>
          </sphere>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
EOF

    source /opt/ros/humble/setup.bash && \
    gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory \
    --reptype ignition.msgs.Boolean --timeout 1000 \
    --req 'sdf_filename: \"/tmp/sphere.sdf\", name: \"test_sphere\", pose: {position: {x: 0, y: 0, z: 0.5}}'
  "
  echo "Primitive sphere model spawned. Check the Gazebo window."
  exit 0
else
  echo "Unknown model: $1"
  echo "Usage: ./scripts/spawn.sh [box|mesh|debug|primitive]"
  exit 1
fi

# Spawn the model
docker exec -it gazebo_garden bash -c "source /opt/ros/humble/setup.bash && \
  export GZ_SIM_RESOURCE_PATH=/workspace/src:/workspace/models:/tmp/puppybot_models && \
  export IGN_GAZEBO_RESOURCE_PATH=/workspace/src:/workspace/models:/tmp/puppybot_models && \
  gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory \
  --reptype ignition.msgs.Boolean --timeout 1000 \
  --req 'sdf_filename: \"/tmp/$MODEL\", name: \"$NAME\", pose: {position: {$POSITION}}'" 