import config
from hardware.motorClass import Motor
from hardware.driveTrainClass import DriveTrain
from hardware.lineSensorsClass import LineSensors
from hardware.servoClass import Servo
from hardware.gripperClass import Grip
from hardware.lifterClass import Lift
from behaviour.lineFollow import LineFollower
from behaviour.junctionDetector import JunctionDetector
from behaviour.turn import Turn
from behaviour.packageHandler import PackageHandler
from mission.routeRunner import Runner
from mission import routes
from utime import ticks_ms, ticks_diff, sleep_ms



leftMotor = Motor(config.LEFT_MOTOR_DIR_PIN, config.LEFT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.LEFT_MOTOR_REVERSED, config.LEFT_MOTOR_MIN_SPEED)
rightMotor = Motor(config.RIGHT_MOTOR_DIR_PIN, config.RIGHT_MOTOR_PWM_PIN, config.MOTOR_PWM_FREQ_HZ, config.RIGHT_MOTOR_REVERSED, config.RIGHT_MOTOR_MIN_SPEED)
driveTrain = DriveTrain(leftMotor, rightMotor)
lineSensors = LineSensors(config.LINE_OUTER_LEFT_PIN, config.LINE_INNER_LEFT_PIN, config.LINE_INNER_RIGHT_PIN, config.LINE_OUTER_RIGHT_PIN, config.LINE_DETECTED_VALUE)
lineFollower = LineFollower(config.BASE_SPEED, config.TURN_BIAS_FRACTION, config.LOST_TURN_FRACTION)
junctionDetector = JunctionDetector(config.JUNCTION_CONFIRM_MS)
turn = Turn(config.TURN_SPEED, config.JUNCTION_ADVANCE_MS, config.TURN_MIN_MS, config.TURN_TIMEOUT_MS, config.SPIN_MIN_MS)
gripServo = Servo(config.GRIP_SERVO_PIN, config.GRIP_MIN_ANGLE, config.GRIP_MAX_ANGLE)
liftServo = Servo(config.LIFT_SERVO_PIN, config.LIFT_MIN_ANGLE, config.LIFT_MAX_ANGLE)
gripper = Grip(gripServo, config.GRIP_CLOSED_ANGLE, config.GRIP_OPEN_ANGLE)
lifter = Lift(liftServo, config.LIFT_UP_ANGLE, config.LIFT_DOWN_ANGLE)
packageHandler = PackageHandler(config.GRIP_MOVE_MS, config.LIFT_MOVE_MS)

gripper.release()
lifter.lower()

route = getattr(routes, config.ROUTE_NAME)
runner = Runner(route, lineFollower, junctionDetector, turn, config.LINE_END_MS, packageHandler)

print('Hello World!, Team M210 is the bestest team ever and will win the IDP')
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
        if runner.packageCommand == 'grip':
            gripper.grip()
        elif runner.packageCommand == 'release':
            gripper.release()
        elif runner.packageCommand == 'lift':
            lifter.lift()
        elif runner.packageCommand == 'lower':
            lifter.lower()
        elif runner.packageCommand is not None:
            raise RuntimeError('unknown package handler command: ' + runner.packageCommand)

        driveTrain.drive(left, right)
        
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