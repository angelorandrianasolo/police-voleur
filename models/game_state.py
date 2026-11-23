class GameState:

    def __init__(self, thief, police):

        self.thief = thief
        self.police = police

        self.current_turn = "thief"
        self.finished = False
        self.winner = None

        self.message = "Au voleur de jouer"

    def occupied_nodes(self):

        return set(self.police + [self.thief])