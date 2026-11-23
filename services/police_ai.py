from services.graph_service import bfs, GRAPH


class PoliceAI:

    def choose_move(self, police, index, thief):

        current = police[index]

        occupied = set(police + [thief])

        occupied.remove(current)

        distances = bfs(thief)

        best_node = None
        best_distance = float("inf")

        for neighbor in GRAPH[current]:

            if neighbor in occupied:
                continue

            distance = distances.get(neighbor, float("inf"))

            if distance < best_distance:

                best_distance = distance
                best_node = neighbor

        return best_node