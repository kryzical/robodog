PUPPY_MSGS PACKAGE
=================

Custom ROS message definitions for the puppy robot:

Message Types:
- Contacts.msg - Contact state information
- ContactsStamped.msg - Time-stamped contact states
- Joints.msg - Joint state information
- Point.msg - Custom point representation
- PointArray.msg - Array of points
- Pose.msg - Robot pose information
- Velocities.msg - Robot velocity states

Purpose:
- Defines custom message types used across packages
- Enables standardized communication between nodes
- Provides robot-specific data structures

Dependencies:
- Standard ROS message types (std_msgs, geometry_msgs, sensor_msgs)
- message_generation for build
- message_runtime for execution