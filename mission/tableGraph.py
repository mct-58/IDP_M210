class TableGraph:
    def __init__(self, edgeList):
        self.edgeList = edgeList
        self.adjacency = {}
        for edge in self.edgeList:
            if edge[0] not in self.adjacency:
                self.adjacency[edge[0]] = []
            if edge[1] not in self.adjacency:
                self.adjacency[edge[1]] = []
            self.adjacency[edge[0]].append((edge[1], edge[2], edge[3], edge[4]))
            self.adjacency[edge[1]].append((edge[0], (edge[2] + 2) % 4, edge[3], edge[4]))

    def branches(self, node):
        return self.adjacency[node]

    def edge(self, a, b):
        desiredEdge = None
        for edge in self.adjacency[a]:
            if edge[0] == b:
                desiredEdge = edge
        return (desiredEdge[1], desiredEdge[2])

    def shortestPath(self, start, goal):
        dist = {}
        prev = {}
        finished = []

        for node in self.adjacency:
            if node == start:
                dist[node] = 0
            else:
                dist[node] = float('inf')

        while True:
            neighbours = []
            for edge in self.adjacency[start]:
                neighbours.append(edge[0])