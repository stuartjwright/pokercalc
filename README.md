# Poker Calculator

A Python library for calculating all-in equities in Texas Hold'em Poker hands.

## Disclaimer

The purpose of this library is to demonstrate the power of NumPy broadcasting, and how it can be used to avoid slow Python loops. The calculations performed are accurate and time-efficient, but not space-efficient. It is suitable for use in local data analysis workflows, but it has not been built with production in mind.

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

If the large lookup array is called `HAND_RANKS` and the 7 cards are in integer variables `c1`, `c2`, ... `c7`, the Python code to return a hand strength looks like this:

```python
return (
    HAND_RANKS[
        HAND_RANKS[
            HAND_RANKS[
                HAND_RANKS[
                    HAND_RANKS[
                        HAND_RANKS[
                            HAND_RANKS[
                                53 + c1
                            ] + c2
                        ] + c3
                    ] + c4
                ] + c5
            ] + c6
        ] + c7
    ]
)
```

While this is not the most readable code, it avoids introducing a slow Python loop. If the code above is the body of function `get_hand_strength`, then we can run:

```python
get_hand_strength(52, 48, 44, 40, 36, 1, 2)  # The first five cards here are AKQJT of spades, a royal flush
```

And the return value is `36874`. The exact meaning of this value is described further in the linked article, but for our purposes here, we just need to know that it can be compared to other hand strengths returned by the same function, thus allowing us to find the winning hand.

But how does this help with the equity calculator? Going with the earlier example where one player has `['Js', 'Ts']`, another player has `['2c', '2d']`, and the board is `['9s', '8s', '3c']`, to calculate the equity of each hand, we need to find all possible final boards, evaluate the strength of each hand on each possible board, and tally the results. With 45 unknown cards and 2 cards still to be dealt, there are 990 (45 choose 2) final boards. The obvious option is to perform these steps in a loop, but loops are notoriously slow in native Python. 990 iterations isn't many, but if fewer board cards are known, more iterations are needed (up to 1,712,304, or 48 choose 5).

This is where [NumPy Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) works its magic. If we shape our input arrays correctly, we can call the `get_hand_strength` function once, and it will return a results array of shape 990x2 (where 990 is the number of possible final boards and 2 is the number of players), thus avoiding a slow Python loop.

The exact steps to generate the appropriate input data can be seen in `EquityCalculator.__get_enumerated_strengths`, but ultimately what happens in this case is that arguments `c1` - `c5` are all 1-d arrays of length 2. `c1` will contain the first hole card of each player. `c2` will contain the second hole card of each player. `c3` will contain the first board card, repeated so that each player has their own personal copy (required for broadcasting to work correctly). The same applies for `c4` and `c5`. `c6` and `c7` are both 2-d arrays of shape 990x1. By combining the two different array shapes in our indexing, we end up with the desired 990x2 array, which can then be summarised to calculate the expected value of each hand (see `EquityCalculator.__get_summary_statistics`) for details.

The same code works regardless of which array shapes are needed. For example, a three-player preflop hand would need 1-d arrays of length 3 for each of `c1` and `c2`. Then `c3` - `c7` would each be of shape 1,370,754 x 1. Clearly, this is not a particularly space-efficient way to perform these calculations, but assuming enough RAM is available, the speed-up over a Python loop solution is significant. For both speed and space efficiency, a looped solution using Numba or Cython would be preferable. In addition, for preflop match-ups where 1M+ evaluations are required, caching the results for fast lookup would undoubtedly be preferable to any of the on-the-fly methods proposed here.
