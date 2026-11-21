# ----------------------------------------------------------------- PINS -----
# Drive motors (12 V connectors: left = motor 3/J39, right = motor 4/J40)
LEFT_MOTOR_DIR_PIN = 4
LEFT_MOTOR_PWM_PIN = 5
RIGHT_MOTOR_DIR_PIN = 7
RIGHT_MOTOR_PWM_PIN = 6

# Line sensors, left to right across the front
LINE_OUTER_LEFT_PIN = 18
LINE_INNER_LEFT_PIN = 19
LINE_INNER_RIGHT_PIN = 20
LINE_OUTER_RIGHT_PIN = 21

# Servos (PicoBot servo connectors: J35 = GP13, J36 = GP15)
GRIP_SERVO_PIN = 13           # TODO: confirm which servo is on which connector
LIFT_SERVO_PIN = 15           # TODO

# Distance sensors - one per I2C bus (both use address 0x29)
TOF_FRONT_BUS = 0
TOF_FRONT_SDA_PIN = 8
TOF_FRONT_SCL_PIN = 9
TOF_BACK_BUS = 1
TOF_BACK_SDA_PIN = 10         # TODO: confirm wiring
TOF_BACK_SCL_PIN = 11         # TODO

# Magnetic sensor - must be an ADC pin (26, 27 or 28)
MAGNET_PIN = 26

# Start button, LEDs (via opto-isolator), IR receiver
START_BUTTON_PIN = None       # TODO
AMBER_LED_PIN = None          # TODO
RED_LED_PIN = None            # TODO
GREEN_LED_PIN = None          # TODO
STATUS_LED_PIN = "LED"        # Pico's onboard LED
IR_RECEIVER_PIN = None        # TODO (top-deck stretch goal)


# ------------------------------------------------------- MOTORS & DRIVING ---
MOTOR_PWM_FREQ_HZ = 1000
LEFT_MOTOR_REVERSED = False
RIGHT_MOTOR_REVERSED = True
LEFT_MOTOR_MIN_SPEED = 25     # deadband: lowest speed % that reliably turns the wheel
RIGHT_MOTOR_MIN_SPEED = 25

BASE_SPEED = 70               # line-following speed, 0-100
TURN_SPEED = 60               # speed during creep and pivots, 0-100


# ------------------------------------------------ LINE SENSING & FOLLOWING ---
LINE_DETECTED_VALUE = 1       # what a line sensor reads over the white line
TURN_BIAS_FRACTION = 0.5      # inner wheel = BASE_SPEED x this when correcting
LOST_TURN_FRACTION = 0.2      # inner wheel fraction when both inner sensors lose the line


# ---------------------------------------------------- JUNCTIONS & TURNS -----
JUNCTION_CONFIRM_MS = 70      # outer sensor must see a line this long to count
JUNCTION_ADVANCE_MS = 830     # creep after a junction so the axle reaches it
TURN_MIN_MS = 750             # 90 deg turns/pivots: ignore line sensors this long
SPIN_MIN_MS = 1900            # 180 deg spins: ignore line sensors this long
TURN_TIMEOUT_MS = 5000        # give up on any turn after this long
LINE_END_MS = 100             # both inner sensors off this long = end of line


# -------------------------------------------------- START BUTTON & LEDS -----
BUTTON_PRESSED_VALUE = 1      # pin value when pressed (1 = wired to 3.3 V)
BUTTON_DEBOUNCE_MS = 200
LED_ON_VALUE = 1              # pin value that lights an LED through the opto (TODO: check wiring)
AMBER_FLASH_PERIOD_MS = 500   # one full on+off cycle while moving


# ------------------------------------------------------ MAGNETIC SENSOR -----
MAGNETIC_DEAD_BAND_MV = 200  
MAGNET_INVERT = False         
MAGNET_READ_MS = 300          # collect readings this long, then take the majority


# ------------------------------------------------------- DISTANCE (ToF) -----
TOF_FRONT_OFFSET_MM = 0       # subtracted from readings (from ruler calibration)
TOF_BACK_OFFSET_MM = 0
BLOCK_DETECT_MM = None        # TODO: front ToF reading at which to stop and grab
BLOCK_CONFIRM_READINGS = 3    # consecutive readings below BLOCK_DETECT_MM to count as a block


# ----------------------------------------------------- GRIPPER & LIFT -------
GRIP_MIN_ANGLE = 30         # TODO: safe limits, found by moving slowly to each stop
GRIP_MAX_ANGLE = 240         # TODO
GRIP_OPEN_ANGLE = 180        # TODO
GRIP_CLOSED_ANGLE = 100      # TODO

LIFT_MIN_ANGLE = 30
LIFT_MAX_ANGLE = 230
LIFT_UP_ANGLE = 150          # TODO (carrying height: block <= 30 mm off the ground)
LIFT_DOWN_ANGLE = 20        # TODO

GRIP_MOVE_MS = 600            # TODO: time for the gripper to finish moving
LIFT_MOVE_MS = 800            # TODO: time for the lift to finish moving


# ------------------------------------------------------ MISSION & ROUTE -----
BAY_SPACING_MS = None         # TODO: timed drive from one bay junction to the next
LOOP_PERIOD_MS = 10
RUN_TIME_MS = 120000          # backstop: stop if a run lasts longer than this
ROUTE_NAME = 'GRAB'