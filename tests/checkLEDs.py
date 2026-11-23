# LED CHECK - each LED in turn, then the flasher on the flashing amber.
# Part 1: each LED lights alone for 2 s, named on screen. If the wrong one lights,
#         the pins are swapped in config. If one never lights, check its wiring and
#         opto-isolator. If ALL are inverted (lit when they should be off), flip LED_ON_VALUE.
# Part 2: flashing amber driven by Flasher for 6 s at AMBER_FLASH_PERIOD_MS.
#         Count the flashes: 6 s at 500 ms = 12 flashes. Then it must go OFF.
# Part 3: everything off except the power amber, which stays on (as in main).
# Any LED whose pin is None in config is skipped.

from utime import sleep_ms, ticks_ms, ticks_diff
import config
from hardware.ledClass import LED
from behaviour.flasher import Flasher

FLASH_TEST_MS = 6000

leds = (("POWER amber", config.POWER_AMBER_LED_PIN),
        ("FLASHING amber", config.FLASHING_AMBER_LED_PIN),
        ("RED", config.RED_LED_PIN),
        ("GREEN", config.GREEN_LED_PIN))

built = {}
for name, pin in leds:
    if pin is None:
        print("SKIPPING", name, "- pin is None in config")
    else:
        built[name] = LED(pin, config.LED_ON_VALUE)


def allOff():
    for led in built.values():
        led.off()


def run():
    print("LED_ON_VALUE =", config.LED_ON_VALUE)
    print("All LEDs should be OFF now (2 s)")
    allOff()
    sleep_ms(2000)

    print("--- Part 1: one at a time ---")
    for name, pin in leds:
        if name in built:
            print(name, "ON  (pin", pin, ")")
            built[name].on()
            sleep_ms(2000)
            built[name].off()
            sleep_ms(500)

    if "FLASHING amber" not in built:
        print("No flashing amber pin - skipping Part 2")
        return
    flashingLed = built["FLASHING amber"]
    print("--- Part 2: flashing amber for", FLASH_TEST_MS // 1000, "s - count the flashes ---")
    flasher = Flasher(config.AMBER_FLASH_PERIOD_MS)
    start = ticks_ms()
    flasher.start(start)
    while ticks_diff(ticks_ms(), start) < FLASH_TEST_MS:
        flashingLed.set(flasher.update(ticks_ms()))
        sleep_ms(config.LOOP_PERIOD_MS)
    flasher.stop()
    flashingLed.off()
    print("Expected", FLASH_TEST_MS // config.AMBER_FLASH_PERIOD_MS, "flashes. Flashing amber should now be OFF.")
    sleep_ms(2000)

    if "POWER amber" in built:
        print("--- Part 3: power amber ON, all others OFF ---")
        built["POWER amber"].on()
    print("Done.")


try:
    run()
except KeyboardInterrupt:
    allOff()
    print("Stopped, all LEDs off")