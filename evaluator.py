from data import HAND_RANKS


def get_hand_strength(c1, c2, c3, c4, c5, c6, c7):
    """
    Function returns strength of best 5-card poker hand from the 7 cards passed in.
    The 7 cards are passed in as integers, where 0-3 are deuces, and 49-52 are aces.
    The strength is returned as an integer. Uses 7 array lookups as explained here:
    https://www.codingthewheel.com/tags/poker-hand-evaluation/#2p2

    Using numpy broadcasting, we can pass in arrays instead of single integers to lookup
    strengths for multiple hands with a single operation.
    """

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
