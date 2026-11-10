class DriveTrain:
    def __init__(self, leftMotor, rightMotor):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        
    def _setMotor(self, motor, speed):
        if speed < 0:
            motor.reverse(abs(speed))
        else:
            motor.forward(speed)

    def drive(self, leftSpeed, rightSpeed):
        self._setMotor(self.leftMotor, leftSpeed)
        self._setMotor(self.rightMotor, rightSpeed)

    def stop(self):
        self.rightMotor.off()
        self.leftMotor.off()