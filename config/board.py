# Coordonnees des 19 sommets
NODE_POSITIONS = {
    "A": (270, 85),
    "B": (400, 95),
    "C": (545, 115),

    "D": (70, 260),
    "E": (65, 405),
    "F": (145, 405),
    "G": (85, 500),

    "H": (310, 405),
    "I": (400, 405),
    "J": (490, 405),
    "K": (400, 285),
    "L": (400, 520),

    "M": (400, 600),
    "N": (220, 685),
    "O": (390, 745),
    "P": (550, 705),

    "Q": (690, 500),
    "R": (720, 405),
    "S": (680, 270),
}

# Connexions du graphe non oriente
EDGES = [
    # Contour exterieur
    ("A", "B"), ("B", "C"),
    ("C", "S"), ("S", "R"),
    ("R", "Q"), ("Q", "P"),
    ("P", "O"), ("O", "N"),
    ("N", "G"), ("G", "E"),
    ("E", "D"), ("D", "A"),

    # Courbes exterieures
    ("A", "C"),
    ("D", "G"),
    ("S", "Q"),
    ("N", "P"),

    # Axe horizontal
    ("E", "F"),
    ("F", "H"),
    ("H", "I"),
    ("I", "J"),
    ("J", "R"),

    # Axe vertical
    ("B", "K"),
    ("K", "I"),
    ("I", "L"),
    ("L", "M"),
    ("M", "O"),

    # Cercle central
    ("K", "J"),
    ("J", "L"),
    ("L", "H"),
    ("H", "K"),
]

BOARD_WIDTH = 790
BOARD_HEIGHT = 830

INITIAL_THIEF = "I"
INITIAL_POLICE = ["B", "E", "R"]