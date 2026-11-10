from machine import Pin

class LineSensors:
    def __init__(self, olPinNum, ilPinNum, irPinNum, orPinNum, positiveLineValue):
        self.olPin = Pin(olPinNum, Pin.IN)
        self.ilPin = Pin(ilPinNum, Pin.IN)
        self.irPin = Pin(irPinNum, Pin.IN)
        self.orPin = Pin(orPinNum, Pin.IN)
        self.positiveLineValue = positiveLineValue

    def read(self):
        return (self.olPin.value() == self.positiveLineValue, self.ilPin.value() == self.positiveLineValue, self.irPin.value() == self.positiveLineValue, self.orPin.value() == self.positiveLineValue)