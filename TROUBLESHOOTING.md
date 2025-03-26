# Troubleshooting Guide

This guide documents common issues encountered during setup and operation of the PuppyPi simulation, along with their solutions.

## Controller Manager Issues

### Symptom: Controller Spawner Fails
```
[WARN] Controller Spawner couldn't find the expected controller_manager ROS interface.
```

#### Solution
1. Ensure proper initialization order in the launch file:
   ```xml
   <!-- Initialize controller manager first -->
   <node name="controller_manager" pkg="controller_manager" type="controller_manager" respawn="false" output="screen" ns="puppy"/>
   
   <!-- Then spawn controllers -->
   <node name="controller_spawner" pkg="controller_manager" type="spawner" ... ns="puppy"/>
   ```

2. Check namespace configuration:
   - Controller configuration should be loaded with namespace: `ns="puppy"`
   - Controller manager and spawner should use the same namespace
   - Remove any top-level namespace from the YAML file if using `ns` in the launch file

3. Verify package installation:
   ```bash
   sudo apt-get install ros-noetic-effort-controllers
   ```

## Virtual Joystick Issues

### Symptom: Joystick Not Responding
The virtual joystick GUI appears but doesn't control the robot.

#### Solution
1. Check topic names:
   - Virtual joystick publishes to `/joy`
   - Joypad controller should subscribe to `/joy` (with leading slash)
   - Verify using `rostopic list` and `rostopic echo /joy`

2. Verify button mappings:
   - Check that button indices match between virtual joystick and controller
   - Default mappings:
     - Forward: Button 4
     - Backward: Button 6
     - Left: Button 7
     - Right: Button 5
     - Stop: Button 2

3. Check velocity commands:
   ```bash
   rostopic echo /cmd_vel
   ```
   Should show non-zero values when buttons are pressed.

## Gazebo Issues

### Symptom: Robot Not Spawning
The Gazebo window opens but the robot model doesn't appear.

#### Solution
1. Check model deletion:
   ```xml
   <node if="$(arg delete_model)" pkg="rosservice" type="rosservice" name="delete_model" 
         args="call /gazebo/delete_model '{model_name: puppy}'" 
         launch-prefix="bash -c 'sleep 2.0; $0 $@'" />
   ```
   - The sleep delay ensures Gazebo is ready
   - The `if="$(arg delete_model)"` allows skipping deletion if needed

2. Verify URDF loading:
   ```xml
   <param name="robot_description" command="$(find xacro)/xacro $(find puppy_description)/urdf/puppy.urdf.xacro"/>
   ```
   - Check that the URDF file exists and is valid
   - Try loading it manually: `rosrun xacro xacro puppy.urdf.xacro`

3. Check spawn position:
   ```xml
   <node name="urdf_spawner" pkg="gazebo_ros" type="spawn_model" 
         args="-urdf -model puppy -param robot_description -z 0.15 ..."
   ```
   - The z=0.15 ensures the robot spawns above the ground
   - Initial joint positions should be set for standing pose

## Joint State Issues

### Symptom: Joint States Not Publishing
The robot appears in Gazebo but joint states aren't being published.

#### Solution
1. Check joint state publisher configuration:
   ```xml
   <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher">
     <param name="/use_gui" value="false"/> 
     <param name="publish_rate" value="100"/>
     <rosparam param="/source_list">[/puppy/joint_states]</rosparam>
   </node>
   ```

2. Verify robot state publisher:
   ```xml
   <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher">
     <remap from="/joint_states" to="/puppy/joint_states" />
   </node>
   ```

3. Check topics:
   ```bash
   rostopic list | grep joint
   rostopic echo /puppy/joint_states
   ```

## General Tips

1. **Launch File Order**
   - Always ensure proper initialization order
   - Use `launch-prefix="bash -c 'sleep X; $0 $@'"` for timing-sensitive nodes
   - Group related nodes together

2. **Namespace Management**
   - Be consistent with namespace usage
   - Avoid double namespacing
   - Use remaps when needed

3. **Debugging Tools**
   - Use `rqt_graph` to visualize node connections
   - Use `rqt_console` to view logs
   - Use `rostopic list` and `rostopic echo` to check topics
   - Use `rosnode list` and `rosnode info` to check nodes

4. **Common Commands**
   ```bash
   # List all topics
   rostopic list
   
   # Check node connections
   rqt_graph
   
   # View logs
   rqt_console
   
   # Check node status
   rosnode list
   rosnode info /node_name
   
   # Monitor topics
   rostopic echo /topic_name
   ``` 