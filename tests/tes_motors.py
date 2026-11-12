# Motor direction + stall speed test. WHEELS OFF THE GROUND. Motor power ON.
# Watch each step and write down what happens. Ctrl+C at any time stops the motors.

from utime import sleep_ms
import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain

TEST_SPEED = 40
STEP_MS = 2000

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN,
                  config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN,
                   config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED)
driveTrain = DriveTrain(leftMotor, rightMotor)


def step(description, left, right, ms=STEP_MS):
    print(description)
    sleep_ms(1500)                      # time to read the line before it moves
    driveTrain.drive(left, right)
    sleep_ms(ms)
    driveTrain.stop()
    sleep_ms(500)


try:
    print("Starting in 3 s - wheels off the ground!")
    sleep_ms(3000)

    # Direction checks: each should roll the robot FORWARD unless it says reverse
    step("1. LEFT wheel only, forward   -> only left turns, robot-forward direction?", TEST_SPEED, 0)
    step("2. LEFT wheel only, reverse   -> opposite to step 1?", -TEST_SPEED, 0)
    step("3. RIGHT wheel only, forward  -> only right turns, robot-forward direction?", 0, TEST_SPEED)
    step("4. RIGHT wheel only, reverse  -> opposite to step 3?", 0, -TEST_SPEED)
    step("5. BOTH forward               -> both robot-forward?", TEST_SPEED, TEST_SPEED)
    step("6. Pivot right (L fwd, R rev) -> clockwise seen from above?", TEST_SPEED, -TEST_SPEED)
    step("7. Pivot left  (L rev, R fwd) -> anticlockwise seen from above?", -TEST_SPEED, TEST_SPEED)

    # Stall speed: lowest speed at which each wheel actually turns
    for name, sign in (("LEFT", (1, 0)), ("RIGHT", (0, 1))):
        print("8. Stall sweep,", name, "wheel - note the first speed where it turns")
        sleep_ms(1500)
        for speed in range(5, 45, 5):
            print("   speed", speed)
            driveTrain.drive(speed * sign[0], speed * sign[1])
            sleep_ms(1500)
        driveTrain.stop()
        sleep_ms(1000)

    print("Done.")
finally:
    driveTrain.stop()
    print("Motors stopped")