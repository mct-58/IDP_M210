# Loading-area reverse + pivot test.
# Start: robot on the LOWER GREEN stub, facing west (towards the loading area),
#        a little way before the box, centred on the stub line.
# What it does:
#   1. follows the stub until the line ends (just inside the loading area)
#   2. stops for MEASURE_MS  -> MEASURE: axle to edge line distance d (mm)
#   3. reverses for REVERSE_MS
#   4. stops for MEASURE_MS  -> CHECK: axle should be on (or just short of) the edge line
#   5. pivots left onto the edge line (now facing south)
#   6. follows the edge line south to the bottom-right corner and stops
#
# Tuning: REVERSE_MS = d / 90 * 1000   (90 mm/s = measured speed at 40)
# When it works, copy REVERSE_MS into step 14 of PERFORM.

from utime import ticks_ms, ticks_diff, sleep_ms
import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain
from hardware.lineSensorsClass import LineSensors
from behaviour.lineFollow import LineFollower
from behaviour.junctionDetector import JunctionDetector
from behaviour.turn import Turn
from mission.routeRunner import Runner

REVERSE_MS = 720
REVERSE_SPEED = 40
MEASURE_MS = 5000

ROUTE = [
    ('toEnd',),
    ('wait', MEASURE_MS),
    ('drive', REVERSE_MS, -REVERSE_SPEED),
    ('wait', MEASURE_MS),
    ('pivot', 'right'),      # was 'left': facing east, right turns south
    ('follow', 1, 'left'),   # was 'right': on the left side, stubs and the corner are on the robot's left
]

NOTES = [
    "following stub to the loading area",
    "MEASURE NOW: axle to edge line (mm)",
    "reversing %d ms" % REVERSE_MS,
    "CHECK NOW: is the axle over the edge line?",
    "pivoting left onto the edge line",
    "following edge line south to the corner",
]

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ,
                  config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ,
                   config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)
driveTrain = DriveTrain(leftMotor, rightMotor)
lineSensors = LineSensors(config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN,
                          config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN,
                          config.LINE_DETECTED_VALUE)
lineFollower = LineFollower(config.BASE_SPEED, config.TURN_BIAS_FRACTION, config.LOST_TURN_FRACTION)
junctionDetector = JunctionDetector(config.JUNCTION_CONFIRM_MS)
turn = Turn(config.TURN_SPEED, config.JUNCTION_ADVANCE_MS, config.TURN_MIN_MS,
            config.TURN_TIMEOUT_MS, config.SPIN_MIN_MS)
runner = Runner(ROUTE, lineFollower, junctionDetector, turn, config.LINE_END_MS)

print("Loading stub test: REVERSE_MS =", REVERSE_MS, "- starting in 3 s")
sleep_ms(3000)

try:
    runStart = ticks_ms()
    runner.start(runStart)
    lastStep = -1
    while True:
        loopStart = ticks_ms()
        ol, il, ir, orr = lineSensors.read()
        left, right = runner.update(ol, il, ir, orr, loopStart)
        driveTrain.drive(left, right)

        if runner.stepIndex != lastStep and not runner.finished:
            print("step %d: %s" % (runner.stepIndex + 1, NOTES[runner.stepIndex]))
            lastStep = runner.stepIndex

        if runner.finished:
            print("done - reached the corner" if runner.stepIndex >= len(ROUTE)
                  else "stopped early (turn timeout?)")
            break
        if ticks_diff(ticks_ms(), runStart) > 60000:
            print("backstop time reached")
            break

        elapsed = ticks_diff(ticks_ms(), loopStart)
        if elapsed < config.LOOP_PERIOD_MS:
            sleep_ms(config.LOOP_PERIOD_MS - elapsed)
finally:
    driveTrain.stop()
    print("Motors stopped")