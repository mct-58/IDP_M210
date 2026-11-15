from machine import Pin

class Button:
    def __init__(self, pinNum, onValue):
        self.pin = Pin(pinNum)
        self.onValue = onValue

    def read(self):
        return self.pin.value()