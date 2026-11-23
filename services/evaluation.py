
class Evaluation:

    def __init__(self, graph, game):
        self.graph = graph
        self.game = game

    def score(self, state):

        if state.winner == "thief":
            return 100000

        if state.winner == "police":
            return -100000

        distances = [
            self.graph.shortest_distance(
                police,
                state.thief
            )
            for police in state.police
        ]

        nearest_distance = min(distances)

        total_distance = sum(distances)

        exits = len(
            self.game.thief_moves(state, self.graph)
        )

        # Score positif : position favorable au voleur.
        # Score négatif : position favorable aux policiers.

        return (
            nearest_distance * 8
            + total_distance * 2
            + exits * 5
        )
