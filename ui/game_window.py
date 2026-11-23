import tkinter as tk

from config.board import (
    BOARD_WIDTH,
    BOARD_HEIGHT,
    NODE_POSITIONS
)

from services.game_service import GameService
from ui.board_renderer import BoardRenderer


class GameWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Voleur et policiers")

        self.game = GameService()

        self.canvas = tk.Canvas(
            root,
            width=BOARD_WIDTH,
            height=BOARD_HEIGHT,
            bg="white"
        )

        self.canvas.pack(padx=10, pady=10)

        self.renderer = BoardRenderer(self.canvas)

        self.canvas.bind(
            "<Button-1>",
            self.on_click
        )

        self.refresh()

    def refresh(self):

        legal_moves = self.game.legal_moves(
            self.game.state.thief
        )

        self.renderer.draw(
            self.game.state,
            legal_moves
        )

    def on_click(self, event):

        for node, (x, y) in NODE_POSITIONS.items():

            distance = (
                (event.x-x)**2 +
                (event.y-y)**2
            )**0.5

            if distance <= 20:

                if self.game.move_thief(node):

                    self.refresh()

                    self.root.after(
                        400,
                        self.play_police
                    )

                break

    def play_police(self):

        self.game.move_police()

        self.refresh()