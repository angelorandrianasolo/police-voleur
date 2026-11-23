"""Tests simples des règles et du graphe."""
import unittest

from config.board import NODE_POSITIONS
from services.graph_service import GRAPH
from services.game_service import GameService


class GameTests(unittest.TestCase):
    def test_plateau_contient_19_sommets(self):
        self.assertEqual(len(NODE_POSITIONS), 19)
        self.assertEqual(len(GRAPH), 19)

    def test_graphe_non_oriente(self):
        for node, neighbors in GRAPH.items():
            for neighbor in neighbors:
                self.assertIn(node, GRAPH[neighbor])

    def test_deplacement_sur_une_arete(self):
        game = GameService()
        start = game.state.thief
        legal = game.get_legal_thief_moves()
        self.assertTrue(legal)

        destination = legal[0]
        success, _ = game.move_thief(destination)
        self.assertTrue(success)
        self.assertEqual(game.state.thief, destination)
        self.assertIn(destination, GRAPH[start])

    def test_impossible_de_sauter(self):
        game = GameService()
        success, _ = game.move_thief("A")
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
