import random
from calculations import EquityCalculator, CARDS


def example():
    hand_1 = ['Kd', 'Qd']  # Each hand must have exactly two hole cards
    hand_2 = ['Ks', 'Qs']
    hand_3 = ['5s', '5d']
    hand_4 = ['9c', '8c']
    hole_cards = [hand_1, hand_2, hand_3, hand_4]  # Must be 2-10 hands in total
    board = ['Js', 'Tc', '2c']  # Board must have no more than 4 cards already dealt, can be empty
    return EquityCalculator(hole_cards, board)


def another_example():
    hand_1 = ['Js', 'Ts']
    hand_2 = ['2c', '2d']
    hole_cards = [hand_1, hand_2]
    board = ['9s', '8s', '3c']
    return EquityCalculator(hole_cards, board)


def random_example():
    deck = CARDS.copy()
    random.shuffle(deck)
    num_players = random.randint(2, 10)
    num_board_cards = random.randint(0, 4)
    board = [deck.pop() for _ in range(num_board_cards)]
    hole_cards = [[deck.pop(), deck.pop()] for _ in range(num_players)]
    return EquityCalculator(hole_cards, board)


if __name__ == '__main__':
    # View full list of valid cards
    print(CARDS)

    # Create example EquityCalculator object
    equities = example()

    # Print console-friendly summary:
    print(equities)

    # Extract hole cards and board cards
    hc = equities.hole_cards
    b = equities.board

    # Extract Pandas DataFrame containing summary data
    df = equities.dataframe

    # Or extract same data in dictionary format
    d = equities.summary

    # Other examples
    print(another_example())
    print(random_example())
