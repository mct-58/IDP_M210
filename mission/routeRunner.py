class Runner:
    def __init__(self, route, follower, detector, turn, lineEndMs):
        self.route = route
        self.follower = follower
        self.detector = detector
        self.turn = turn
        self.lineEndMs = lineEndMs
        self.stepIndex = 0
        self.stepStart = None
        self.junctionCount = 0
        self.lostSince = None
        self.finished = False

    def start(self, now):
        self._beginStep(now)

    def _beginStep(self, now):
        self.stepStart = now
        self.junctionCount = 0
        self.lostSince = None
        self.follower.reset()
        self.detector.reset()
        step = self.route[self.stepIndex]
        if step[0] == 'turn':
            self.turn.start(step[1], now, True)
        if step[0] == 'spin':
            self.turn.start(step[1], now, False)

    def _nextStep(self, now):
        self.stepIndex += 1
        if self.stepIndex >= len(self.route):
            self.finished = True
        else:
            self._beginStep(now)

    def update(self, ol, il, ir, orr, now):
        step = self.route[self.stepIndex]
        if self.finished:
            return (0,0)
        if step == '':
        if step == '':
        if step == '':
        if step == '':
        if step == '':
