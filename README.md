# Poker Calculator

A Python library for calculating all-in equities in Texas Hold'em Poker hands.

## Requirements

 - Python 3.9+
 - NumPy 1.22.3+
 - pandas 1.4.2+

## Usage

Import the `EquityCalculator` class from the `calculations` module:

```python
from calculations import EquityCalculator, CARDS
```

Importing `CARDS` is optional, but it is useful for simulating randomly generated hands. `CARDS` is a list of valid cards which can be used as input:

```python
['2c', '2d', '2h', '2s', '3c', '3d', ..., 'Kh', 'Ks', 'Ac', 'Ad', 'Ah', 'As']
```

The `EquityCalculator` constructor takes two arguments:

 - hole_cards - a list of lists, where each inner list contains two cards.
 - board - a list of 0-4 cards representing the board.

In the following example, there are two players, and three cards on the board:

```python
hole_cards = [['Js', 'Ts'], ['2c', '2d']]
board = ['9s', '8s', '3c']
equities = EquityCalculator(hole_cards, board)
```

Printing `equities` would display the following results:

```
Calculated equities from evaluated hand strengths on all 990 possible final boards.
Board: 9s 8s 3c
Hole Cards      Win    Win %      Tie    Tie %     Lose   Lose %       EV
     Js Ts      716   72.32%        0    0.00%      274   27.68%    0.723
     2c 2d      274   27.68%        0    0.00%      716   72.32%    0.277
```

Various other data points can be extracted from the `equities` object - see the `example_usage.py` script for some more examples.

# How This Works

This library was inspired by the [Two Plus Two Evaluator](https://www.codingthewheel.com/tags/poker-hand-evaluation/#2p2), which can evaluate the strength of any 7-card poker hand using 7 array lookups on its pre-generated array of 32,487,834 integers. The 7-card poker hand is represented by integers, where 1 is the 2 of clubs, and 52 is the Ace of Spades.

continue here