
from collections import deque

from config.board import NODE_POSITIONS, BOARD_PATHS


class GraphService:

    def __init__(self):
        self.graph = self.build_graph()

    def build_graph(self):
        graph = {
            node: set()
            for node in NODE_POSITIONS
        }

        for path in BOARD_PATHS:
            for i in range(len(path) - 1):

                first = path[i]
                second = path[i + 1]

                if first not in graph or second not in graph:
                    raise ValueError(
                        f"Sommet inconnu : {first} ou {second}"
                    )

                graph[first].add(second)
                graph[second].add(first)

        return graph

    def get_neighbors(self, node):
        return sorted(self.graph.get(node, set()))

    def are_connected(self, first, second):
        return second in self.graph.get(first, set())

    def degree(self, node):
        return len(self.graph.get(node, set()))

    def bfs(self, start):
        if start not in self.graph:
            return {}

        distances = {start: 0}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            for neighbor in self.get_neighbors(current):

                if neighbor not in distances:

                    distances[neighbor] = (
                        distances[current] + 1
                    )

                    queue.append(neighbor)

        return distances

    def shortest_distance(self, start, destination):
        distances = self.bfs(start)

        return distances.get(
            destination,
            float("inf")
        )

    def shortest_path(self, start, destination):

        if start not in self.graph:
            return []

        if destination not in self.graph:
            return []

        queue = deque([start])

        parents = {
            start: None
        }

        while queue:

            current = queue.popleft()

            if current == destination:
                break

            for neighbor in self.get_neighbors(current):

                if neighbor not in parents:

                    parents[neighbor] = current
                    queue.append(neighbor)

        if destination not in parents:
            return []

        path = []
        current = destination

        while current is not None:

            path.append(current)
            current = parents[current]

        return list(reversed(path))

    def adjacency_matrix(self):

        nodes = sorted(self.graph)

        matrix = []

        for first in nodes:

            row = []

            for second in nodes:

                row.append(
                    1 if second in self.graph[first] else 0
                )

            matrix.append(row)

        return nodes, matrix

    def display_graph(self):

        for node in sorted(self.graph):

            print(
                f"{node} : {self.get_neighbors(node)}"
            )
