from evdev import InputDevice, categorize, ecodes
import threading
import time
import math

class XboxController(object):
    MAX_TRIG_VAL = 1023  # The maximum value for triggers
    MAX_JOY_VAL = 65535  # The maximum value for joysticks

    def __init__(self, device_path):
        self.device = InputDevice(device_path)
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=()
        )
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):  # return the buttons/triggers that you care about in this method
        # Wheels
        left_joy_x = self.LeftJoystickX
        right_trigger = self.RightTrigger
        left_trigger = self.LeftTrigger

        wheels_inputs = [left_joy_x, right_trigger, left_trigger]

        # Operating Mode
        Y_button = self.Y
        B_button = self.B
        A_button = self.A
        X_button = self.X

        operating_mode_inputs = [Y_button, B_button, A_button, X_button]

        # Check Mode
        right_thumb = self.RightThumb

        check_mode = [right_thumb]

        # Mast
        right_bumper = self.RightBumper
        left_bumper = self.LeftBumper
        right_joy_y = self.RightJoystickY

        mast_inputs = [right_bumper, left_bumper, right_joy_y]

        input_dict = {"wheels": wheels_inputs, "operating_mode": operating_mode_inputs, "check_mode": check_mode, "mast": mast_inputs}
        return input_dict

    def _monitor_controller(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_ABS:
                abs_event = categorize(event)
                if abs_event.event.code == ecodes.ABS_Y:
                    self.LeftJoystickY = abs_event.event.value / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif abs_event.event.code == ecodes.ABS_X:
                    self.LeftJoystickX = abs_event.event.value / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif abs_event.event.code == ecodes.ABS_RZ:
                    self.RightJoystickY = abs_event.event.value / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif abs_event.event.code == ecodes.ABS_Z:
                    self.RightJoystickX = abs_event.event.value / XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif abs_event.event.code == ecodes.ABS_BRAKE:
                    self.LeftTrigger = abs_event.event.value / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
                elif abs_event.event.code == ecodes.ABS_GAS:
                    self.RightTrigger = abs_event.event.value / XboxController.MAX_TRIG_VAL  # normalize between 0 and 1
            elif event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.event.code == ecodes.BTN_TL:
                    self.LeftBumper = key_event.event.value
                elif key_event.event.code == ecodes.BTN_TR:
                    self.RightBumper = key_event.event.value
                elif key_event.event.code == ecodes.BTN_SOUTH:
                    self.A = key_event.event.value
                elif key_event.event.code == ecodes.BTN_NORTH:
                    self.Y = key_event.event.value
                elif key_event.event.code == ecodes.BTN_WEST:
                    self.X = key_event.event.value
                elif key_event.event.code == ecodes.BTN_EAST:
                    self.B = key_event.event.value
                elif key_event.event.code == ecodes.BTN_THUMBL:
                    self.LeftThumb = key_event.event.value
                elif key_event.event.code == ecodes.BTN_THUMBR:
                    self.RightThumb = key_event.event.value
                elif key_event.event.code == ecodes.BTN_SELECT:
                    self.Back = key_event.event.value
                elif key_event.event.code == ecodes.BTN_START:
                    self.Start = key_event.event.value
                elif key_event.event.code == ecodes.BTN_TRIGGER_HAPPY1:
                    self.LeftDPad = key_event.event.value
                elif key_event.event.code == ecodes.BTN_TRIGGER_HAPPY2:
                    self.RightDPad = key_event.event.value
                elif key_event.event.code == ecodes.BTN_TRIGGER_HAPPY3:
                    self.UpDPad = key_event.event.value
                elif key_event.event.code == ecodes.BTN_TRIGGER_HAPPY4:
                    self.DownDPad = key_event.event.value
            time.sleep(0.01)

if __name__ == "__main__":
    # Replace '/dev/input/eventX' with the actual device path for your Xbox controller
    device_path = '/dev/input/event11'
    joy = XboxController(device_path)
    while True:
        print(joy.read())
