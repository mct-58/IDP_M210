from utime import ticks_diff

class JunctionDetector:
    def __init__(self, confirmMS):
        self.confirmMS = confirmMS
        self.armed = True
        self.candidateStart = None
        self.sawLeft = False
        self.sawRight = False

    def update(self, ol, orr, now):
        if not self.armed:
            if not ol and not orr:
                self.armed = True
            return None
        if self.armed and (ol or orr):
            if self.candidateStart is None:
                self.candidateStart = now
                self.sawLeft = False
                self.sawRight = False
                if ol:
                    self.sawLeft = True
                if orr:
                    self.sawRight = True
                return None
            if ticks_diff(now, self.candidateStart) <= self.confirmMS:
                if ol:
                    self.sawLeft = True
                if orr:
                    self.sawRight = True
            if ticks_diff(now, self.candidateStart) >= self.confirmMS:
                if ol and orr:
                    return 'Both'
                if ol:
                    return 'Left'
                if orr:
                    return 'Right'