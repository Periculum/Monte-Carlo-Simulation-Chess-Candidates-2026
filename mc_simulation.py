#!/usr/bin/env python3
import random
from collections import defaultdict

class MonteCarlo:
    def __init__(self):
        self.sim_count = 1000000  # Number of simulations
        self.start_round = 8      # Simulate from this round onwards
        self.white_bonus = 35     # White player advantage
        self.draw_rate = 0.6      # Draw rate

        # Player Elo ratings (as of March 2026)
        self.players = [
            ("Sindarov", 2745),       # 0
            ("Esipenko", 2698),       # 1
            ("Bluebaum", 2698),       # 2
            ("Wei Yi", 2754),         # 3
            ("Praggnanandhaa", 2741), # 4
            ("Giri", 2753),           # 5
            ("Caruana", 2795),        # 6
            ("Nakamura", 2810)]       # 7

        # Pairings: (white, black, result)
        # Result: 1 = white wins, 0.5 = draw, 0 = black wins
        self.schedule = [
            # Round 1
            (0, 1, 1.0), (2, 3, 0.5), (4, 5, 1.0), (6, 7, 1.0),
            # Round 2
            (1, 7, 0.5), (5, 6, 0.5), (3, 4, 0.5), (0, 2, 0.5),
            # Round 3
            (2, 1, 0.5), (4, 0, 0.0), (6, 3, 1.0), (7, 5, 0.5),
            # Round 4
            (1, 5, 0.0), (3, 7, 0.5), (0, 6, 1.0), (2, 4, 0.5),
            # Round 5
            (4, 1, 0.5), (6, 2, 1.0), (7, 0, 0.0), (5, 3, 0.5),
            # Round 6
            (6, 1, 0.5), (7, 4, 0.5), (5, 2, 0.5), (3, 0, 0.0),
            # Round 7
            (1, 3, 0.0), (0, 5, 0.5), (2, 7, 0.5), (4, 6, 0.5),
            # Round 8
            (1, 0, 0.5), (3, 2, 0.5), (5, 4, 1.0), (7, 6, 1.0),
            # Round 9
            (7, 1, 0.5), (6, 5, 0.0), (4, 3, 0.5), (2, 0, 0.5),
            # Round 10
            (1, 2, 0.5), (0, 4, 1.0), (3, 6, 0.5), (5, 7, 0.5),
            # Round 11
            (5, 1, 0.5), (7, 3, 0.5), (6, 0, 0.5), (4, 2, 0.5),
            # Round 12
            (1, 4, 0.5), (2, 6, 0.5), (0, 7, 0.5), (3, 5, 0.5),
            # Round 13
            (3, 1, 1.0), (5, 0, 0.5), (7, 2, 0.5), (6, 4, 0.5),
            # Round 14
            (1, 6, 0.0), (4, 7, 0.5), (2, 5, 0.0), (0, 3, 0.5),
        ]

        # Pre-calculate win probabilities for games to be simulated
        self.win_probs = {
            i: self.calculate_probability(self.players[white][1] + self.white_bonus, self.players[black][1])
            for i, (white, black, _) in enumerate(self.schedule)
            if i // 4 + 1 >= self.start_round
        }

    def get_points(self):
        # Calculate current standings based on completed games
        points = defaultdict(float)
        for i, (white, black, result) in enumerate(self.schedule):
            s_round = i // 4 + 1
            if s_round < self.start_round:
                points[white] += result
                points[black] += (1 - result)
        return points

    def calculate_probability(self, elo_a, elo_b):
        # Elo formula to determine the expected score of a game
        return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    def simulate_game(self, p):
        # 40% of games are decisive; 60% are draws
        if random.random() > self.draw_rate:
            # White or black wins
            return 1.0 if random.random() < p else 0.0
        return 0.5  # Draw

    def simulate_tournament(self):
        points = defaultdict(float)
        for i, (white, black, result) in enumerate(self.schedule):
            s_round = i // 4 + 1
            if s_round >= self.start_round:
                # Simulate games not yet played
                r = self.simulate_game(self.win_probs[i])
            else:
                # Use real result for completed games
                r = result
            points[white] += r
            points[black] += (1 - r)
        # Randomly pick a winner in case of a tie
        max_score = max(points.values())
        leaders = [i for i in range(len(self.players)) if points[i] == max_score]
        return random.choice(leaders)

    def run_monte_carlo(self):
        # Count tournament winners across all simulations
        wins = defaultdict(int)
        for _ in range(self.sim_count):
            wins[self.simulate_tournament()] += 1
        return wins


def main():
    # Run simulation
    mc = MonteCarlo()
    wins = mc.run_monte_carlo()

    # Print results table
    points = mc.get_points()
    print(f"{'Player':<18} {'Elo':>4}  {'Points':>8}  {'Probability':>11}  {'Wins':>4}")
    print("-" * 54)
    for i, (name, elo) in sorted(enumerate(mc.players), key=lambda x: -wins[x[0]]):
        print(f"{name:<18} {elo:>5}  {points[i]:>6}  {wins[i]/mc.sim_count*100:>9.1f}% {wins[i]:>8}")

if __name__ == '__main__':
    main()
