from machine import PWM, Pin

class LineSensors:
    def __init__(self, olPIN, ilPIN, irPIN, orPIN, positiveLineValue):
        self.olPIN = Pin(olPIN, Pin.IN)
        self.ilPIN = Pin(ilPIN, Pin.IN)
        self.irPIN = Pin(irPIN, Pin.IN)
        self.orPIN = Pin(orPIN, Pin.IN)
        self.positiveLineValue = positiveLineValue

    def read(self):
        return (self.olPIN.value() == self.positiveLineValue, self.ilPIN.value() == self.positiveLineValue, self.irPIN.value() == self.positiveLineValue, self.orPIN.value() == self.positiveLineValue)