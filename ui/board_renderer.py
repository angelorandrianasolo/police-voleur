
import tkinter as tk

from config.board import (
    NODE_POSITIONS,
    CURVED_PATHS,
    BOARD_WIDTH,
    BOARD_HEIGHT
)


class BoardRenderer:

    def __init__(self, canvas, on_node_click):

        self.canvas = canvas
        self.on_node_click = on_node_click

        self.draw_board()

    def draw_curved_path(self, names):

        points = [
            coordinate
            for name in names
            for coordinate in NODE_POSITIONS[name]
        ]

        self.canvas.create_line(
            *points,
            fill="#64748b",
            width=3,
            smooth=True,
            splinesteps=30
        )

    def draw_board(self):

        self.canvas.delete("all")

        # Cercle extérieur
        self.canvas.create_oval(
            110, 110, 710, 710,
            outline="#34465e",
            width=4
        )

        # Cercle intérieur
        self.canvas.create_oval(
            310, 310, 510, 510,
            outline="#34465e",
            width=4
        )

        # Courbes
        for path in CURVED_PATHS:
            self.draw_curved_path(path)

        # Axes droits
        self.canvas.create_line(
            410, 110, 410, 710,
            fill="#64748b",
            width=3
        )

        self.canvas.create_line(
            110, 410, 710, 410,
            fill="#64748b",
            width=3
        )

        # Sommets
        for name, (x, y) in NODE_POSITIONS.items():

            r = 17

            self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill="#f1f5f9",
                outline="#34465e",
                width=2,
                tags=(f"node_{name}",)
            )

            self.canvas.create_text(
                x, y,
                text=name,
                font=("Arial", 9, "bold"),
                fill="#1e293b",
                tags=(f"node_{name}",)
            )

            self.canvas.tag_bind(
                f"node_{name}",
                "<Button-1>",
                lambda event, node=name:
                    self.on_node_click(node)
            )

    def draw_pieces(self, state, legal_moves=None):

        self.canvas.delete("pieces")
        self.canvas.delete("hints")

        legal_moves = legal_moves or []

        # Cases accessibles
        for node in legal_moves:

            x, y = NODE_POSITIONS[node]

            self.canvas.create_oval(
                x-23, y-23, x+23, y+23,
                outline="#16a34a",
                width=3,
                tags="hints"
            )

        # Policiers
        for index, node in enumerate(state.police):

            x, y = NODE_POSITIONS[node]

            self.canvas.create_oval(
                x-14, y-14, x+14, y+14,
                fill="#2563eb",
                outline="white",
                width=2,
                tags="pieces"
            )

            self.canvas.create_text(
                x, y,
                text=str(index + 1),
                fill="white",
                font=("Arial", 9, "bold"),
                tags="pieces"
            )

        # Voleur
        x, y = NODE_POSITIONS[state.thief]

        self.canvas.create_oval(
            x-15, y-15, x+15, y+15,
            fill="#dc2626",
            outline="white",
            width=2,
            tags="pieces"
        )

        self.canvas.create_text(
            x, y,
            text="V",
            fill="white",
            font=("Arial", 9, "bold"),
            tags="pieces"
        )
