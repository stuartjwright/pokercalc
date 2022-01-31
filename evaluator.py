from data import HAND_RANKS
from numba import njit, uint8, int32


@njit
def get_river_hand_strength(hc1: uint8, hc2: uint8, f1: uint8, f2: uint8, f3: uint8, t: uint8, r: uint8) -> int32:
    """Returns strength of best 5-card poker hand from the 7 cards passed in.
    The 7 cards are passed in as integers, where 0-3 are deuces, and 49-52 are aces.
    The strength is returned as an integer. Uses 7 array lookups as explained here:
    https://www.codingthewheel.com/tags/poker-hand-evaluation/#2p2
    The numba @njit decorator is used to allow this function to be called from other
    numba functions which may call this function several times in a loop. This function
    itself doesn't gain any speed benefit from numba.
    :param hc1: first hole card
    :param hc2: second hole card
    :param f1: first flop card
    :param f2: second flop card
    :param f3: third flop card
    :param t: turn card
    :param r: river card
    :return: integer representation of hand strength
    """

    return (
        HAND_RANKS[
            HAND_RANKS[
                HAND_RANKS[
                    HAND_RANKS[
                        HAND_RANKS[
                            HAND_RANKS[
                                HAND_RANKS[
                                    53 + hc1
                                ] + hc2
                            ] + f1
                        ] + f2
                    ] + f3
                ] + t
            ] + r
        ]
    )


if __name__ == '__main__':
    test = get_river_hand_strength(1, 4, 5, 7, 8, 12, 24)
