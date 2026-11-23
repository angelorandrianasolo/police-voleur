from collections import deque
from config.board import NODE_POSITIONS, EDGES


def build_graph():

    graph = {
        node: [] for node in NODE_POSITIONS
    }

    for a, b in EDGES:

        graph[a].append(b)
        graph[b].append(a)

    return graph


GRAPH = build_graph()


def bfs(start, graph=GRAPH):

    distances = {start: 0}

    queue = deque([start])

    while queue:

        current = queue.popleft()

        for neighbor in graph[current]:

            if neighbor not in distances:

                distances[neighbor] = distances[current] + 1

                queue.append(neighbor)

    return distances