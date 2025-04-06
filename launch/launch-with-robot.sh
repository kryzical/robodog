#!/bin/bash

# Script to run inside Docker container to launch Gazebo and spawn robot

# Source ROS
source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash 2>/dev/null || echo 'Warning: Could not source workspace'

# Start Gazebo with default empty world
echo 'Starting Gazebo with empty world...'
gz sim -v 4 empty.sdf &
sleep 5

# Create links to help find meshes if needed
echo 'Setting up mesh paths...'
if [ -d '/workspace/src/puppy_description/meshes' ]; then
  echo 'Found mesh directory, creating links...'
  mkdir -p /tmp/puppybot_models/meshes
  mkdir -p /workspace/models/puppybot/meshes
  ln -sf /workspace/src/puppy_description/meshes/* /tmp/puppybot_models/meshes/ 2>/dev/null
  ln -sf /workspace/src/puppy_description/meshes/* /workspace/models/puppybot/meshes/ 2>/dev/null
fi

# Find and use the robot URDF/SDF if available
if [ -d '/workspace/src/puppy_description/urdf' ]; then
  echo 'Found URDF directory, attempting to use it...'
  
  # Check for the main URDF file
  if [ -f '/workspace/src/puppy_description/urdf/puppy.urdf.xacro' ]; then
    echo 'Found puppy.urdf.xacro, setting up white body color...'
    
    # Create a temporary Gazebo color override
    if [ -f '/workspace/src/puppy_description/urdf/puppy.gazebo.xacro' ]; then
      echo 'Modifying Gazebo color settings...'
      cp /workspace/src/puppy_description/urdf/puppy.gazebo.xacro /tmp/puppy.gazebo.xacro.bak
      
      # Update the Gazebo color to white for the base link
      sed -i 's/<xacro:model_color link_name="base_link"\/>/<gazebo reference="base_link"><material>Gazebo\/White<\/material><turnGravityOff>false<\/turnGravityOff><\/gazebo>/' /workspace/src/puppy_description/urdf/puppy.gazebo.xacro
    fi
    
    # Generate URDF with white body
    echo 'Generating URDF with white body...'
    sed -i 's/name="black"/name="white"/' /workspace/src/puppy_description/urdf/puppy.urdf.xacro
    xacro /workspace/src/puppy_description/urdf/puppy.urdf.xacro > /tmp/puppy.urdf
    
    # Restore original files
    if [ -f '/tmp/puppy.gazebo.xacro.bak' ]; then
      mv /tmp/puppy.gazebo.xacro.bak /workspace/src/puppy_description/urdf/puppy.gazebo.xacro
    fi
    
    # Convert URDF to SDF for Gazebo
    echo 'Converting URDF to SDF...'
    gz sdf -p /tmp/puppy.urdf > /tmp/puppy.sdf
    
    # Try to spawn the model
    echo 'Spawning robot model...'
    gz service -s /world/empty/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 5000 --req 'sdf_filename: "/tmp/puppy.sdf", name: "puppy", pose: {position: {x: 0, y: 0, z: 0.2}}'
  else
    echo 'No URDF file found, falling back to primitive model'
    
    # Create a simple robot model as fallback
    echo 'Creating simple robot model...'
    cat > /tmp/simple_puppy.sdf << EOF
<?xml version='1.0'?>
<sdf version='1.6'>
  <model name='simple_puppy'>
    <pose>0 0 0.1 0 0 0</pose>
    <link name='base'>
      <visual name='visual'>
        <geometry>
          <box>
            <size>0.3 0.15 0.05</size>
          </box>
        </geometry>
        <material>
          <ambient>1 1 1 1</ambient>
          <diffuse>1 1 1 1</diffuse>
        </material>
      </visual>
      <collision name='collision'>
        <geometry>
          <box>
            <size>0.3 0.15 0.05</size>
          </box>
        </geometry>
      </collision>
    </link>
    <link name='fl_leg'>
      <pose>0.1 0.06 -0.05 0 0 0</pose>
      <visual name='visual'>
        <geometry>
          <cylinder>
            <radius>0.01</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
        </material>
      </visual>
    </link>
    <joint name='fl_joint' type='fixed'>
      <parent>base</parent>
      <child>fl_leg</child>
    </joint>
    <link name='fr_leg'>
      <pose>0.1 -0.06 -0.05 0 0 0</pose>
      <visual name='visual'>
        <geometry>
          <cylinder>
            <radius>0.01</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
        </material>
      </visual>
    </link>
    <joint name='fr_joint' type='fixed'>
      <parent>base</parent>
      <child>fr_leg</child>
    </joint>
    <link name='bl_leg'>
      <pose>-0.1 0.06 -0.05 0 0 0</pose>
      <visual name='visual'>
        <geometry>
          <cylinder>
            <radius>0.01</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
        </material>
      </visual>
    </link>
    <joint name='bl_joint' type='fixed'>
      <parent>base</parent>
      <child>bl_leg</child>
    </joint>
    <link name='br_leg'>
      <pose>-0.1 -0.06 -0.05 0 0 0</pose>
      <visual name='visual'>
        <geometry>
          <cylinder>
            <radius>0.01</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>1 0 0 1</ambient>
          <diffuse>1 0 0 1</diffuse>
        </material>
      </visual>
    </link>
    <joint name='br_joint' type='fixed'>
      <parent>base</parent>
      <child>br_leg</child>
    </joint>
  </model>
</sdf>
EOF
    # Spawn the simple model as fallback
    echo 'Spawning simple model...'
    gz service -s /world/empty/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 5000 --req 'sdf_filename: "/tmp/simple_puppy.sdf", name: "simple_puppy", pose: {position: {x: 0, y: 0, z: 0.2}}'
  fi
else
  echo 'No robot description found. Please make sure your robot model is in the workspace.'
fi

# Keep container running
echo 'Gazebo started. Press Ctrl+C to exit.'
tail -f /dev/null 