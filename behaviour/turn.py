from utime import ticks_diff

class Turn:
    def __init__(self, turnSpeed, advanceMs, minMs, timeoutMs):
        self.turnSpeed = turnSpeed
        self.advanceMs = advanceMs
        self.minMs = minMs
        self.timoutMs = timeoutMs
        self.direction = None
        self.phase = None
        self.turnStart = None
        self.phaseStart = None

    def start(self, direction, now, advance):
        self.direction = direction
        self.turnStart = now
        self.phaseStart= now
        if advance:
            self.phase = 'advance'
        if not advance:
            self.phase = 'pivot'

    def update(self, il, ir, now):
        if ticks_diff(now, self.turnStart) >= self.timeoutMs:
            self.phase = None
            return ('timeout', 0, 0)
        if self.phase == 'advance':
            if ticks_diff(now, self.phase) >= self.advanceMs:
                self.phase = 'pivot'
                self.phaseStart = now
            else:
                return ('running', self.turnSpeed, self.turnSpeed)
            