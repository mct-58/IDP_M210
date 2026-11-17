from machine import Pin

class LED:
    def __init__(self, pinNum, onValue):
        self.pin = Pin(pinNum, Pin.OUT, value=1)
        self.onValue = onValue
        self.status = False

    def on(self):
        self.pin.value(self.onValue)
        self.status = True

    def off(self):
        self.pin.value(1 - self.onValue)
        self.status = False

    def set(self, state):
        if state:
            self.on()
        else:
            self.off()

    def isOn(self):
        return self.status