# Motor consistency test. WHEELS OFF THE GROUND, motor power ON.
# Runs each motor alone at a range of speeds, 3 rounds, so you can see whether
# a motor's behaviour is repeatable (threshold problem) or random (loose wire / binding).
# Write down for each line: turns / doesn't / stutters.

from utime import sleep_ms
import config
from hardware.motorClass import Motor

SPEEDS = (20, 30, 40, 50, 70, 100)
ROUNDS = 3
RUN_MS = 2000

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN,
                  config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN,
                   config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)

try:
    print("Starting in 3 s - wheels off the ground!")
    sleep_ms(3000)
    for roundNum in range(1, ROUNDS + 1):
        for name, motor in (("RIGHT", rightMotor), ("LEFT", leftMotor)):
            for speed in SPEEDS:
                print("round %d  %-5s speed %3d" % (roundNum, name, speed))
                motor.forward(speed)
                sleep_ms(RUN_MS)
                motor.off()
                sleep_ms(700)
    print("Done.")
finally:
    leftMotor.off()
    rightMotor.off()
    print("Motors stopped")