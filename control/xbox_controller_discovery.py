import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:
   print(devices)
   print(device.path, device.name, device.phys)