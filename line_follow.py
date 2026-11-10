from machine import Pin, PWM
from utime import sleep
import config, motorClass

motor1 = Motor(Pin(0), Pin(1))
start = time.ticks_ms() # get millisecond counter
delta = time.ticks_diff(time.ticks_ms(), start)
while delta < 1000:
    motor1.forward(50)
    delta = time.ticks_diff(time.ticks_ms(), start)




 # Pin 18 = GP18 (labelled 24 on the jumper)


while True:
    light_1 = Pin(18, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    light_2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
    light_3 = Pin(20, Pin.IN, Pin.PULL_DOWN)
    light_4 = Pin(21, Pin.IN, Pin.PULL_DOWN)
    ref_value = 10
    
