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
        '''
        dist = {}
        prev = {}
        finished = []

        for node in self.adjacency:
            if node == start:
                dist[node] = 0
            else:
                dist[node] = float('inf')
`       '''
        working_nodes = []
        fixed_nodes = []
        fixed_nodenames = []
        current = start
        while True:
            for edge in self.adjacency[current]:
                if edge[4]: #route is drivable
                    if current == start:
                        working_nodes.append((edge[0], current, edge[3]))   # ('B, 'A', 3)
                    else:
                        working_nodes.append((edge[0], current, minDist + edge[3]))
                else:
                    pass
            
            minDist = float('inf')
            minNode = None
            for node in working_nodes:
                if node[2] < minDist and not node[0] in fixed_nodenames: #edge length less than minDist
                    minDist = node[2]
                    minNode = node
                else:
                    pass
            
            fixed_nodes.append(minNode)
            fixed_nodenames.append(minNode[0])
            current = minNode[0]
            if current == goal:
                break
        print("min distance from start to goal is " + str(minDist))



 



        
        







