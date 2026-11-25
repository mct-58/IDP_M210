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
        if start == goal:
            return [start]

        working_nodes = []
        fixed_nodes = []
        fixed_nodenames = [start]
        current = start
        first_time = True
        minDist = 0
        while True:
            for edge in self.adjacency[current]:
                if edge[3]: #route is drivable
                    if first_time:
                        working_nodes.append((edge[0], current, edge[2]))   # ('B, 'A', 3)
                        first_time = False
                    else:
                        working_nodes.append((edge[0], current, minDist + edge[2]))
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
            if minNode is None:
                return None

            fixed_nodes.append(minNode)
            fixed_nodenames.append(minNode[0])
            current = minNode[0]
            if current == goal:
                break

        print("min distance from start to goal is " + str(minDist))

        # now need to digest route from fixed_nodes
        route = [goal]
        desired_node = goal
        while desired_node != start:
            predecessor = None
            for node in fixed_nodes:
                if node[0] == desired_node:
                    predecessor = node[1]
                    break
            if predecessor is None or predecessor in route:
                return None
            route.append(predecessor)
            desired_node = predecessor

        route.reverse()
        # route now should be e.g. ['A', 'B', 'D', 'G']
        return route, minDist





 



        
        







