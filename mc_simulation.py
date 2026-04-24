#!/usr/bin/env python3
import random
from collections import defaultdict

class MonteCarlo:
    def __init__(self):
        self.sim_count = 1000000 # Anzahl Simulationen
        self.start_round = 8     # Ab dieser Runde simulieren
        self.white_bonus = 35    # Weißvorteil
        self.draw_rate = 0.6     # Remisrate
        
        # Echte Spielerelo (Stand: März 2026)
        self.players = [
            ("Sindarov", 2745),       # 0
            ("Esipenko", 2698),       # 1
            ("Bluebaum", 2698),       # 2
            ("Wei Yi", 2754),         # 3
            ("Praggnanandhaa", 2741), # 4
            ("Giri", 2753),           # 5
            ("Caruana", 2795),        # 6
            ("Nakamura", 2810)]       # 7

        # Paarungen: (weiß, schwarz, ergebnis)
        # Ergebnis: 1 = Weiß gewinnt, 0.5 = Remis, 0 = Schwarz gewinnt
        self.schedule = [
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

        # Gewinnwahrscheinlichkeit für noch nicht gespielte Partien vorberechnen
        self.win_probs = {
            i: self.calculate_probability(self.players[white][1] + self.white_bonus, self.players[black][1])
            for i, (white, black, _) in enumerate(self.schedule)
            if i // 4 + 1 >= self.start_round
        }

    def get_points(self):
        # aktuellen Punktestand für die Tabelle kalkulieren
        points = defaultdict(float)
        for i, (white, black, result) in enumerate(self.schedule):
            s_round = i // 4 + 1
            if s_round < self.start_round:
                points[white] += result
                points[black] += (1 - result)
        return points

    def calculate_probability(self, elo_a, elo_b):
        # eloformel zum Bestimmen des Erwartungswertes einer Partie
        return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    def simulate_game(self, p):        
        # 40 Prozent der Partien sind entscheidend; 60 Prozent Remis
        if random.random() > self.draw_rate:
            # Weiß/Schwarz gewinnt
            return 1.0 if random.random() < p else 0.0 
        return 0.5 # Remis

    def simulate_tournament(self):
        points = defaultdict(float)
        for i, (white, black, result) in enumerate(self.schedule):
            s_round = i // 4 + 1
            if s_round >= self.start_round:
                # Noch nicht gespielte Partien simulieren
                r = self.simulate_game(self.win_probs[i])
            else:
                # Bereits gespielt Partien
                r = result
            points[white] += r
            points[black] += (1 - r)
        # zufällig einen Führenden mit gleicher Punktzahl auswählen
        max_score = max(points.values())
        leaders = [i for i in range(len(self.players)) if points[i] == max_score]
        return random.choice(leaders)

    def run_monte_carlo(self):
        # Turnier-Sieger zählen
        wins = defaultdict(int)
        for _ in range(self.sim_count):
            wins[self.simulate_tournament()] += 1
        return wins


def main():
    # Simulation starten
    mc = MonteCarlo()
    wins = mc.run_monte_carlo()

    # Ausgabe der Daten; Tabelle
    points = mc.get_points()
    print(f"{'Spieler':<18} {'Elo':>4}  {'Punkte':>8}  {'Wahrsch.':>10}  {'Siege':>4}")
    print("-" * 52)
    for i, (name, elo) in sorted(enumerate(mc.players), key=lambda x: -wins[x[0]]):
        print(f"{name:<18} {elo:>5}  {points[i]:>6}  {wins[i]/mc.sim_count*100:>8.1f}% {wins[i]:>8}")

if __name__ == '__main__':
    main()
