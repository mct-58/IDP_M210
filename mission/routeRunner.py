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
        if self.route[self.stepIndex] == 'turn':
            self.turn.start(self.route[self.stepIndex][1], now, True)
        if self.route[self.stepIndex] == 'spin':
            self.turn.start(self.route[self.stepIndex][1], now, False)

    def _nextStep(self, now):
        self.stepIndex += 1
        if self.stepIndex > len(self.route):
            self.finished = True
        else:
            self._beginStep(now)

    def update(self, ol, il, ir, orr, now):
        if self.finished;
            return (0,0)

