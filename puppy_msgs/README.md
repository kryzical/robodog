# Puppy Messages Package

This package defines custom message and service types used for communication between different nodes in the puppy robot system.

## Structure

- **msg/**: Custom ROS message definitions
  - Contains message types for robot state, commands, and sensor data

## Usage

To use these messages in another package, add the following to your `package.xml`:
```xml
<depend>puppy_msgs</depend>
```

And to your `CMakeLists.txt`:
```cmake
find_package(catkin REQUIRED COMPONENTS
  puppy_msgs
  # other dependencies
)
```

Then include the messages in your code:
```cpp
#include <puppy_msgs/YourMessageType.h>
```

Or in Python:
```python
from puppy_msgs.msg import YourMessageType
```