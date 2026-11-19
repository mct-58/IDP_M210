from utime import sleep_ms
from machine import PIN
import Hardware.ledClass as led

pin = None # insert actual LED PIN: 12, 14
test_led = led(pin, 1) # check whether 1 is actually 'onValue'
for i in range(0, 1000):
    test_led.on()
    is_on = led.isOn()
    print(is_on)
    sleep_ms(10)
    test_led.off()
    is_on = led.isOn()
    print(is_on)
    sleep_ms(10)

sleep_ms(5000)
led.set(True)
sleep_ms(1000)
led.set(False)
