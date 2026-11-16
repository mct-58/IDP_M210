# Analogue inner sensor calibration. Prints raw ADC readings (0-65535) 5 times a second.
# Hold the robot so the inner sensors are over, in turn:
#   1. the WHITE line          2. the plain BOARD (black)
#   3. the RED inside a red loading box   4. GREEN inside a green box
# Write down the typical number for each. Ctrl+C to stop.

from machine import ADC, Pin
from utime import sleep_ms

innerLeft = ADC(Pin(27))
innerRight = ADC(Pin(28))

try:
    while True:
        print("IL %5d    IR %5d" % (innerLeft.read_u16(), innerRight.read_u16()))
        sleep_ms(200)
except KeyboardInterrupt:
    print("Stopped")