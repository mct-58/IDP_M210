from utime import ticks_diff

class ButtonPress:
    def __init__(self, debounceTime):
        self.debounceTime = debounceTime
        self.acceptedState = False
        self.prevRaw = False
        self.possibleChangeStart = 0

    def update(self, raw, now):
        if raw != self.prevRaw:
            self.possibleChangeStart = now
            self.prevRaw = raw
            return False
        if ticks_diff(now, self.possibleChangeStart) <= self.debounceTime:
            return False
        if ticks_diff(now, self.possibleChangeStart) > self.debounceTime and (raw != self.acceptedState):
            self.acceptedState = raw
            return self.acceptedState
        return False