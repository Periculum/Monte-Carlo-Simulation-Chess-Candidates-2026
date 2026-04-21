#!/usr/bin/env python3
import random
from collections import defaultdict

# Echte Spielerelo vor dem Turnier (Stand: März 2026)
spieler = [
    ("Sindarov", 2745),       # 0
    ("Esipenko", 2698),       # 1
    ("Bluebaum", 2698),       # 2
    ("Wei Yi", 2754),         # 3
    ("Praggnanandhaa", 2741), # 4
    ("Giri", 2753),           # 5
    ("Caruana", 2795),        # 6
    ("Nakamura", 2810),       # 7
]

# Paarungen: (weiß, schwarz, ergebnis_weiß)
# Ergebnis: 1 = Weiß gewinnt, 0.5 = Remis, 0 = Schwarz gewinnt, None = wird noch gespielt
# Alle Ergebnisse
schedule2 = [
    # Runde 1
    (0, 1, 1.0), (2, 3, 0.5), (4, 5, 1.0), (6, 7, 1.0),
    # Runde 2
    (1, 7, 0.5), (5, 6, 0.5), (3, 4, 0.5), (0, 2, 0.5),
    # Runde 3
    (2, 1, 0.5), (4, 0, 0.0), (6, 3, 1.0), (7, 5, 0.5),
    # Runde 4
    (1, 5, 0.0), (3, 7, 0.5), (0, 6, 1.0), (2, 4, 0.5),
    # Runde 5
    (4, 1, 0.5), (6, 2, 1.0), (7, 0, 0.0), (5, 3, 0.5),
    # Runde 6
    (6, 1, 0.5), (7, 4, 0.5), (5, 2, 0.5), (3, 0, 0.0),
    # Runde 7
    (1, 3, 0.0), (0, 5, 0.5), (2, 7, 0.5), (4, 6, 0.5),
    # Runde 8
    (1, 0, 0.5), (3, 2, 0.5), (5, 4, 1.0), (7, 6, 1.0),
    # Runde 9
    (7, 1, 0.5), (6, 5, 0.0), (4, 3, 0.5), (2, 0, 0.5),
    # Runde 10
    (1, 2, 0.5), (0, 4, 1.0), (3, 6, 0.5), (5, 7, 0.5),
    # Runde 11
    (5, 1, 0.5), (7, 3, 0.5), (6, 0, 0.5), (4, 2, 0.5),
    # Runde 12
    (1, 4, 0.5), (2, 6, 0.5), (0, 7, 0.5), (3, 5, 0.5),
    # Runde 13
    (3, 1, 1.0), (5, 0, 0.5), (7, 2, 0.5), (6, 4, 0.5),
    # Runde 14
    (1, 6, 0.0), (4, 7, 0.5), (2, 5, 0.0), (0, 3, 0.5),
]
# Turnier nach der Hälfte der Spiele
schedule = [
    # Runde 1
    (0, 1, 1.0), (2, 3, 0.5), (4, 5, 1.0), (6, 7, 1.0),
    # Runde 2
    (1, 7, 0.5), (5, 6, 0.5), (3, 4, 0.5), (0, 2, 0.5),
    # Runde 3
    (2, 1, 0.5), (4, 0, 0.0), (6, 3, 1.0), (7, 5, 0.5),
    # Runde 4
    (1, 5, 0.0), (3, 7, 0.5), (0, 6, 1.0), (2, 4, 0.5),
    # Runde 5
    (4, 1, 0.5), (6, 2, 1.0), (7, 0, 0.0), (5, 3, 0.5),
    # Runde 6
    (6, 1, 0.5), (7, 4, 0.5), (5, 2, 0.5), (3, 0, 0.0),
    # Runde 7
    (1, 3, 0.0), (0, 5, 0.5), (2, 7, 0.5), (4, 6, 0.5),
    # Runde 8
    (1, 0, None), (3, 2, None), (5, 4, None), (7, 6, None),
    # Runde 9
    (7, 1, None), (6, 5, None), (4, 3, None), (2, 0, None),
    # Runde 10
    (1, 2, None), (0, 4, None), (3, 6, None), (5, 7, None),
    # Runde 11
    (5, 1, None), (7, 3, None), (6, 0, None), (4, 2, None),
    # Runde 12
    (1, 4, None), (2, 6, None), (0, 7, None), (3, 5, None),
    # Runde 13
    (3, 1, None), (5, 0, None), (7, 2, None), (6, 4, None),
    # Runde 14
    (1, 6, None), (4, 7, None), (2, 5, None), (0, 3, None),
]
# Turnier zu Beginn
schedule2 = [
    # Runde 1
    (0, 1, None), (2, 3, None), (4, 5, None), (6, 7, None),
    # Runde 2
    (1, 7, None), (5, 6, None), (3, 4, None), (0, 2, None),
    # Runde 3
    (2, 1, None), (4, 0, None), (6, 3, None), (7, 5, None),
    # Runde 4
    (1, 5, None), (3, 7, None), (0, 6, None), (2, 4, None),
    # Runde 5
    (4, 1, None), (6, 2, None), (7, 0, None), (5, 3, None),
    # Runde 6
    (6, 1, None), (7, 4, None), (5, 2, None), (3, 0, None),
    # Runde 7
    (1, 3, None), (0, 5, None), (2, 7, None), (4, 6, None),
    # Runde 8
    (1, 0, None), (3, 2, None), (5, 4, None), (7, 6, None),
    # Runde 9
    (7, 1, None), (6, 5, None), (4, 3, None), (2, 0, None),
    # Runde 10
    (1, 2, None), (0, 4, None), (3, 6, None), (5, 7, None),
    # Runde 11
    (5, 1, None), (7, 3, None), (6, 0, None), (4, 2, None),
    # Runde 12
    (1, 4, None), (2, 6, None), (0, 7, None), (3, 5, None),
    # Runde 13
    (3, 1, None), (5, 0, None), (7, 2, None), (6, 4, None),
    # Runde 14
    (1, 6, None), (4, 7, None), (2, 5, None), (0, 3, None),
]

