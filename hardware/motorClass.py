from machine import Pin, PWM

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def _duty_value(self, speed):
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        return int(65535 * speed / 100)

    def forward(self, speed=50):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(self._duty_value(speed))  # speed range 0-100 motor

    def reverse(self, speed=50):
        self.mDir.value(1)
        self.pwm.duty_u16(self._duty_value(speed))