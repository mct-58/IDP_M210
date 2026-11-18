from machine import Pin, PWM




class Servo:
    # Common settings for 270° servos:
    # 0.5 ms → minimum (0°)
    # 2.5 ms → maximum (270°)
    # Total span = 2.0 ms
    # Frequency: 50 Hz (20 ms period)
    # 
    # Duty % = Pulse width / Period x 100
    # Minimum (0°) = 0.5/20
    # Centre (135°) = 1.5/20
    # Maximum (270°) = 2.5/20
    #
    # Convert to Pico PWM (16-bit)
    # Pico uses: 0 → 65535
    # Duty value = Duty Fraction x 65535
    # Minimum (0.5 ms) = 0.025 * 65535
    # Centre (1.5 ms) = 0.075 * 65535
    # Maximum (2.5 ms) = 0.125 * 65535
    MIN_DUTY = 1638 # 0°
    MID_DUTY = 4915 # 135°
    MAX_DUTY = 8192 # 270°
    
    def __init__(self, servoPinNum, minAngle, maxAngle):
        self.servoPin = PWM(Pin(servoPinNum))
        self.servoPin.freq(50)  # 50 Hz for servo
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        
 
    # Convert angle (0–270) to duty
    def setAngle(self, angle):
       # Clamp angle
       if angle < self.minAngle:
           angle = self.minAngle
       if angle > self.maxAngle:
           angle = self.maxAngle
 
       duty = int(self.MIN_DUTY + (angle / 270) * (self.MAX_DUTY - self.MIN_DUTY))
       self.servoPin.duty_u16(duty)

    def off(self):
        self.servoPin.duty_u16(0)

