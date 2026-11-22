class BlockDetector:
    def __init__(self, detectionDistance, numConsecReadings):
        self.detectionDistance = detectionDistance
        self.numConsecReadings = numConsecReadings
        self.currentNumConsecReadings = 0

    def reset(self):
        self.currentNumConsecReadings = 0

    def update(self, isNew, distance):
        if isNew:
            if distance is None:
                self.currentNumConsecReadings = 0
            elif distance <= self.detectionDistance:
                self.currentNumConsecReadings += 1
            else:
                self.currentNumConsecReadings = 0
        return(self.currentNumConsecReadings >= self.numConsecReadings)