class driveTrain:
    def __innit__(self, rightMotor, leftMotor, rightSpeed, leftSpeed):
        self.rightMotor = rightMotor
        self.leftMotor = leftMotor
        self.rightSpeed = rightSpeed
        self.leftSpeed = leftSpeed

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

    def stop(self):
        self.rightSpeed = 0
        self.leftSpeed = 0