import tkinter as tk

from config.board import NODE_POSITIONS, EDGES


class BoardRenderer:

    def __init__(self, canvas):

        self.canvas = canvas

    def draw(self, state, legal_moves):

        self.canvas.delete("all")

        # Grand cercle exterieur
        self.canvas.create_oval(
            65, 100, 735, 750,
            outline="#777777",
            width=3
        )

        # Cercle central
        self.canvas.create_oval(
            300, 300, 500, 510,
            outline="#777777",
            width=3
        )

        # Cercles lateraux
        self.canvas.create_oval(
            40, 330, 160, 475,
            outline="#777777",
            width=3
        )

        self.canvas.create_oval(
            640, 330, 760, 475,
            outline="#777777",
            width=3
        )

        # Cercle du haut
        self.canvas.create_oval(
            270, 50, 550, 190,
            outline="#777777",
            width=3
        )

        # Cercle du bas
        self.canvas.create_oval(
            220, 650, 570, 780,
            outline="#777777",
            width=3
        )

        # Axes horizontaux et verticaux
        self.canvas.create_line(
            65, 405, 735, 405,
            fill="#777777",
            width=2
        )

        self.canvas.create_line(
            400, 95, 400, 745,
            fill="#777777",
            width=2
        )

        # Dessiner les points
        for node, (x, y) in NODE_POSITIONS.items():

            self.canvas.create_oval(
                x-6, y-6,
                x+6, y+6,
                fill="white",
                outline="black"
            )

        # Destinations autorisees
        for node in legal_moves:

            x, y = NODE_POSITIONS[node]

            self.canvas.create_oval(
                x-19, y-19,
                x+19, y+19,
                outline="green",
                width=3
            )

        # Dessiner les policiers
        for index, node in enumerate(state.police):

            self.draw_piece(node, "blue", str(index+1))

        # Dessiner le voleur
        self.draw_piece(state.thief, "red", "V")

    def draw_piece(self, node, color, label):

        x, y = NODE_POSITIONS[node]

        self.canvas.create_oval(
            x-15, y-15,
            x+15, y+15,
            fill=color,
            outline="black",
            width=2
        )

        self.canvas.create_text(
            x, y,
            text=label,
            fill="white",
            font=("Arial", 10, "bold")
        )