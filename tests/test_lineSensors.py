# Live line sensor check: move the robot by hand and watch the output.
# Prints only when something changes. Ctrl+C to stop.
#
# Order everywhere: (outer left, inner left, inner right, outer right)
#   raw    = what each pin actually reads (0/1) -> use this to set LINE_DETECTED_VALUE
#   onLine = what LineSensors.read() reports, using LINE_DETECTED_VALUE from config

from utime import sleep_ms
import config
from hardware.lineSensorsClass import LineSensors

pinNums = (config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN,
           config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN)

if None in pinNums:
    raise ValueError("Fill in the four LINE_*_PIN values in config.py first: " + str(pinNums))

sensors = LineSensors(*pinNums, config.LINE_DETECTED_VALUE)
pins = (sensors.olPin, sensors.ilPin, sensors.irPin, sensors.orPin)

print("Pins (OL, IL, IR, OR):", pinNums, " LINE_DETECTED_VALUE =", config.LINE_DETECTED_VALUE)

last = None
try:
    while True:
        raw = tuple(p.value() for p in pins)
        if raw != last:
            print("raw", raw, "  onLine", sensors.read())
            last = raw
        sleep_ms(20)
except KeyboardInterrupt:
    print("Stopped")