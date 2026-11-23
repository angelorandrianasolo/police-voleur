
import unittest

from config.board import NODE_POSITIONS
from services.graph_service import GraphService


class GraphTests(unittest.TestCase):

    def setUp(self):

        self.graph = GraphService()

    def test_number_of_vertices(self):

        self.assertEqual(
            len(NODE_POSITIONS),
            21
        )

    def test_graph_is_undirected(self):

        for node, neighbors in self.graph.graph.items():

            for neighbor in neighbors:

                self.assertIn(
                    node,
                    self.graph.graph[neighbor]
                )

    def test_center_neighbors(self):

        self.assertEqual(
            set(self.graph.get_neighbors("I")),
            {"H", "J", "K", "L"}
        )

    def test_bfs(self):

        path = self.graph.shortest_path(
            "I",
            "B"
        )

        self.assertEqual(path[0], "I")
        self.assertEqual(path[-1], "B")

    def test_distance(self):

        distance = self.graph.shortest_distance(
            "I",
            "K"
        )

        self.assertEqual(distance, 1)


if __name__ == "__main__":

    unittest.main()
