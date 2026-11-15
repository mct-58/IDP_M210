from utime import ticks_diff

class Turn:
    def __init__(self, turnSpeed, advanceMs, minMs, timeoutMs, spinMinMs):
        self.turnSpeed = turnSpeed
        self.advanceMs = advanceMs
        self.minMs = minMs
        self.timeoutMs = timeoutMs
        self.spinMinMs = spinMinMs
        self.activeMinMs = 0
        self.direction = None
        self.phase = None
        self.turnStart = None
        self.phaseStart = None
        self.seenOff = False

    def start(self, direction, now, mode):
        self.direction = direction
        self.turnStart = now
        self.phaseStart= now
        self.seenOff = False
        if mode == 'junction':
            self.phase = 'advance'
            self.activeMinMs = self.minMs
        if mode == 'spin':
            self.phase = 'pivot'
            self.activeMinMs = self.spinMinMs
        if mode == 'pivot':
            self.phase = 'pivot'
            self.activeMinMs = self.minMs

    def update(self, il, ir, now):
        if ticks_diff(now, self.turnStart) >= self.timeoutMs:
            self.phase = None
            return ('timeout', 0, 0)
        if self.phase == 'advance':
            if ticks_diff(now, self.phaseStart) >= self.advanceMs:
                self.phase = 'pivot'
                self.phaseStart = now
            else:
                return ('running', self.turnSpeed, self.turnSpeed)
        if self.phase == 'pivot':
            if not il and not ir:
                self.seenOff = True
            if ticks_diff(now, self.phaseStart) >= self.activeMinMs and (il or ir) and self.seenOff:
                self.phase = None
                return ('done', 0, 0)
            if self.direction == 'left':
                return ('running', -self.turnSpeed, self.turnSpeed)
            return ('running', self.turnSpeed, -self.turnSpeed)

            