def calculate_probability(elo_a, elo_b):
    # eloformel zum Bestimmen des Erwartungswertes einer Partie
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

def simulate_game(elo_a, elo_b):
    elo_a += 35 #Weißvorteil
    p = calculate_probability(elo_a, elo_b)
    
    # 40 Prozent der Partien sind entscheidend; 60 Prozent Remis
    if random.random() > 0.60:          
        if random.random() < p:
            return 1.0 # Weiß gewinnt
        else:
            return 0.0 # Schwarz gewinnt
    else:
        return 0.5 # Remis

def simulate_tournament():
    points = defaultdict(float)
    for white, black, result in schedule:
        if result is None:
            # Noch nicht gespielte Partien simulieren
            w = simulate_game(spieler[white][1], spieler[black][1])
        else:
            # Bereits gespielt Partien
            w = result
        points[white] += w
        points[black] += (1 - w)
    # zufällig einen Führenden mit gleicher Punktzahl auswählen
    max_score = max(points.values())
    leaders = [i for i in range(len(spieler)) if points[i] == max_score]
    return random.choice(leaders)

# Monte-Carlo
N = 1000000 # Anzahl Simulationen
wins = defaultdict(int)
for _ in range(N):
    wins[simulate_tournament()] += 1

# aktuelle Punktzahl
stand = defaultdict(float)
for white, black, result in schedule:
    if result is not None:
        stand[white] += result
        stand[black] += (1 - result)

# Ausgabe der Daten; Tabelle
print(f"{'Spieler':<18} {'Elo':>4}  {'Punkte':>8}  {'Wahrsch.':>10}  {'Siege':>4}")
print("-" * 52)
for i, (name, elo) in sorted(enumerate(spieler), key=lambda x: -wins[x[0]]):
    print(f"{name:<18} {elo:>5}  {stand[i]:>6}  {wins[i]/N*100:>8.1f}% {wins[i]:>8}")
