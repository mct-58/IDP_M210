# MOTOR CHECK - direction, ramp and stall. WHEELS OFF THE GROUND, motor power ON.
# Ctrl+C at any time stops both motors.
#
# Part 1 - direction: every "forward" line must turn that wheel so the robot would
#          drive FORWARD. If a wheel turns backwards, flip its *_MOTOR_REVERSED in config.
#          If the WRONG wheel turns, the left/right pins are swapped in config.
# Part 2 - ramp: each wheel 0 -> 100 -> 0 in steps. Speed should rise and fall smoothly.
#          The first step jumps straight to the stall speed (dead-band compensation) - expected.
#          A wheel that stutters, stops mid-ramp or sounds rough points to wiring or binding.
# Part 3 - stall sweep: note the lowest speed where each wheel turns reliably from rest.
#          Motor already compensates for *_MOTOR_MIN_SPEED, so with good config values
#          even speed 5 should turn the wheel. If not, raise *_MOTOR_MIN_SPEED.

from utime import sleep_ms
import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain

TEST_SPEED = 40
STEP_MS = 2000
RAMP_STEP = 5
RAMP_STEP_MS = 150

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ,
                  config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ,
                   config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)
driveTrain = DriveTrain(leftMotor, rightMotor)


def step(description, left, right, ms=STEP_MS):
    print(description)
    sleep_ms(1500)
    driveTrain.drive(left, right)
    sleep_ms(ms)
    driveTrain.stop()
    sleep_ms(500)


def ramp(name, leftSign, rightSign):
    print("RAMP", name, "- watch for smooth speed-up and slow-down")
    sleep_ms(1500)
    speeds = list(range(0, 101, RAMP_STEP)) + list(range(100 - RAMP_STEP, -1, -RAMP_STEP))
    for speed in speeds:
        print("   speed", speed)
        driveTrain.drive(speed * leftSign, speed * rightSign)
        sleep_ms(RAMP_STEP_MS)
    driveTrain.stop()
    sleep_ms(1000)


def run():
    print("Config: left reversed =", config.LEFT_MOTOR_REVERSED, " right reversed =", config.RIGHT_MOTOR_REVERSED)
    print("Starting in 3 s - wheels off the ground!")
    sleep_ms(3000)

    print("--- Part 1: direction ---")
    step("1. LEFT forward   -> only the left wheel, robot-forward direction?", TEST_SPEED, 0)
    step("2. LEFT reverse   -> left wheel, opposite to 1?", -TEST_SPEED, 0)
    step("3. RIGHT forward  -> only the right wheel, robot-forward direction?", 0, TEST_SPEED)
    step("4. RIGHT reverse  -> right wheel, opposite to 3?", 0, -TEST_SPEED)
    step("5. BOTH forward   -> both robot-forward?", TEST_SPEED, TEST_SPEED)
    step("6. Pivot right    -> clockwise seen from above?", TEST_SPEED, -TEST_SPEED)
    step("7. Pivot left     -> anticlockwise seen from above?", -TEST_SPEED, TEST_SPEED)

    print("--- Part 2: ramp ---")
    ramp("LEFT forward", 1, 0)
    ramp("RIGHT forward", 0, 1)
    ramp("BOTH forward", 1, 1)
    ramp("BOTH reverse", -1, -1)

    print("--- Part 3: stall sweep ---")
    for name, signs in (("LEFT", (1, 0)), ("RIGHT", (0, 1))):
        print("Stall sweep", name, "- note the first speed where it turns")
        sleep_ms(1500)
        for speed in range(5, 45, 5):
            print("   speed", speed)
            driveTrain.drive(speed * signs[0], speed * signs[1])
            sleep_ms(1500)
            driveTrain.stop()
            sleep_ms(500)

    print("Done.")


try:
    run()
finally:
    driveTrain.stop()
    print("Motors stopped")