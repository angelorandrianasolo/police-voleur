
class PoliceAI:

    def __init__(self, graph, game, minimax):
        self.graph = graph
        self.game = game
        self.minimax = minimax

    def choose_move(self, state):

        # Essayer d'abord Minimax
        move = self.minimax.choose_police_move(state)

        if move is not None:
            return move

        # Si Minimax ne trouve aucun mouvement,
        # utiliser BFS pour se rapprocher du voleur.

        index = state.police_index

        moves = self.game.police_moves(
            state,
            index,
            self.graph
        )

        if not moves:
            return None

        best_move = None
        best_score = float("inf")

        for destination in moves:

            distance = self.graph.shortest_distance(
                destination,
                state.thief
            )

            score = (
                distance * 10
                - self.graph.degree(destination)
            )

            if score < best_score:
                best_score = score
                best_move = destination

        return best_move
