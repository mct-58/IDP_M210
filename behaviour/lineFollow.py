class LineFollower:
    def __init__(self, baseSpeed, biasFraction, lostFraction):
        self.baseSpeed = baseSpeed
        self.biasFraction = biasFraction
        self.lostFraction = lostFraction
        self.lastSide = None

    def update(self, innerLeft, innerRight):
        if innerLeft and innerRight:
            return (self.baseSpeed, self.baseSpeed)
        if not innerLeft and innerRight:
            self.lastSide = 'Right'
            return (self.baseSpeed, self.biasFraction * self.baseSpeed)
        if innerLeft  and not innerRight:
            self.lastSide = 'Left'
            return (self.baseSpeed * self.biasFraction, self.baseSpeed)
        if not innerLeft and not innerRight and self.lastSide == 'Left':
            return (self.baseSpeed * self.lostFraction, self.baseSpeed)
        if not innerLeft and not innerRight and self.lastSide == 'Right':
            return (self.baseSpeed, self.baseSpeed * self.lostFraction)
        if not innerLeft and not innerRight and self.lastSide == None:
            return (0,0)
