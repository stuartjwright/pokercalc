from itertools import product


def generate_cards() -> list[str]:
    """Simple function to generate list of strings for the 52 cards.
    :return: list of strings: ['2c', '2d'... 'Ah', 'As']
    """

    suits = ['c', 'd', 'h', 's']
    ranks = [str(i) for i in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A']
    cards = [''.join(card) for card in product(ranks, suits)]
    return cards


CARDS = generate_cards()


def generate_card_int_lookup() -> dict[str, int]:
    """Generates a string to integer card lookup dictionary. The integer version of the
    card is used for hand evaluations.
    :return: lookup dictionary in following format:  {'2c': 1, '2d': 2, ... 'Ah': 51, 'As': 52}
    """

    card_int_lookup = {card: i+1 for i, card in enumerate(CARDS)}
    return card_int_lookup


CARD_INT_LOOKUP = generate_card_int_lookup()
