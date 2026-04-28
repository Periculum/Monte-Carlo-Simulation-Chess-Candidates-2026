# Monte-Carlo-Simulation of the Chess-Candidates-2026
A simple Monte Carlo simulation of the 2026 FIDE Candidates Tournament, written for a c't article on Monte Carlo Simulations. The Article was published online on heise+.

## How it works

All player Elo ratings (March 2026) and pairings are hardcoded. The simulation uses the standard Elo formula to calculate win probabilities, then runs the remaining rounds a million times to estimate each player's
chances of winning the tournament.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `sim_count` | 1,000,000 | Number of simulations to run |
| `start_round` | 8 | Simulate from this round onwards; earlier rounds use real results |
| `white_bonus` | 35 | Elo bonus for the white player (see [Sonas, 2002](https://en.chessbase.com/post/the-sonas-rating-formula-better-than-elo)) |
| `draw_rate` | 0.60 | Probability of a draw |

The draw rate of 60% is derived from all Candidates Tournament games since 2013: 392 games, 236 draws, 156 decisive results.

## Results

For the default settings the Model produced these results:
```
Player              Elo    Points  Probability  Wins
------------------------------------------------------
Sindarov            2745     6.0       81.3%   813462
Caruana             2795     4.5       14.9%   149099
Giri                2753     3.5        1.6%    15999
Praggnanandhaa      2741     3.5        1.3%    12840
Wei Yi              2754     3.0        0.5%     4555
Nakamura            2810     2.5        0.2%     2020
Bluebaum            2698     3.0        0.2%     1947
Esipenko            2698     2.0        0.0%       78
```

## Copyright

Copyright ©️ 2026 Wilhelm Drehling, Heise Medien GmbH & Co. KG

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
