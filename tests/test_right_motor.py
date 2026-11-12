# Right motor diagnosis. WHEELS OFF THE GROUND, motor power ON.
# Drives the right motor channel directly (no Motor class) at FULL power.
# Watch the right wheel during each test and note whether it spins.

from machine import Pin, PWM
from utime import sleep_ms

RUN_MS = 3000
pwmObjects = []


def runChannel(label, dirPinNum, pwmPinNum):
    print(label)
    print("   DIR = GP%d, PWM = GP%d, full power for %d s" % (dirPinNum, pwmPinNum, RUN_MS // 1000))
    sleep_ms(1500)
    direction = Pin(dirPinNum, Pin.OUT)
    direction.value(0)
    pwm = PWM(Pin(pwmPinNum))
    pwmObjects.append(pwm)
    pwm.freq(1000)
    pwm.duty_u16(65535)
    sleep_ms(RUN_MS)
    pwm.duty_u16(0)
    pwm.deinit()
    pwmObjects.remove(pwm)
    print("   stopped - did the RIGHT wheel spin?")
    sleep_ms(2000)


try:
    print("Starting in 3 s - wheels off the ground!")
    sleep_ms(3000)
    runChannel("TEST 1: pins as on the PicoBot sheet", 3, 2)
    runChannel("TEST 2: pins swapped", 2, 3)
    print("Done.")
    print("Test 1 spun  -> hardware fine, motor needs higher speed (stall)")
    print("Test 2 spun  -> sheet is wrong: swap RIGHT_MOTOR_DIR_PIN and RIGHT_MOTOR_PWM_PIN in config")
    print("Neither spun -> hardware: swap J37/J38 plugs and run test_motors.py steps 1-4")
finally:
    for pwm in pwmObjects:
        pwm.duty_u16(0)
    print("Motor stopped")