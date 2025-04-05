#!/bin/bash

# Simple script to test mesh loading in Gazebo Garden

# Make sure there are no existing containers
docker rm -f gazebo_garden 2>/dev/null || true

# Set X11 permissions
xhost +local:docker

# Start the container
echo "Starting Gazebo container..."
docker run -it --rm \
  --name gazebo_garden \
  --network host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $(pwd)/puppy_ros2_ws:/workspace:rw \
  -v /dev/dri:/dev/dri \
  -v /dev/shm:/dev/shm \
  ros2_gazebo_garden \
  bash -c "
    # Create mesh directory
    mkdir -p /workspace/models/puppybot/meshes
    
    # Copy mesh files
    cp -r /workspace/src/puppy_description/meshes/*.STL /workspace/models/puppybot/meshes/
    chmod 644 /workspace/models/puppybot/meshes/*
    
    # Create complete puppy SDF file
    cat > /tmp/puppy_model.sdf << 'EOF'
<?xml version=\"1.0\" ?>
<sdf version=\"1.6\">
  <model name=\"puppy\">
    <!-- Base link (body) -->
    <link name=\"base_link\">
      <pose>0 0 0.11 0 0 0</pose>
      <inertial>
        <mass>0.0656</mass>
        <inertia>
          <ixx>0.0001015640290354</ixx>
          <iyy>4.73014549137098E-05</iyy>
          <izz>0.000137571042581761</izz>
          <ixy>5.44665608405109E-10</ixy>
          <ixz>-5.74905560030545E-09</ixz>
          <iyz>-4.46099046853099E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/base_link.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.5 0.5 0.5 1</ambient>
          <diffuse>0.7 0.7 0.7 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/base_link.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <!-- Left Back leg parts -->
    <link name=\"lb_link1\">
      <pose>0.042 0.0778 0.126 -0.752 0 0</pose>
      <inertial>
        <mass>0.0101</mass>
        <inertia>
          <ixx>4.75129190044601E-06</ixx>
          <iyy>2.87659318790812E-06</iyy>
          <izz>2.92897619209419E-06</izz>
          <ixy>2.10473016237263E-08</ixy>
          <ixz>1.88925228411051E-08</ixz>
          <iyz>2.14913235084379E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lb_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lb_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"lb_joint1\" type=\"revolute\">
      <parent>base_link</parent>
      <child>lb_link1</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <link name=\"lb_link2\">
      <pose>0.054 0.13 0.073 -0.752 0 3.14159</pose>
      <inertial>
        <mass>0.0054</mass>
        <inertia>
          <ixx>4.05444909185018E-06</ixx>
          <iyy>1.97885521739999E-06</iyy>
          <izz>2.19064599298264E-06</izz>
          <ixy>1.22817063923314E-15</ixy>
          <ixz>5.50500791639953E-16</ixz>
          <iyz>-1.87063799891709E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lb_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lb_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"lb_joint2\" type=\"revolute\">
      <parent>lb_link1</parent>
      <child>lb_link2</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Right Back leg parts -->
    <link name=\"rb_link1\">
      <pose>-0.042 0.0778 0.126 -0.752 0 0</pose>
      <inertial>
        <mass>0.0101</mass>
        <inertia>
          <ixx>4.75129811236989E-06</ixx>
          <iyy>2.87660393694748E-06</iyy>
          <izz>2.92897914074097E-06</izz>
          <ixy>-2.1017569726548E-08</ixy>
          <ixz>-1.89306363229736E-08</ixz>
          <iyz>2.14913401997947E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rb_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rb_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"rb_joint1\" type=\"revolute\">
      <parent>base_link</parent>
      <child>rb_link1</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <link name=\"rb_link2\">
      <pose>-0.0605 0.13 0.073 -0.752 0 3.14159</pose>
      <inertial>
        <mass>0.0054</mass>
        <inertia>
          <ixx>4.05444909186485E-06</ixx>
          <iyy>1.97885521739198E-06</iyy>
          <izz>2.19064599300475E-06</izz>
          <ixy>1.22890997212443E-15</ixy>
          <ixz>5.5049632107985E-16</ixz>
          <iyz>-1.87063799892702E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rb_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rb_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"rb_joint2\" type=\"revolute\">
      <parent>rb_link1</parent>
      <child>rb_link2</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Left Front leg parts -->
    <link name=\"lf_link1\">
      <pose>0.042 -0.0778 0.121 -0.752 0 0</pose>
      <inertial>
        <mass>0.0101</mass>
        <inertia>
          <ixx>4.75131109114716E-06</ixx>
          <iyy>2.87660804474965E-06</iyy>
          <izz>2.92898830803666E-06</izz>
          <ixy>2.10480769743655E-08</ixy>
          <ixz>1.88912920202068E-08</ixz>
          <iyz>2.14914102954077E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lf_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lf_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"lf_joint1\" type=\"revolute\">
      <parent>base_link</parent>
      <child>lf_link1</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <link name=\"lf_link2\">
      <pose>0.054 -0.13 0.068 -0.752 0 3.14159</pose>
      <inertial>
        <mass>0.0054</mass>
        <inertia>
          <ixx>0.0001</ixx>
          <iyy>0.0001</iyy>
          <izz>0.0001</izz>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyz>0</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lf_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/lf_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"lf_joint2\" type=\"revolute\">
      <parent>lf_link1</parent>
      <child>lf_link2</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Right Front leg parts -->
    <link name=\"rf_link1\">
      <pose>-0.042 -0.0778 0.121 -0.752 0 0</pose>
      <inertial>
        <mass>0.0101</mass>
        <inertia>
          <ixx>4.75129811233804E-06</ixx>
          <iyy>2.87660393692374E-06</iyy>
          <izz>2.9289791407718E-06</izz>
          <ixy>-2.1017569770552E-08</ixy>
          <ixz>-1.89306363663801E-08</ixz>
          <iyz>2.14913401996578E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rf_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rf_link1.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"rf_joint1\" type=\"revolute\">
      <parent>base_link</parent>
      <child>rf_link1</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <link name=\"rf_link2\">
      <pose>-0.0605 -0.13 0.068 -0.752 0 3.14159</pose>
      <inertial>
        <mass>0.0054</mass>
        <inertia>
          <ixx>4.05444909185018E-06</ixx>
          <iyy>1.97885521739999E-06</iyy>
          <izz>2.19064599298264E-06</izz>
          <ixy>1.22817063923314E-15</ixy>
          <ixz>5.50500791639953E-16</ixz>
          <iyz>-1.87063799891709E-06</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rf_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/rf_link2.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"rf_joint2\" type=\"revolute\">
      <parent>rf_link1</parent>
      <child>rf_link2</child>
      <axis>
        <xyz>1 0 0</xyz>
        <limit>
          <lower>-2</lower>
          <upper>2</upper>
        </limit>
      </axis>
    </joint>
    
    <!-- Camera link -->
    <link name=\"camera_link\">
      <pose>0 -0.101 0.127 0.0342 0 0</pose>
      <inertial>
        <mass>0.01</mass>
        <inertia>
          <ixx>0.00001</ixx>
          <iyy>0.00001</iyy>
          <izz>0.00001</izz>
          <ixy>0</ixy>
          <ixz>0</ixz>
          <iyz>0</iyz>
        </inertia>
      </inertial>
      <visual name=\"visual\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/camera_link.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0 0 0 1</ambient>
          <diffuse>0 0 0 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <collision name=\"collision\">
        <geometry>
          <mesh>
            <uri>file:///workspace/models/puppybot/meshes/camera_link.STL</uri>
            <scale>1 1 1</scale>
          </mesh>
        </geometry>
      </collision>
    </link>
    
    <joint name=\"camera_joint\" type=\"fixed\">
      <parent>base_link</parent>
      <child>camera_link</child>
    </joint>
  </model>
</sdf>
EOF

    # Start Gazebo and spawn the model
    echo 'Starting Gazebo with the puppy model...'
    source /opt/ros/humble/setup.bash
    
    # Run Gazebo with empty world
    gz sim -r empty.sdf --headless-rendering false -p &
    sleep 5
    
    # Spawn the puppy model
    echo 'Spawning puppy model...'
    gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory --reptype ignition.msgs.Boolean --timeout 1000 --req 'sdf_filename: \"/tmp/puppy_model.sdf\", name: \"puppy\", pose: {position: {x: 0, y: 0, z: 0.5}}'
    
    # Keep the container running
    echo 'Puppy model spawned. Press Ctrl+C to exit.'
    tail -f /dev/null
  " 