class PoleVote:
    def __init__(self):
        self.northReadings = 0
        self.southReadings = 0
        self.noReadings = 0

    def add(self, reading):
        if reading is None:
            self.noReadings += 1
        if reading == 'south':
            self.southReadings += 1
        if reading == 'north':
            self.northReadings += 1

    def reset(self):
        self.northReadings = 0
        self.southReadings = 0
        self.noReadings = 0

    def result(self):
        maxVal = 0
        tempL = [self.northReadings, self.southReadings, self.noReadings]
        for i in tempL:
            if i > maxVal:
                maxVal = i

        resultIndex = tempL.index(maxVal)
        if resultIndex = 0:
            return 'north'
        if resultIndex = 1:
            return 'south'
        if resultIndex = 2:
            return None