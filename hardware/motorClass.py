from machine import Pin, PWM

class Motor:
    def __init__(self, dirPin, pwmPin, pwmFreq, isReversed, stallSpeed):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(pwmPin))  # set motor pwm pin
        self.pwm.freq(pwmFreq)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        self.isReversed = isReversed
        self.stallSpeed = stallSpeed

    def off(self):
        self.pwm.duty_u16(0)
        
    def _dutyValue(self, speed):
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        return int(65535/100 * (self.stallSpeed + (100 - self.stallSpeed) * speed / 100))

    def forward(self, speed):
        self.mDir.value(self.isReversed)
        self.pwm.duty_u16(self._dutyValue(speed))  # speed range 0-100 motor

    def reverse(self, speed):
        self.mDir.value(not self.isReversed)
        self.pwm.duty_u16(self._dutyValue(speed))