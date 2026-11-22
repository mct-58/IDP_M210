from utime import ticks_diff

class Runner:
    def __init__(self, route, follower, detector, turn, lineEndMs, entranceDetector, grippingDetector, approachSpeedFrac=0.75, checkWindowMs=200, packageHandler=None):
        self.route = route
        self.follower = follower
        self.detector = detector
        self.turn = turn
        self.packageHandler = packageHandler
        self.entranceDetector = entranceDetector
        self.grippingDetector = grippingDetector
        self.lineEndMs = lineEndMs
        self.stepIndex = 0
        self.stepStart = None
        self.junctionCount = 0
        self.lostSince = None
        self.finished = False
        self.packageCommand = None
        self.blockOutcome = None
        self.checkWindowMs = checkWindowMs
        self.approachSpeedFrac = approachSpeedFrac

    def start(self, now):
        self._beginStep(now)

    def _beginStep(self, now):
        self.stepStart = now
        self.junctionCount = 0
        self.lostSince = None
        self.follower.reset()
        self.detector.reset()
        self.entranceDetector.reset()
        self.grippingDetector.reset()
    
        step = self.route[self.stepIndex]
        if step[0] == 'turn':
            self.turn.start(step[1], now, 'junction')
        if step[0] == 'spin':
            self.turn.start(step[1], now, 'spin')
        if step[0] == 'pivot':
            self.turn.start(step[1], now, 'pivot')
        if step[0] == 'pickup' or step[0] == 'unload':
            if self.packageHandler is None:
                raise RuntimeError('pickup and unload steps require a package handler')
            self.packageHandler.start(step[0], now)
        if step[0] == 'check' or (step[0] == 'approach'):
            self.blockOutcome = None

    def _nextStep(self, now):
        self.stepIndex += 1
        if self.stepIndex >= len(self.route):
            self.finished = True
        else:
            self._beginStep(now)

    def update(self, ol, il, ir, orr, now, newReading=False, distance=None):

        if self.finished:
            self.packageCommand = None
            return (0,0)

        self.packageCommand = None
        step = self.route[self.stepIndex]

        if step[0] == 'follow':
            speeds = self.follower.update(il, ir)
            j = self.detector.update(ol, orr, now)
            if j is not None and (j == step[2] or step[2] == 'any'):
                self.junctionCount += 1
                if self.junctionCount == step[1]:
                    self._nextStep(now)
            return speeds

        if step[0] == 'turn' or step[0] == 'spin' or step[0] == 'pivot':
            status, l, r = self.turn.update(il, ir, now)
            if status =='done':
                self._nextStep(now)
            elif status == 'timeout':
                self.finished = True
            return (l, r)

        if step[0] == 'toBox':
            if il + ir + ol + orr >= 3:        # True counts as 1, so this counts sensors on the line
                self._nextStep(now)
                return (0, 0)
            return self.follower.update(il, ir)

        if step[0] == 'toEnd':
            if il or ir:
                self.lostSince = None
                return self.follower.update(il, ir)
            if self.lostSince is None:
                self.lostSince = now
            if ticks_diff(now, self.lostSince) >= self.lineEndMs:
                self._nextStep(now)
            return (0,0)

        if step[0] == 'wait':
            if ticks_diff(now, self.stepStart) >= step[1]:
                self._nextStep(now)
            return (0,0)

        if step[0] == 'drive':
            if ticks_diff(now, self.stepStart) >= step[1]:
                self._nextStep(now)
                return (0,0)
            return (step[2], step[2])

        if step[0] == 'pickup' or step[0] == 'unload':
            status, self.packageCommand = self.packageHandler.update(now)
            if status == 'done':
                self._nextStep(now)
            elif status != 'running':
                raise RuntimeError('package handler is not active for the current route step')
            return (0, 0)

        if step[0] == 'check':
            

        self.finished = True
        return (0,0)
