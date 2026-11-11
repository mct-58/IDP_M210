import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain
from hardware.lineSensorsClass import LineSensors
from behaviour.lineFollow import LineFollower
from utime import ticks_ms, ticks_diff, sleep_ms

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED)
driveTrain = DriveTrain(leftMotor, rightMotor)
lineSensors = LineSensors(config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN, config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN, config.LINE_DETECTED_VALUE)
lineFollower = LineFollower(config.BASE_SPEED, config.TURN_BIAS_FRACTION, config.LOST_TURN_FRACTION)

print('Hello World!, Team M210 is the bestest team every and will win the IDP')
sleep_ms(3000)

try:
    runStart = ticks_ms()
    while True:
        loopStart = ticks_ms()
        ol, il, ir, orr = lineSensors.read()
        lSpeed, rSpeed = lineFollower.update(il, ir)
        driveTrain.drive(lSpeed, rSpeed)
        elapsed = ticks_diff(ticks_ms(), loopStart)
        if ticks_diff(ticks_ms(), runStart) > config.RUN_TIME_MS:
            break 
        if elapsed < config.LOOP_PERIOD_MS:
            sleep_ms(config.LOOP_PERIOD_MS - elapsed)
finally:
    driveTrain.stop()
    print('Whoopsies, it seems the robot has taken a quick pit stop! ')