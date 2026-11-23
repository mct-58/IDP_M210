# BUTTON CHECK - raw pin state and debounced presses. Ctrl+C to stop.
# Prints every raw change (bounces included) and every debounced press.
# - Press and release normally: raw may flicker several times, but "PRESS" must
#   appear exactly ONCE per press, and never on release.
# - Hold it down for a few seconds: still only one PRESS.
# - If raw never changes, check wiring and START_BUTTON_PIN.
# - If raw reads True when NOT pressed, BUTTON_PRESSED_VALUE is the wrong way round.

from utime import sleep_ms, ticks_ms
import config
from hardware.startButton import Button
from behaviour.buttonPress import ButtonPress

if config.START_BUTTON_PIN is None:
    raise ValueError("START_BUTTON_PIN is None in config")

button = Button(config.START_BUTTON_PIN, config.BUTTON_PRESSED_VALUE)
buttonPress = ButtonPress(config.BUTTON_DEBOUNCE_MS)

print("Pin", config.START_BUTTON_PIN, " pressed value", config.BUTTON_PRESSED_VALUE,
      " debounce", config.BUTTON_DEBOUNCE_MS, "ms")
print("Raw state now:", button.read(), "(should be False if not pressed)")

lastRaw = None
presses = 0
start = ticks_ms()
try:
    while True:
        now = ticks_ms()
        raw = button.read()
        if raw != lastRaw:
            print("  raw", raw, " at", now - start, "ms")
            lastRaw = raw
        if buttonPress.update(raw, now):
            presses += 1
            print("PRESS", presses)
        sleep_ms(config.LOOP_PERIOD_MS)
except KeyboardInterrupt:
    print("Stopped after", presses, "presses")