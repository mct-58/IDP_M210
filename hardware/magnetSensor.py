from machine import Pin, ADC
from utime import ticks_ms, ticks_diff, sleep_ms

class MagnetSensor:
    MV_PER_UNIT = 3300/65535

    def __init__(self, adcPinNum, deadBand, invert):
        self.adcPin = ADC(Pin(adcPinNum))
        self.deadBand = deadBand
        self.deadBandUnits = self.deadBand * self.MV_PER_UNIT
        self.invert = invert
        self.baseLine = 1650

    def calibrate(self):
        total = 0
        for _ in range(100):
            total += self.adcPin.read_u16() * self.MV_PER_UNIT
            sleep_ms(10)
        self.baseLine = total/100

    def read(self):
        total = 0
        for _ in range(20):
            total += self.adcPin.read_u16() * self.MV_PER_UNIT
        avgRead = total / 20

        if avgRead > (self.baseLine + self.deadBand):
            if not self.invert:
                return 'South'
            if self.invert:
                return 'North'
        if avgRead < (self.baseLine - self.deadBand):
            if self.invert:
                return 'South'
            if not self.invert:
                return 'North'
        else:
            return None

    def rawChange(self):
        return self.adcPin.read_u16() - self.baseLine