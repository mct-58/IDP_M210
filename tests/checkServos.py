# SERVO CHECK - gripper and lifter, using the angles in config.
# Prop the robot up so the lifter can go fully down without hitting the table.
# Ctrl+C at any time turns both servo signals off.
#
# Part 1 - gripper: open/close 3 times. Check it opens wide enough for a 60 mm block
#          and closes firmly on a 40 mm one (try both by hand-holding a block in the jaws).
#          If GRIP and LIFT move the wrong mechanism, swap GRIP_SERVO_PIN / LIFT_SERVO_PIN.
# Part 2 - lifter: down/up 3 times. Down must put a block on the floor; up must lift it
#          clear but keep it within 30 mm of the ground. Listen for buzzing at either end:
#          a servo buzzing while still means it is pushing against a hard stop - back
#          the angle off a few degrees.
# Part 3 - sweeps: each servo walks across its MIN..MAX range in 5 degree steps, printing
#          the angle. Use it to find the real open/closed/up/down angles for config.
#          It never goes outside GRIP_/LIFT_MIN_ANGLE..MAX_ANGLE.

from utime import sleep_ms
import config
from hardware.servoClass import Servo
from hardware.gripperClass import Grip
from hardware.lifterClass import Lift

HOLD_MS = 1500
CYCLES = 3
SWEEP_STEP = 5
SWEEP_STEP_MS = 400

gripServo = Servo(config.GRIP_SERVO_PIN, config.GRIP_MIN_ANGLE, config.GRIP_MAX_ANGLE)
liftServo = Servo(config.LIFT_SERVO_PIN, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE)
gripper = Grip(gripServo, config.GRIP_CLOSED_ANGLE, config.GRIP_OPEN_ANGLE)
lifter = Lift(liftServo, config.LIFT_UP_ANGLE, config.LIFT_DOWN_ANGLE)


def sweep(name, servo, low, high):
    print("SWEEP", name, "from", low, "to", high)
    sleep_ms(1000)
    for angle in list(range(low, high + 1, SWEEP_STEP)) + list(range(high, low - 1, -SWEEP_STEP)):
        print("   angle", angle)
        servo.setAngle(angle)
        sleep_ms(SWEEP_STEP_MS)


def run():
    print("Grip pin", config.GRIP_SERVO_PIN, " open", config.GRIP_OPEN_ANGLE, " closed", config.GRIP_CLOSED_ANGLE,
          " limits", config.GRIP_MIN_ANGLE, "-", config.GRIP_MAX_ANGLE)
    print("Lift pin", config.LIFT_SERVO_PIN, " down", config.LIFT_DOWN_ANGLE, " up", config.LIFT_UP_ANGLE,
          " limits", config.LIFT_MIN_ANGLE, "-", config.LIFT_MAX_ANGLE)
    for name, angle, low, high in (("GRIP_OPEN", config.GRIP_OPEN_ANGLE, config.GRIP_MIN_ANGLE, config.GRIP_MAX_ANGLE),
                                   ("GRIP_CLOSED", config.GRIP_CLOSED_ANGLE, config.GRIP_MIN_ANGLE, config.GRIP_MAX_ANGLE),
                                   ("LIFT_DOWN", config.LIFT_DOWN_ANGLE, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE),
                                   ("LIFT_UP", config.LIFT_UP_ANGLE, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE)):
        if angle < low or angle > high:
            print("WARNING:", name, "=", angle, "is outside its limits and will be clamped to", low, "-", high)
    print("Starting in 3 s")
    sleep_ms(3000)

    print("--- Part 1: gripper ---")
    for cycle in range(1, CYCLES + 1):
        print("Cycle", cycle, "OPEN (", config.GRIP_OPEN_ANGLE, ")")
        gripper.release()
        sleep_ms(HOLD_MS)
        print("Cycle", cycle, "CLOSED (", config.GRIP_CLOSED_ANGLE, ")")
        gripper.grip()
        sleep_ms(HOLD_MS)
    gripper.release()

    print("--- Part 2: lifter ---")
    for cycle in range(1, CYCLES + 1):
        print("Cycle", cycle, "DOWN (", config.LIFT_DOWN_ANGLE, ")")
        lifter.lower()
        sleep_ms(HOLD_MS)
        print("Cycle", cycle, "UP (", config.LIFT_UP_ANGLE, ")")
        lifter.lift()
        sleep_ms(HOLD_MS)
    lifter.lower()

    print("--- Part 3: sweeps ---")
    sweep("GRIP", gripServo, config.GRIP_MIN_ANGLE, config.GRIP_MAX_ANGLE)
    gripper.release()
    sweep("LIFT", liftServo, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE)
    lifter.lower()
    sleep_ms(HOLD_MS)
    print("Done.")


try:
    run()
finally:
    gripServo.off()
    liftServo.off()
    print("Servo signals off")