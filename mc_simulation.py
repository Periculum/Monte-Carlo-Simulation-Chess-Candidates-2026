#!/usr/bin/env python3
import random
from collections import defaultdict

N = 1000000      # Anzahl Simulationen
start_round = 7  # Ab dieser Runde simulieren

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

def simulate_tournament(s_round):
    points = defaultdict(float)
    for i, (white, black, result) in enumerate(schedule):
        round = i // 4 + 1
        if round >= s_round:
            # Noch nicht gespielte Partien simulieren
            r = simulate_game(spieler[white][1], spieler[black][1])
        else:
            # Bereits gespielt Partien
            r = result
        points[white] += r
        points[black] += (1 - r)
    # zufällig einen Führenden mit gleicher Punktzahl auswählen
    max_score = max(points.values())
    leaders = [i for i in range(len(spieler)) if points[i] == max_score]
    return random.choice(leaders)

# Monte-Carlo
wins = defaultdict(int)
for _ in range(N):
    wins[simulate_tournament(start_round)] += 1

# aktuelle Punktzahl
stand = defaultdict(float)
for i, (white, black, result) in enumerate(schedule):
    round = i // 4 + 1
    if round < start_round:
        stand[white] += result
        stand[black] += (1 - result)

# Ausgabe der Daten; Tabelle
print(f"{'Spieler':<18} {'Elo':>4}  {'Punkte':>8}  {'Wahrsch.':>10}  {'Siege':>4}")
print("-" * 52)
for i, (name, elo) in sorted(enumerate(spieler), key=lambda x: -wins[x[0]]):
    print(f"{name:<18} {elo:>5}  {stand[i]:>6}  {wins[i]/N*100:>8.1f}% {wins[i]:>8}")
