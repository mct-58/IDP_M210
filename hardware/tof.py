from machine import Pin, I2C
from hardware.VL53L0X.VL53L0X import VL53L0X

class tof:
    def __init__(self, busNum, sdaPinNum, sclPinNum, offset):
        self.offset = offset
        self.busNum = busNum
        self.sdaPin = Pin(sdaPinNum)
        self.sclPin = Pin(sclPinNum)
        self.i2cBus = I2C(id=self.busNum, sda=self.sdaPin, scl=self.sclPin)
        self.vl53l0x = VL53L0X(self.i2cBus)
        self.vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
        self.vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)
        self.vl53l0x.start()

    def update(self):
        mask = 0x07
        info = self.vl53l0x._register(0x13)
        value = mask & info
        if not value:
            return None
        reading = self.vl53l0x.read()
        if reading > 8000:
            return None
        return reading - self.offset