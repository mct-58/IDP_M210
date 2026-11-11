from utime import sleep
import config

# input to line_follow is simply tuple of form e.g. (0.001, 0.998, 0.998, 0.001)
# this would represent two central sensors above white tape, two outers not
# could introduce new config vars: TURN_BIAS_FRACTION
def line_follow(out_left, in_left, in_right, out_right):
    # out_left etc. are True or False
    motor_speeds = [] #scale factor of motor speeds
    if in_left and in_right:
        motor_speeds = [1, 1] #[L, R] values from 0-1
    elif not in_left and in_right:
        motor_speeds = [TURN_BIAS_FRACTION, 1]
    elif in_left and not in_right:
        motor_speeds = [1, TURN_BIAS_FRACTION]
    else:
        motor_speeds = [0,0] # need to add a case for getting lost completely off the line
    return motor_speeds












'''
motorL = Motor()
motorR = Motor(Pin(2), Pin(3))
start = time.ticks_ms() # get millisecond counter
delta = time.ticks_diff(time.ticks_ms(), start)
drive_train = driveTrainClass()
while delta < 1000:
    motor1.forward(50)
    delta = time.ticks_diff(time.ticks_ms(), start)

 # Pin 18 = GP18 (labelled 24 on the jumper)


while True:
    light_1 = Pin(18, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    light_2 = Pin(19, Pin.IN, Pin.PULL_DOWN)
    light_3 = Pin(20, Pin.IN, Pin.PULL_DOWN)
    light_4 = Pin(21, Pin.IN, Pin.PULL_DOWN)
    ref_value = 10
'''
