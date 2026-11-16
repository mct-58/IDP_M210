from machine import Pin

class Button:
    def __init__(self, pinNum, onValue):
        self.pin = Pin(pinNum, Pin.IN, Pin.PULL_DOWN)
        self.onValue = onValue

    def read(self, onValue):
        if self.pin.value() == onValue:
            return True
        else:
            return False