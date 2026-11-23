
from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    thief: str
    police: tuple
    turn: str = "thief"
    winner: str | None = None
    police_index: int = 0
