# Magnetic sensor (DRV5055A2) test. Ctrl+C to stop.
# Wiring: VCC -> 3.3 V (NOT 5 V), GND -> GND, OUT -> GP26 (Pico pin 31).
# 1. Keep magnets away for the first 2 s while it measures the no-field level.
# 2. Then bring a block's magnet up to the sensor's marked face, one side, then flip it.
# Prints: raw ADC value, voltage, change from no-field level (mV and mT), and N/S/- guess.

from machine import ADC, Pin
from utime import sleep_ms

PIN = 26
THRESHOLD_MV = 60          # dead-band either side of the no-field level (= 2 mT); tune
MV_PER_MT = 30             # DRV5055A2 sensitivity at 3.3 V

adc = ADC(Pin(PIN))

def millivolts():
    return adc.read_u16() * 3300 / 65535

print("Measuring no-field level - keep magnets away...")
total = 0
for _ in range(100):
    total += millivolts()
    sleep_ms(20)
baseline = total / 100
print("No-field level: %.0f mV (expect about 1650)" % baseline)

try:
    while True:
        mv = millivolts()
        delta = mv - baseline
        if delta > THRESHOLD_MV:
            pole = "SOUTH"
        elif delta < -THRESHOLD_MV:
            pole = "NORTH"
        else:
            pole = "-"
        print("raw %5d   %4.0f mV   change %+5.0f mV  (%+5.1f mT)   %s"
              % (adc.read_u16(), mv, delta, delta / MV_PER_MT, pole))
        sleep_ms(200)
except KeyboardInterrupt:
    print("Stopped")