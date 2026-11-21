from utime import ticks_diff

class Flasher:
    def __innit__(self, period):
        self.period = period
        self.active = False
        self.flashingStartTime = None

    def start(self, now):
        if not self.active:
            self.active = True
            self.flashingStartTime = now

    def stop(self):
        self.active = False
        self.flashingStartTime = None

    def update(self, now):
        if not self.active:
            return False
        if (ticks_diff(now, self.flashingStartTime) % self.period) <= (self.period/2):
            return True
        else:
            return False