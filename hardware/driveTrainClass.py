class DriveTrain:
    def __init__(self, rightMotor, leftMotor):
        self.rightMotor = rightMotor
        self.leftMotor = leftMotor

    def _speed_splitter(self, speed):
        mod_speed = 0
        dir = 0
        if speed < 0:
            mod_speed = speed * -1
            dir = 0
        else:
            mod_speed = speed
            dir = 1
        return mod_speed, dir

    def drive(self, leftSpeed, rightSpeed):
        self.leftMotor._duty_value(leftSpeed)
        self.rightMotor._duty_value(rightSpeed)

    def stop(self):
        self.rightMotor.off()
        self.leftMotor.off()