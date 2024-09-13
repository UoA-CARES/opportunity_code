# Opportunity Rover Project
This repository houses the opportunity rover control code.

## Installation
Follow the installation instructions for the [CARES General Library](https://github.com/UoA-CARES/cares_lib)

Install additional python dependencies
```
cd opportunity_code
pip install -r requirements.txt
```

This repository uses an Xbox One Controller and Realsense Camera

## Getting Started

To run the entire project
```python3
# From project root
python3 main.py
```

To test components run their respective scripts
```
# Test wheels
python3 wheels_test.py

# Test Mast
python3 mast_test.py

# Test Robotic Arm
python3 arm_test.py

# Test whether servos can be controlled from background thread
python3 background_thread_control_test.py

# Test whether multiple threads can control the same servos
python3 multi_thread_servo_control_test.py

# Test face tracking => mast following, face replacement
python3 face_tracking_test.py

# Test Stationary (Display) Mode
python3 stationary_mode_test.py 
```

## Operating the Rover

All scripts use the Xbox One Controller to operate the Rover

There are **4 Operating Modes**. These are Emergency Stop, Stationary Mode, Drive Mode, and Robotic Arm Mode

To change between modes, you use the x, y, a, and b buttons. You will hear audio feedback when changing modes.
To check what mode you are currently in, press down the right analog.
![image](media/Operating%20Modes.png)

### Emergency Stop
Sends stop commands to all components of the rover. This is the default mode when running any script

### Stationary Mode
This mode is a display mode. When this mode is active, the robotic arm will maneuver to set positions at a fixed interval.
In addition, the face tracking will be operational. 
This is when the camera turns on, and does face replacement on participants in the frame. 
The mast will attempt to follow the person in front of it.

### Drive Mode
This mode allows the user to manually drive the rover. 
The right and left triggers are used to drive forward and backward respectively. 
And the left analoge stick is used to turn.
Use the right and left bumper to rotate the mast, and the right stick (up and down) to tilt the mast.

### Robotic Arm Mode
Robotic Arm mode controls the robotic arm at the front of the rover.
The dpad is used to move the arm.
The triggers are used to rotate the camera at the end of the arm.

## FAQ
**What do I do if some components don't work?**

Ensure that all the torques are enabled for the servos in dynamixel

**The arm suddenly stops working?**

There is a chance that the servos may have been overloaded. Reboot the servos.
