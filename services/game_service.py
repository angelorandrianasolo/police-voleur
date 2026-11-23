from models.game_state import GameState

from config.board import (
    INITIAL_THIEF,
    INITIAL_POLICE,
    EDGES
)

from services.graph_service import GRAPH
from services.police_ai import PoliceAI


class GameService:

    def __init__(self):

        self.state = GameState(
            INITIAL_THIEF,
            INITIAL_POLICE.copy()
        )

        self.ai = PoliceAI()

    def legal_moves(self, position):

        occupied = self.state.occupied_nodes()

        return [
            node for node in GRAPH[position]
            if node not in occupied
        ]

    def move_thief(self, destination):

        if destination not in self.legal_moves(
            self.state.thief
        ):
            return False

        self.state.thief = destination

        self.state.current_turn = "police"

        return True

    def move_police(self):

        for index in range(3):

            destination = self.ai.choose_move(
                self.state.police,
                index,
                self.state.thief
            )

            if destination:

                self.state.police[index] = destination

        self.state.current_turn = "thief"

        if not self.legal_moves(self.state.thief):

            self.state.finished = True
            self.state.winner = "police"
            self.state.message = "Les policiers ont gagne !"