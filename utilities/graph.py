from collections import defaultdict
from collections import deque
import sys


class Graph:
    def __init__(self):
        self.vertexes = []
        self.edges = defaultdict(list)

    def add_vertex(self, vertex):
        if vertex not in self.vertexes:
            self.vertexes.append(vertex)

    def add_edge(self, vertex1, vertex2):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        if vertex1 not in self.edges:
            self.edges[vertex1] = []
        self.edges[vertex1].append(vertex2)

    def __str__(self):
        res = ""
        for src_vertex, vertexes in self.edges.items():
            for vertex in vertexes:
                res += str(src_vertex) + "<->" + str(vertex) + "\n"
        return res

    def distance(self, start, end, max_distance=sys.maxsize):
        queue = deque([(start, 0)])
        visited = set()
        while queue:
            node, distance = queue.popleft()
            if distance > 10:
                return float('inf')
            if node in visited or max_distance < distance:
                continue
            visited.add(node)
            if node == end:
                return distance
            for adjacent in self.edges.get(node, []):
                queue.append((adjacent, distance + 1))

    def network_count(self, start, max_distance=sys.maxsize):
        queue = deque([(start, 0)])
        visited = set()
        while queue:
            node, distance = queue.popleft()
            if node in visited or max_distance < distance:
                continue
            visited.add(node)
            for adjacent in self.edges.get(node, []):
                queue.append((adjacent, distance + 1))
        return len(visited)
