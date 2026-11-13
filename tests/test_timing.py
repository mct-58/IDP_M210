# Timing test: (A) is the Pico's clock right?  (B) how long does one loop pass really take?
# Motors are commanded to 0 the whole time - the wheels will not move.

from utime import ticks_ms, ticks_us, ticks_diff, sleep_ms
import machine
import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain
from hardware.lineSensorsClass import LineSensors
from behaviour.lineFollow import LineFollower

print("CPU frequency:", machine.freq() // 1000000, "MHz")

# ---- A: clock check against a stopwatch -------------------------------------
# Start your phone stopwatch exactly when it prints 0. At 10 it should read 10.0 s.
print("\nA) Clock check - start a stopwatch on '0'")
sleep_ms(2000)
start = ticks_ms()
for second in range(11):
    while ticks_diff(ticks_ms(), start) < second * 1000:
        pass
    print(second)

# ---- B: loop timing using the real objects ----------------------------------
leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN,
                  config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN,
                   config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)
driveTrain = DriveTrain(leftMotor, rightMotor)
lineSensors = LineSensors(config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN,
                          config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN,
                          config.LINE_DETECTED_VALUE)
lineFollower = LineFollower(config.BASE_SPEED, config.TURN_BIAS_FRACTION, config.LOST_TURN_FRACTION)

PASSES = 500
workTimes = []      # time spent doing the work in one pass (us)
periods = []        # full pass time including the pacing sleep (us)

print("\nB) Timing", PASSES, "loop passes, LOOP_PERIOD_MS =", config.LOOP_PERIOD_MS)
try:
    previous = ticks_us()
    for _ in range(PASSES):
        loopStart = ticks_ms()
        workStart = ticks_us()

        ol, il, ir, orr = lineSensors.read()
        lSpeed, rSpeed = lineFollower.update(il, ir)
        driveTrain.drive(0, 0)              # same call cost as real driving, wheels stay still

        workTimes.append(ticks_diff(ticks_us(), workStart))
        elapsed = ticks_diff(ticks_ms(), loopStart)
        if elapsed < config.LOOP_PERIOD_MS:
            sleep_ms(config.LOOP_PERIOD_MS - elapsed)

        now = ticks_us()
        periods.append(ticks_diff(now, previous))
        previous = now
finally:
    driveTrain.stop()

print("Work per pass:   avg %d us, max %d us" % (sum(workTimes) // PASSES, max(workTimes)))
print("Full loop period: avg %.2f ms, min %.2f ms, max %.2f ms" %
      (sum(periods) / PASSES / 1000, min(periods) / 1000, max(periods) / 1000))
print("Done")