from utime import ticks_diff

class ButtonPress:
    def __init__(self, debounceTime):
        self.debounceTime = debounceTime
        self.acceptedState = 'released'
        self.prevState = False
        self.possibleChangeStart = 0

    def update(self, now, raw):
        if raw != self.prevState:
            self.possibleChangeStart = now
            return False
        if raw == self.prevState and (ticks_diff(now, self.possibleChangeStart) <= self.debounceTime):
            return False
        if raw == self.prevState and (ticks_diff(now, self.possibleChangeStart) >= self.debounceTime) and 