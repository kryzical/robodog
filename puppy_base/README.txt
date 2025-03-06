PUPPY_BASE PACKAGE
================

This package contains the core control and operation functionality for the puppy robot:

Key Components:
- Core robot controllers and hardware interfaces
- State estimation and sensor fusion
- Movement primitives and gait controllers
- Hardware abstraction layer

Key Files:
- unified_controller.py: Main controller handling both physical and simulation control
- unified_sim.py: Simulation-specific control implementation
- unified_nonsim.py: Physical hardware control implementation
- walking.py: Walking gait implementations
- stand_up.py: Stand-up behavior implementation

Directories:
/config - Configuration files for EKF and velocity smoothing
/include - C++ header files for core functionality
/launch - Launch files for different control scenarios
/scripts - Python implementations of robot behaviors
/src - C++ implementations of core functionality

Dependencies:
- ROS Control
- Robot State Publisher
- Joint State Publisher
- TF2
- Navigation Stack Integration