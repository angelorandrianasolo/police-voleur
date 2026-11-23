
from models.game_state import GameState


class Minimax:

    def __init__(self, graph, game, evaluation, depth=2):
        self.graph = graph
        self.game = game
        self.evaluation = evaluation
        self.depth = depth

    def police_turn(self, state, index, depth, alpha, beta):

        if state.winner:
            return self.evaluation.score(state)

        # Les trois policiers ont terminé leur tour.
        # On passe au tour suivant du voleur.
        if state.turn == "thief" or index >= 3:

            next_state = GameState(
                thief=state.thief,
                police=state.police,
                turn="thief",
                winner=state.winner,
                police_index=0
            )

            return self.search(
                next_state,
                depth - 1,
                True,
                alpha,
                beta
            )

        moves = self.game.police_moves(
            state,
            index,
            self.graph
        )

        # Si ce policier ne peut pas bouger,
        # on passe au policier suivant.
        if not moves:

            next_state = GameState(
                thief=state.thief,
                police=state.police,
                turn="police",
                winner=None,
                police_index=index + 1
            )

            return self.police_turn(
                next_state,
                index + 1,
                depth,
                alpha,
                beta
            )

        best_score = float("inf")

        for destination in moves:

            child = self.game.move_police(
                state,
                destination,
                self.graph
            )

            if child.winner:
                score = self.evaluation.score(child)

            elif child.turn == "thief":
                score = self.search(
                    child,
                    depth - 1,
                    True,
                    alpha,
                    beta
                )

            else:
                score = self.police_turn(
                    child,
                    child.police_index,
                    depth,
                    alpha,
                    beta
                )

            best_score = min(best_score, score)

            beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score

    def search(self, state, depth, maximizing, alpha, beta):

        if state.winner or depth <= 0:
            return self.evaluation.score(state)

        if maximizing:

            moves = self.game.thief_moves(
                state,
                self.graph
            )

            # Le voleur est bloqué : victoire des policiers.
            if not moves:
                return -100000

            best_score = float("-inf")

            for destination in moves:

                child = self.game.move_thief(
                    state,
                    destination,
                    self.graph
                )

                score = self.police_turn(
                    child,
                    0,
                    depth,
                    alpha,
                    beta
                )

                best_score = max(best_score, score)

                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            return best_score

        return self.police_turn(
            state,
            state.police_index,
            depth,
            alpha,
            beta
        )

    def choose_thief_move(self, state):

        moves = self.game.thief_moves(
            state,
            self.graph
        )

        if not moves:
            return None

        best_move = None
        best_score = float("-inf")

        for destination in moves:

            child = self.game.move_thief(
                state,
                destination,
                self.graph
            )

            score = self.police_turn(
                child,
                0,
                self.depth,
                float("-inf"),
                float("inf")
            )

            if score > best_score:
                best_score = score
                best_move = destination

        return best_move

    def choose_police_move(self, state):

        index = state.police_index

        if index >= 3:
            return None

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

            child = self.game.move_police(
                state,
                destination,
                self.graph
            )

            if child.winner:
                score = self.evaluation.score(child)

            elif child.turn == "thief":
                score = self.search(
                    child,
                    self.depth - 1,
                    True,
                    float("-inf"),
                    float("inf")
                )

            else:
                score = self.police_turn(
                    child,
                    child.police_index,
                    self.depth,
                    float("-inf"),
                    float("inf")
                )

            if score < best_score:
                best_score = score
                best_move = destination

        return best_move
