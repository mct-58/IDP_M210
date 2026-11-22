class BlockDetector:
    def __init__(self, detectionDistance, numConsecReadings):
        self.detectionDistance = detectionDistance
        self.numConsecReadings = numConsecReadings
        self.currentNumConsecReadings = 0

    def reset(self):
        self.currentNumConsecReadings = 0

    def update(self, isNew, distance):
        if not isNew:
            pass
        if distance is None:
            self.currentNumConsecReadings = 0
        if distance <= self.detectionDistance:
            self.currentNumConsecReadings += 1
        if distance > self.detectionDistance:
            self.currentNumConsecReadings = 0
        if self.currentNumConsecReadings >= self.numConsecReadings:
            return True