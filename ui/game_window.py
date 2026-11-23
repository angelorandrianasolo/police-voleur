
import tkinter as tk
from tkinter import messagebox

from config.board import BOARD_WIDTH, BOARD_HEIGHT

from models.game_state import GameState

from services.graph_service import GraphService
from services.game_service import GameService
from services.evaluation import Evaluation
from services.minimax import Minimax
from services.police_ai import PoliceAI
from services.thief_ai import ThiefAI

from ui.board_renderer import BoardRenderer


class GameWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Police-Voleur - Intelligence Artificielle"
        )

        self.root.resizable(False, False)

        # ==============================
        # INITIALISATION DES SERVICES
        # ==============================

        self.graph = GraphService()
        self.game = GameService()

        self.evaluation = Evaluation(
            self.graph,
            self.game
        )

        self.minimax = Minimax(
            self.graph,
            self.game,
            self.evaluation,
            depth=2
        )

        self.police_ai = PoliceAI(
            self.graph,
            self.game,
            self.minimax
        )

        self.thief_ai = ThiefAI(
            self.graph,
            self.game,
            self.minimax
        )

        # ==============================
        # ÉTAT DE LA PARTIE
        # ==============================

        self.state = self.game.initial_state()

        self.mode = tk.StringVar(value="both")

        self.paused = True
        self.after_id = None

        # ==============================
        # PLATEAU DE JEU
        # ==============================

        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg="white",
            highlightthickness=0
        )

        self.canvas.grid(
            row=0,
            column=0,
            rowspan=10,
            padx=10,
            pady=10
        )

        self.renderer = BoardRenderer(
            self.canvas,
            self.on_node_click
        )

        # ==============================
        # PANNEAU DE COMMANDES
        # ==============================

        panel = tk.Frame(
            self.root,
            padx=15,
            pady=15
        )

        panel.grid(
            row=0,
            column=1,
            sticky="n"
        )

        tk.Label(
            panel,
            text="POLICE - VOLEUR",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(
            panel,
            text="Mode de jeu"
        ).pack(anchor="w")

        tk.Radiobutton(
            panel,
            text="IA contre IA",
            variable=self.mode,
            value="both",
            command=self.change_mode
        ).pack(anchor="w")

        tk.Radiobutton(
            panel,
            text="Je contrôle le voleur",
            variable=self.mode,
            value="thief",
            command=self.change_mode
        ).pack(anchor="w")

        tk.Radiobutton(
            panel,
            text="Je contrôle les policiers",
            variable=self.mode,
            value="police",
            command=self.change_mode
        ).pack(anchor="w")

        self.status = tk.Label(
            panel,
            text="",
            justify="left",
            wraplength=220,
            font=("Arial", 10)
        )

        self.status.pack(pady=15)

        tk.Button(
            panel,
            text="Démarrer",
            width=22,
            command=self.start
        ).pack(pady=5)

        tk.Button(
            panel,
            text="Pause",
            width=22,
            command=self.pause
        ).pack(pady=5)

        tk.Button(
            panel,
            text="Recommencer",
            width=22,
            command=self.reset
        ).pack(pady=5)

        tk.Button(
            panel,
            text="Liste d'adjacence",
            width=22,
            command=self.show_graph
        ).pack(pady=5)

        tk.Label(
            panel,
            text=(
                "Rouge : voleur\n"
                "Bleu : policiers\n"
                "Vert : déplacements possibles"
            ),
            justify="left"
        ).pack(pady=20)

        self.refresh()

    # ==============================
    # CHANGEMENT DE MODE
    # ==============================

    def change_mode(self):

        self.pause()
        self.refresh()

    # ==============================
    # ACTUALISATION DU PLATEAU
    # ==============================

    def refresh(self):

        legal_moves = []

        if self.state.turn == "thief":

            legal_moves = self.game.thief_moves(
                self.state,
                self.graph
            )

        elif self.state.turn == "police":

            index = self.state.police_index

            if index < 3:

                legal_moves = self.game.police_moves(
                    self.state,
                    index,
                    self.graph
                )

        self.renderer.draw_pieces(
            self.state,
            legal_moves
        )

        if self.state.winner:

            winner = (
                "Le voleur"
                if self.state.winner == "thief"
                else "Les policiers"
            )

            self.status.config(
                text=(
                    "PARTIE TERMINÉE !\n\n"
                    f"Gagnant : {winner}"
                )
            )

        else:

            if self.state.turn == "thief":
                turn = "Voleur"
            else:
                turn = (
                    f"Policier "
                    f"{self.state.police_index + 1}"
                )

            self.status.config(
                text=(
                    f"Tour : {turn}\n\n"
                    f"Voleur : {self.state.thief}\n"
                    f"Policiers : "
                    f"{', '.join(self.state.police)}"
                )
            )

    # ==============================
    # DÉPLACEMENT MANUEL
    # ==============================

    def on_node_click(self, node):

        if self.paused or self.state.winner:
            return

        mode = self.mode.get()

        # IA contre IA : aucun déplacement manuel.
        if mode == "both":
            return

        # Joueur contrôle le voleur.
        if mode == "thief" and self.state.turn == "thief":

            moves = self.game.thief_moves(
                self.state,
                self.graph
            )

            if node not in moves:
                return

            self.state = self.game.move_thief(
                self.state,
                node,
                self.graph
            )

            self.refresh()
            self.schedule_ai()

        # Joueur contrôle les policiers.
        elif mode == "police" and self.state.turn == "police":

            index = self.state.police_index

            moves = self.game.police_moves(
                self.state,
                index,
                self.graph
            )

            if node not in moves:
                return

            self.state = self.game.move_police(
                self.state,
                node,
                self.graph
            )

            self.state = self.game.finish_if_blocked(
                self.state,
                self.graph
            )

            self.refresh()

            if (
                not self.state.winner
                and self.state.turn == "thief"
            ):
                self.schedule_ai()

    # ==============================
    # PROGRAMMATION DU PROCHAIN TOUR
    # ==============================

    def schedule_ai(self):

        if self.paused or self.state.winner:
            return

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        self.after_id = self.root.after(
            400,
            self.ai_step
        )

    # ==============================
    # PASSAGE AU POLICIER SUIVANT
    # ==============================

    def skip_police(self):

        index = self.state.police_index + 1

        if index >= 3:

            self.state = GameState(
                thief=self.state.thief,
                police=self.state.police,
                turn="thief",
                winner=None,
                police_index=0
            )

        else:

            self.state = GameState(
                thief=self.state.thief,
                police=self.state.police,
                turn="police",
                winner=None,
                police_index=index
            )

    # ==============================
    # EXÉCUTION DE L'IA
    # ==============================

    def ai_step(self):

        self.after_id = None

        if self.paused or self.state.winner:
            return

        mode = self.mode.get()

        # ==========================
        # TOUR DU VOLEUR
        # ==========================

        if self.state.turn == "thief":

            if mode in ("both", "police"):

                destination = self.thief_ai.choose_move(
                    self.state
                )

                if destination is None:

                    self.state = self.game.finish_if_blocked(
                        self.state,
                        self.graph
                    )

                else:

                    self.state = self.game.move_thief(
                        self.state,
                        destination,
                        self.graph
                    )

        # ==========================
        # TOUR DES POLICIERS
        # ==========================

        elif self.state.turn == "police":

            if mode in ("both", "thief"):

                index = self.state.police_index

                moves = self.game.police_moves(
                    self.state,
                    index,
                    self.graph
                )

                if not moves:

                    self.skip_police()

                else:

                    destination = self.police_ai.choose_move(
                        self.state
                    )

                    if destination is None:

                        self.skip_police()

                    else:

                        self.state = self.game.move_police(
                            self.state,
                            destination,
                            self.graph
                        )

        # Vérifier si le voleur est bloqué.
        self.state = self.game.finish_if_blocked(
            self.state,
            self.graph
        )

        # Actualiser les positions.
        self.refresh()

        # Programmer le prochain déplacement.
        if not self.state.winner:

            if mode == "both":
                self.schedule_ai()

            elif (
                mode == "thief"
                and self.state.turn == "police"
            ):
                self.schedule_ai()

            elif (
                mode == "police"
                and self.state.turn == "thief"
            ):
                self.schedule_ai()

    # ==============================
    # DÉMARRER
    # ==============================

    def start(self):

        if self.state.winner:
            return

        self.paused = False

        self.schedule_ai()

    # ==============================
    # PAUSE
    # ==============================

    def pause(self):

        self.paused = True

        if self.after_id is not None:

            self.root.after_cancel(
                self.after_id
            )

            self.after_id = None

    # ==============================
    # RECOMMENCER
    # ==============================

    def reset(self):

        self.pause()

        self.state = self.game.initial_state()

        self.refresh()

        if self.mode.get() == "both":
            self.start()

    # ==============================
    # AFFICHER LE GRAPHE
    # ==============================

    def show_graph(self):

        lines = []

        for node in sorted(self.graph.graph):

            neighbors = self.graph.get_neighbors(
                node
            )

            lines.append(
                f"{node} : {', '.join(neighbors)}"
            )

        messagebox.showinfo(
            "Liste d'adjacence",
            "\n".join(lines)
        )

    # ==============================
    # LANCEMENT DE L'APPLICATION
    # ==============================

    def run(self):

        self.root.mainloop()
