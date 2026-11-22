from machine import Pin, I2C
from hardware.VL53L0X.VL53L0X import VL53L0X

mask = 0x07
statusRegisterNum = 0x13
outOfRangeNum = 8000


class ToF:
    def __init__(self, busNum, sdaPinNum, sclPinNum, offset):
        self.offset = offset
        self.busNum = busNum
        self.sdaPin = Pin(sdaPinNum)
        self.sclPin = Pin(sclPinNum)
        self.i2cBus = I2C(id=self.busNum, sda=self.sdaPin, scl=self.sclPin)
        self.vl53l0x = VL53L0X(self.i2cBus)
        self.vl53l0x.set_Vcsel_pulse_period(self.vl53l0x.vcsel_period_type[0], 18)
        self.vl53l0x.set_Vcsel_pulse_period(self.vl53l0x.vcsel_period_type[1], 14)
        self.vl53l0x.start()
        self.latestReading = None

    def update(self):
        status = self.vl53l0x._register(statusRegisterNum)
        ready = mask & status
        if not ready:
            return False
        reading = self.vl53l0x.read()
        if reading > outOfRangeNum:
            self.latestReading = None
            return True
        if reading < outOfRangeNum:
            adjReading = reading - offset
            if adjReading < 0:
                adjReading = 0
            self.latestReading = adjReading
            return True