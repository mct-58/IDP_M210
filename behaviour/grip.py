class Grip:
    def __init__(self, servo, gripAngle, releaseAngle):
        self.servo = servo
        self.gripAngle = gripAngle
        self.releaseAngle = releaseAngle

    def grip(self):
        self.servo.setAngle(self.gripAngle)

    def release(self):
        self.servo.setAngle(self.releaseAngle)