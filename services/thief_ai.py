
class ThiefAI:

    def __init__(self, graph, game, minimax):

        self.graph = graph
        self.game = game
        self.minimax = minimax

    def choose_move(self, state):

        move = self.minimax.choose_thief_move(state)

        if move is not None:
            return move

        # Repli stratégique basé sur BFS.
        moves = self.game.thief_moves(
            state,
            self.graph
        )

        if not moves:
            return None

        return max(
            moves,
            key=lambda node: (
                min(
                    self.graph.shortest_distance(
                        node,
                        police
                    )
                    for police in state.police
                ),
                self.graph.degree(node)
            )
        )
