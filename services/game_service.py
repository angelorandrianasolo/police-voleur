
from config.board import INITIAL_THIEF, INITIAL_POLICE
from models.game_state import GameState


class GameService:

    # Les seules configurations qui donnent la victoire aux policiers
    POLICE_WIN_CONFIGURATIONS = {
        "E": {"A", "T", "C"},
        "B": {"D", "F", "G"},
        "O": {"M", "N", "P"},
        "R": {"O", "U", "S"},
    }

    def initial_state(self):

        return GameState(
            thief=INITIAL_THIEF,
            police=tuple(INITIAL_POLICE),
            turn="thief",
            winner=None,
            police_index=0
        )

    def check_police_victory(self, state):

        expected_police = self.POLICE_WIN_CONFIGURATIONS.get(
            state.thief
        )

        if expected_police is None:
            return False

        return set(state.police) == expected_police

    def thief_moves(self, state, graph):

        occupied = set(state.police)

        return [
            node
            for node in graph.get_neighbors(state.thief)
            if node not in occupied
        ]

    def police_moves(self, state, index, graph):

        current = state.police[index]

        occupied = set(state.police)
        occupied.discard(current)

        return [
            node
            for node in graph.get_neighbors(current)
            if node not in occupied
        ]

    def move_thief(self, state, destination, graph):

        if state.winner or state.turn != "thief":
            return state

        if destination not in self.thief_moves(state, graph):
            return state

        new_state = GameState(
            thief=destination,
            police=state.police,
            turn="police",
            winner=None,
            police_index=0
        )

        if self.check_police_victory(new_state):

            return GameState(
                thief=new_state.thief,
                police=new_state.police,
                turn=new_state.turn,
                winner="police",
                police_index=new_state.police_index
            )

        return new_state

    def move_police(self, state, destination, graph):

        if state.winner or state.turn != "police":
            return state

        index = state.police_index

        if destination not in self.police_moves(
            state, index, graph
        ):
            return state

        police = list(state.police)
        police[index] = destination

        new_state = GameState(
            thief=state.thief,
            police=tuple(police),
            turn="police",
            winner=None,
            police_index=index
        )

        # Vérifier les quatre configurations de victoire
        if self.check_police_victory(new_state):

            return GameState(
                thief=new_state.thief,
                police=new_state.police,
                turn=new_state.turn,
                winner="police",
                police_index=index
            )

        next_index = index + 1

        if next_index >= 3:

            return GameState(
                thief=new_state.thief,
                police=new_state.police,
                turn="thief",
                winner=None,
                police_index=0
            )

        return GameState(
            thief=new_state.thief,
            police=new_state.police,
            turn="police",
            winner=None,
            police_index=next_index
        )

    def finish_if_blocked(self, state, graph):

        # Le blocage du voleur ne donne plus la victoire.
        return state
