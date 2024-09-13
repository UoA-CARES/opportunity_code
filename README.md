# Opportunity Rover Project
This repository houses the opportunity rover control code.

## Installation
Follow the installation instructions for the [CARES General Library](https://github.com/UoA-CARES/cares_lib)

Install additional python dependencies
```
cd opportunity_code
pip install -r requirements.txt
```

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

