## Capture touch screen position for an Android device connected over USB
## Require ADB to be installed
import subprocess

def get_touch_position():
    # Execute adb command to get touch events
    process = subprocess.Popen(["adb", "shell", "getevent", "-tl", "/dev/input/event1"], stdout=subprocess.PIPE)
    x, y = None, None
    while True:
        line = process.stdout.readline().decode()
        if not line:
            break
        if "ABS_MT_POSITION_X" in line:
            x = int(line.split()[-1], 16)  # Convert hex to int
        if "ABS_MT_POSITION_Y" in line:
            y = int(line.split()[-1], 16)  # Convert hex to int
        if x is not None and y is not None:
            print(x, y)
            x, y = None, None  # Reset coordinates for the next touch

get_touch_position()


