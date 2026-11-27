class RouteBuilder:
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
        raise ValueError('Delta is either 0 or 2 or a weird other number')

    def _label(self, node, heading):
        labels = []
        for edge in self.graph.branches(node):
            r = (edge[1] - heading) % 4
            if r == 1:
                labels.append('right')
            if r == 3:
                labels.append('left')
        if 'right' in labels and ('left' in labels):
            return 'both'
        elif 'right' in labels:
            return 'right'
        elif 'left' in labels:
            return 'left'
        return None

    def _count(self, runStart, runNodes, heading, label):
        prev = runStart
        count = 0
        runningD = 0

        for node in runNodes:
            desiredEdge = self.graph.edge(prev, node)
            runningD += desiredEdge[1]
            if runningD <= (self.sensorOffsetMm - self.marginMm):
                pass
            elif runningD < (self.sensorOffsetMm + self.marginMm):
                if self._label(node, heading) == label:
                    raise ValueError
            else:
                if self._label(node, heading) == label:
                    count += 1

            prev = node

        return (count, runningD)

    def build(self, path, startHeading):
        if len(path) < 2:
            return ([], startHeading) 
        route = []
        pathEdges = []
        currentHeading = startHeading
        for i in range(len(path) - 1):
            pathEdges.append(self.graph.edge(path[i], path[i + 1]))
        if startHeading != pathEdges[0][0]:
            delta = (pathEdges[0][0] - startHeading) % 4
            if delta == 1 or (delta == 3):
                route.append(('pivot', self._turnName(delta)))
                currentHeading = pathEdges[0][0]
            if delta == 2:
                if pathEdges[0][1] > (self.sensorOffsetMm + self.marginMm):
                    route.append(('spin', 'right'))
                else:
                    raise ValueError('Not long enough to perform a U-turn')
                currentHeading = pathEdges[0][0]