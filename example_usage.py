from calculations import EquityCalculator


def example():
    hand_1 = ['Kd', 'Qd']  # Each hand must have exactly two hole cards
    hand_2 = ['Ks', 'Qs']
    hand_3 = ['5s', '5d']
    hand_4 = ['9c', '8c']
    hole_cards = [hand_1, hand_2, hand_3, hand_4]  # Must be 2-10 hands in total
    board = ['Js', 'Tc', '2c']  # Board must have no more than 4 cards already dealt, can be empty
    return EquityCalculator(hole_cards, board)


if __name__ == '__main__':
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
