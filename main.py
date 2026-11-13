from behaviour import junctionDetector
import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain
from hardware.lineSensorsClass import LineSensors
from behaviour.lineFollow import LineFollower
from behaviour.junctionDetector import JunctionDetector
from behaviour.turn import Turn
from mission.routeRunner import Runner
from mission import routes
from utime import ticks_ms, ticks_diff, sleep_ms

leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)
driveTrain = DriveTrain(leftMotor, rightMotor)
lineSensors = LineSensors(config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN, config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN, config.LINE_DETECTED_VALUE)
lineFollower = LineFollower(config.BASE_SPEED, config.TURN_BIAS_FRACTION, config.LOST_TURN_FRACTION)
junctionDetector = JunctionDetector(config.JUNCTION_CONFIRM_MS)
turn = Turn(config.TURN_SPEED, config.JUNCTION_ADVANCE_MS, config.TURN_MIN_MS, config.TURN_TIMEOUT_MS)

route = getattr(routes, config.ROUTE_NAME)
runner = Runner(route, lineFollower, junctionDetector, turn, config.LINE_END_MS)

print('Hello World!, Team M210 is the bestest team every and will win the IDP')
sleep_ms(3000)

try:
    runStart = ticks_ms()
    runner.start(runStart)
    lastStep = -1
    lastCount = -1
    while True:
        loopStart = ticks_ms()
        ol, il, ir, orr = lineSensors.read()
        left, right = runner.update(ol, il, ir, orr, loopStart)
        driveTrain.drive(lSpeed, rSpeed)
        
        if runner.stepIndex != lastStep:
            print('step', runner.stepIndex, route[runner.stepIndex] if not runner.finished else 'END')
            lastStep = runner.stepIndex
        if runner.junctionCount != lastCount:
            print('   junctions', runner.junctionCount)
            lastCount = runner.junctionCount

        if runner.finished:
            break
        if ticks_diff(ticks_ms(), runStart) > config.RUN_TIME_MS:
            print('backstop time reached')
            break

        elapsed = ticks_diff(ticks_ms(), loopStart)
        if elapsed < config.LOOP_PERIOD_MS:
            sleep_ms(config.LOOP_PERIOD_MS - elapsed)

finally:
    driveTrain.stop()
    print('Whoopsies, it seems the robot has taken a quick pit stop! ')