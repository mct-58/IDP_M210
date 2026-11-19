from utime import ticks_diff

class PoleDetector:
    def __init__(self, confirmMS):
        self.confirmMS = confirmMS
        self.armed = True
        self.candidateStart = None
        self.candidatePolarity = None

    def update(self, mag, now):
        if not self.armed:
            if mag is None:
                self.armed = True
            return None

        if mag is None:
            self.candidateStart = None
            self.candidatePolarity = None
            return None

        if mag not in ('north', 'south'):
            raise ValueError("mag must be 'north', 'south', or None")

        if mag != self.candidatePolarity:
            self.candidatePolarity = mag
            self.candidateStart = now
            return None

        if ticks_diff(now, self.candidateStart) >= self.confirmMS:
            self.candidateStart = None
            self.candidatePolarity = None
            self.armed = False
            return mag

        return None

    def reset(self):
        self.armed = False
        self.candidateStart = None
        self.candidatePolarity = None