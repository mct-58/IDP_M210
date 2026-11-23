# MAGNET CHECK - MagnetSensor class with the config values. Ctrl+C to stop.
# 1. Keep every magnet away for the first second while it calibrates.
# 2. Bring a block up to the sensor the way it will sit in the jaws, then flip it over.
# Each line: change from the no-field level in mV and mT, and what read() says.
# - Check the reading matches the block's known pole. If north/south are swapped,
#   flip MAGNET_INVERT.
# - Note the change (mV) with the block in the jaws: the dead band
#   (MAGNETIC_DEAD_BAND_MV) must be comfortably smaller than that, but bigger than
#   the change you see with no block present (motors running nearby too, if you can).

from utime import sleep_ms
import config
from hardware.magnetSensor import MagnetSensor

MV_PER_MT = 30

sensor = MagnetSensor(config.MAGNET_PIN, config.MAGNETIC_DEAD_BAND_MV, config.MAGNET_INVERT)

print("Pin", config.MAGNET_PIN, " dead band", config.MAGNETIC_DEAD_BAND_MV, "mV  invert", config.MAGNET_INVERT)
print("Calibrating - keep magnets away...")
sensor.calibrate()
print("No-field level: %.0f mV (expect about 1650)" % sensor.baseLine)

try:
    while True:
        change = sensor.rawChange()
        print("change %+6.0f mV (%+5.1f mT)   read: %s" % (change, change / MV_PER_MT, sensor.read()))
        sleep_ms(250)
except KeyboardInterrupt:
    print("Stopped")