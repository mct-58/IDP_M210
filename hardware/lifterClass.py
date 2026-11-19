class Lift:
    def __init__(self, servo, upAngle, downAngle):
        self.servo = servo
        self.upAngle = upAngle
        self.downAngle = downAngle

    def lift(self):
        self.servo.setAngle(self.upAngle)

    def lower(self):
        self.servo.setAngle(self.downAngle)