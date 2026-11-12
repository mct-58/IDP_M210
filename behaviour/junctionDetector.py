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
            if self.candidateStart = None:
                self.candidateStart = now
                self.sawLeft = False
                self.sawRight = False
                return None
            if ticks_diff(self.candidateStart, now) > self.confirmMS:
                
