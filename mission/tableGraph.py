class TableGraph:
    def __init__(self, edgeList):
        self.edgeList = edgeList
        self.adjacency = {}
        for edge in self.edgeList:
            for fromNode, toNode in edge:
                if fromNode not in self.adjacency:
                    self.adjacency[fromNode] = []
                if toNode not in self.adjacency:
                    self.adjacency[toNode] = []
            self.adjacency[edge[0]].append((edge[1], edge[2], edge[3], edge[4]))
            self.adjacency[edge[1]].append((edge[0], (edge[2] + 2) % 4, edge[3], edge[4]))

    def branches(self, node):
        return self.adjacency[node]

    def edge(self, a, b):
        desiredEdge = None
        for edge in self.edgeList:
            if edge[0] == a and (edge[1] == b):
                desiredEdge = edge
            elif edge[0] == b and (edge[1] == a):
                desiredEdge = edge
        return (desiredEdge[2], desiredEdge[3])

    def shortestPath(self, start, goal):
        