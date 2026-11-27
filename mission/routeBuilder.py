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

    def _lineAheadMm(self, node, heading):
        total = 0
        while True:
            ahead = [b for b in self.graph.branches(node) if b[1] == heading]
            if not ahead:
                return total
            node = ahead[0][0]
            total += ahead[0][2]

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
                if self._lineAheadMm(path[0], pathEdges[0][0]) > (self.sensorOffsetMm + self.marginMm):
                    route.append(('spin', 'right'))
                else:
                    raise ValueError('Not long enough to perform a U-turn')
                currentHeading = pathEdges[0][0]
        
        chunks = []
        runStart = path[0]
        holder = []
        for j in range(len(pathEdges)):
            holder.append(path[j + 1])
            heading = pathEdges[j][0]
            isLastEdge = (j == len(pathEdges) - 1)
            if isLastEdge or pathEdges[j + 1][0] != heading:
                chunks.append((runStart, holder, heading))
                runStart = path[j + 1]
                holder = []

        for k in range(len(chunks)):
            if k == len(chunks) - 1:
                if len(self.graph.branches(chunks[k][1][-1])) == 1:
                    if len(chunks[k][1]) > 1:
                        raise ValueError('Path drives straight on into a dead end at ' + chunks[k][1][-1])
                else:
                    label =  self._label(chunks[k][1][-1], chunks[k][2])
                    if label is None:
                        raise ValueError('No junction to count at ' + chunks[k][1][-1])
                    count, distance = self._count(chunks[k][0], chunks[k][1], chunks[k][2], label)
                    if count > 0:
                        route.append(('follow', count, label))
                        route.append(('drive', self.advanceMs, self.advanceSpeed))
                    else:
                        route.append(('drive', round(distance * self.advanceMs / self.sensorOffsetMm), self.advanceSpeed))
            else:
                label =  self._label(chunks[k][1][-1], chunks[k][2])
                count, distance = self._count(chunks[k][0], chunks[k][1], chunks[k][2], label)
                nextHeading = chunks[k+1][2]
                turnName = self._turnName((nextHeading - chunks[k][2]) % 4)
                if count > 0:
                    route.append(('follow', count, label))
                    route.append(('turn', turnName))
                else:
                    route.append(('drive', round(distance * self.advanceMs / self.sensorOffsetMm), self.advanceSpeed))
                    route.append(('pivot', turnName))
                currentHeading = nextHeading

        return (route, currentHeading)