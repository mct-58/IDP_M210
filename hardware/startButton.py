from machine import Pin

class Button:
    def __init__(self, pinNum, onValue):
        if onValue:
            self.pin = Pin(pinNum, Pin.IN, Pin.PULL_DOWN)
        if not onValue:
            self.pin = Pin(pinNum, Pin.IN, Pin.PULL_UP)
        self.onValue = onValue

    def read(self):
        return self.pin.value() == self.onValue
            