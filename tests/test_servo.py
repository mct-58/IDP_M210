from utime import sleep_ms
import config
import Hardware.servoClass as sc
import Hardware.gripperClass as gp

SERVO_PIN = 15
GRIP_ANGLE = 73
RELEASE_ANGLE = 53
HOLD_MS = 1500
CYCLES = 3

if SERVO_PIN is None:
    raise ValueError("invalid servo pin")

print("Servo test")

servo = sc.Servo(SERVO_PIN, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE)


gripper = gp.Grip(servo, GRIP_ANGLE, RELEASE_ANGLE)

print("Objects made")

try:
    print("Servo test starting in 3 s. Check that the gripper can move freely.")
    sleep_ms(3000)

    for cycle in range(1, CYCLES + 1):
        print("Cycle %d: release (%d degrees)" % (cycle, RELEASE_ANGLE))
        gripper.release()
        sleep_ms(HOLD_MS)

        print("Cycle %d: grip (%d degrees)" % (cycle, GRIP_ANGLE))
        gripper.grip()
        sleep_ms(HOLD_MS)

    print("Servo test complete.")
finally:
    servo.off()
    print("Servo PWM turned off.")
