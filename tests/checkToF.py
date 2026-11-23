# TOF CHECK - both distance sensors through the ToF class. Ctrl+C to stop.
# Once a second, per sensor: how many new readings arrived, and the latest distance
# (after the config offset) or "out of range".
# - Expect roughly 25-35 new readings per second per sensor. Far fewer means the
#   non-blocking read isn't working and the loop is being held up.
# - Wave a hand in front of each sensor: front must change for the front sensor,
#   back for the back one. If they're swapped, swap the TOF_FRONT_* / TOF_BACK_* config.
# - Hold a ruler: reading vs true distance gives the offset for TOF_*_OFFSET_MM.
# - A sensor that isn't wired is reported and skipped; the other still runs.
# - If constructing a sensor fails, check its wiring and that bus and pins match
#   (I2C0: GP8/9, I2C1: GP10/11).

from utime import sleep_ms, ticks_ms, ticks_diff
import config
from hardware.tof import ToF



def build(name, bus, sda, scl, offset):
    print("Building", name, "sensor (bus", bus, " SDA", sda, " SCL", scl, ")...")
    try:
        sensor = ToF(bus, sda, scl, offset)
        print(name, "OK")
        return sensor
    except Exception as e:
        print(name, "FAILED - not wired, or bus/pins don't match:", e)
        return None


front = build("FRONT", config.TOF_FRONT_BUS, config.TOF_FRONT_SDA_PIN, config.TOF_FRONT_SCL_PIN, config.TOF_FRONT_OFFSET_MM)
back = build("BACK", config.TOF_BACK_BUS, config.TOF_BACK_SDA_PIN, config.TOF_BACK_SCL_PIN, config.TOF_BACK_OFFSET_MM)
if front is None and back is None:
    raise SystemExit("No distance sensors working")


def describe(sensor):
    if sensor is None:
        return "not connected"
    if sensor.latestReading is None:
        return "out of range"
    return str(sensor.latestReading) + " mm"


frontCount = 0
backCount = 0
lastPrint = ticks_ms()
try:
    while True:
        now = ticks_ms()
        if front is not None and front.update():
            frontCount += 1
        if back is not None and back.update():
            backCount += 1
        if ticks_diff(now, lastPrint) >= 1000:
            print("FRONT %2d/s  %-14s   BACK %2d/s  %s" % (frontCount, describe(front), backCount, describe(back)))
            frontCount = 0
            backCount = 0
            lastPrint = now
        sleep_ms(config.LOOP_PERIOD_MS)
except KeyboardInterrupt:
    print("Stopped")