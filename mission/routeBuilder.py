class Translator:
    def __init__(self, graph, sensorOffsetMm, marginMm, advanceMs, advanceSpeed):
        self.graph = graph
        self.sensorOffsetMm = sensorOffsetMm
        self.marginMm = marginMm
        self.advanceMs = advanceMs
        self.advanceSpeed = advanceSpeed

    def _turnName(self, delta):
        if delta == 1:
            return 'right'
        if delta == 3:
            return 'left'
        return None

    def _label(self, node, heading):
        labels = []
        for edge in self.graph.branches(node):
            r = (edge[1] - heading) % 4
            if r == '1':
                labels.append('right')
            if r == '3':
                labels.append('left')

    def _count(self, runStart, runNodes, label):

    def build(self, path, startHeading):