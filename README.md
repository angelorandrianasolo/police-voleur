# Le voleur et les trois policiers

Petit jeu de plateau en Python avec Tkinter. Le terrain est modélisé comme un **graphe non orienté** : les croix sont les sommets et les traits entre les croix sont les arêtes.

## Prérequis

- Python 3.9 ou plus récent
- Tkinter (inclus avec Python sur Windows ; sous Fedora : `sudo dnf install python3-tkinter`)

Aucune bibliothèque Python externe n'est nécessaire.

## Lancer le jeu

Ouvrez un terminal dans le dossier du projet :

### Windows
```bash
py main.py
```

### Fedora / Linux
```bash
python3 main.py
```

## Règles intégrées

1. Le joueur contrôle le voleur rouge.
2. Les trois policiers bleus sont contrôlés par une IA simple.
3. Un pion se déplace vers un sommet directement voisin et libre.
4. Un pion ne peut pas sauter de sommet, traverser un pion ou partager une position.
5. Après le déplacement du voleur, chaque policier joue au maximum un déplacement.
6. Les policiers gagnent si le voleur n'a plus de sommet voisin libre.

## Organisation du code

```text
jeu_voleur_policiers/
├── main.py
├── config/
│   └── board.py
├── models/
│   └── game_state.py
├── services/
│   ├── graph_service.py
│   ├── game_service.py
│   └── police_ai.py
├── ui/
│   ├── board_renderer.py
│   └── game_window.py
└── tests/
    └── test_game.py
```

### Rôle des couches

- **config** : configuration fixe du plateau (sommets, coordonnées, arêtes).
- **models** : données représentant l'état de la partie.
- **services** : règles du jeu, parcours BFS et décisions de l'IA.
- **ui** : affichage Tkinter et interactions avec le joueur.
- **tests** : vérifications automatiques de quelques règles.
- **main.py** : démarre l'application.

## Lancer les tests

Depuis le dossier du projet :

```bash
python -m unittest discover -s tests -v
```

## Modifier le terrain

Pour modifier les connexions, ouvrez `config/board.py` :
- `NODE_POSITIONS` contient les identifiants et coordonnées des croix.
- `EDGES` contient les liaisons autorisées.

Chaque arête `(A, B)` autorise le déplacement de A vers B et de B vers A.

## À propos de la fidélité du plateau

Les connexions ont été retranscrites à partir de la photo et de l'accord que les traits droits et courbes sont tous des chemins autorisés. Les courbes sont dessinées en segments droits entre leurs deux extrémités, mais elles restent une seule arête du graphe. Vérifiez les connexions dans `config/board.py` si certaines croix intermédiaires de votre dessin doivent aussi être reliées.
