
"""
Configuration du plateau Police-Voleur.
Le plateau possède 21 sommets.
"""

BOARD_WIDTH = 820
BOARD_HEIGHT = 820

NODE_POSITIONS = {
    # Grand cercle extérieur
    "A": (250, 140),
    "B": (410, 110),
    "C": (570, 140),
    "S": (680, 250),
    "R": (710, 410),
    "Q": (680, 570),
    "P": (570, 680),
    "O": (410, 710),
    "N": (250, 680),
    "G": (140, 570),
    "E": (110, 410),
    "D": (140, 250),

    # Sommets des quatre courbes
    "T": (410, 235),
    "U": (585, 410),
    "M": (410, 585),
    "F": (235, 410),

    # Cercle intérieur
    "K": (410, 310),
    "J": (510, 410),
    "L": (410, 510),
    "H": (310, 410),

    # Centre
    "I": (410, 410),
}

OUTER_CIRCLE = [
    "A", "B", "C", "S", "R", "Q",
    "P", "O", "N", "G", "E", "D", "A"
]

INNER_CIRCLE = [
    "K", "J", "L", "H", "K"
]

CURVED_PATHS = [
    ["A", "T", "C"],
    ["D", "F", "G"],
    ["S", "U", "Q"],
    ["N", "M", "P"],
]

STRAIGHT_PATHS = [
    ["B", "T", "K", "I", "L", "M", "O"],
    ["E", "F", "H", "I", "J", "U", "R"],
]

BOARD_PATHS = [
    OUTER_CIRCLE,
    INNER_CIRCLE,
] + CURVED_PATHS + STRAIGHT_PATHS

INITIAL_THIEF = "I"

INITIAL_POLICE = [
    "B",
    "E",
    "R",
]
