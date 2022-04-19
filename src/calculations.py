import numpy as np
import pandas as pd
from lookups import CARD_INT_LOOKUP, CARDS
from data import BOARDS
from evaluator import get_hand_strength


class EquityCalculator:
    def __init__(self, hole_cards: list[list[str]], board: list[str]) -> None:
        self.__validate_input(hole_cards, board)
        self.hole_cards = hole_cards
        self.board = board
        self.__int_hole_cards = self.__convert_hole_cards()
        self.__int_board = self.__convert_board()
        self.__strengths = self.__get_enumerated_strengths()
        self.summary = self.__get_summary_statistics()
        self.dataframe = self.__convert_summary_to_df()

    def __convert_hole_cards(self) -> np.ndarray:
        return np.array([[CARD_INT_LOOKUP[card] for card in hand] for hand in self.hole_cards], dtype=np.uint8).T

    def __convert_board(self) -> np.ndarray:
        return np.array([CARD_INT_LOOKUP[card] for card in self.board], dtype=np.uint8)

    def __get_enumerated_strengths(self) -> np.ndarray:
        """Calculates player hand strengths on every possible final board, returning an NxM numpy array
        containing hand strengths, where N is the number of players, and M is the number of iterations required
        to enumerate all possible final boards.
        """
        num_players = self.__int_hole_cards.shape[1]
        repeated_boards = np.repeat(self.__int_board, num_players).reshape(-1, num_players)
        hands = np.concatenate((self.__int_hole_cards, repeated_boards))
        cards_dealt = hands.shape[0]
        cards_to_come = 7 - cards_dealt
        boards = BOARDS[cards_to_come]
        mask = np.in1d(boards, hands.flatten()).reshape(*boards.shape).any(axis=0)
        boards = np.expand_dims(boards[:, ~mask], axis=2)
        return get_hand_strength(*hands, *boards)

    def __get_summary_statistics(self) -> dict:
        """Summarises the information calculated by __get_enumerated_strengths(). Converts the raw hand
        strength data to win %, lose %, etc.
        """
        wins = np.equal(self.__strengths, self.__strengths.max(axis=1).reshape(-1, 1))
        evs = wins / wins.sum(axis=1).reshape(-1, 1)
        outright_wins = (evs == 1).sum(axis=0)
        tied_wins = ((evs < 1) & (evs > 0)).sum(axis=0)
        losses = (evs == 0).sum(axis=0)
        enumerations = self.__strengths.shape[0]
        final_evs = evs.sum(axis=0) / enumerations
        summary = {
            'Enumerations': enumerations,
            'Hole Cards': [' '.join(cards) for cards in self.hole_cards],
            'Win': outright_wins.tolist(),
            'Win %': (outright_wins / enumerations).tolist(),
            'Tie': tied_wins.tolist(),
            'Tie %': (tied_wins / enumerations).tolist(),
            'Lose': losses.tolist(),
            'Lose %': (losses / enumerations).tolist(),
            'EV': final_evs.tolist()
        }
        return summary

    def __convert_summary_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.summary)
        df.drop('Enumerations', axis=1, inplace=True)
        df.sort_values(by='EV', ascending=False, inplace=True)
        return df

    @staticmethod
    def __validate_input(hole_cards, board) -> None:
        num_hands = len(hole_cards)
        num_board_cards = len(board)
        flattened_hole_cards = [card for hand in hole_cards for card in hand]
        all_cards = flattened_hole_cards + board
        if not 2 <= num_hands <= 10:
            raise ValueError(f'Invalid value for hole_cards: {hole_cards}. Must be list of 2-10 hands.')
        if num_board_cards > 4:
            raise ValueError(f'Invalid value for board: {board}. Must be list of 0-4 cards.')
        if any(len(hand) != 2 for hand in hole_cards):
            raise ValueError(f'Invalid value for hole_cards: {hole_cards}. Each hand must have exactly 2 cards.')
        if any(card not in CARDS for card in flattened_hole_cards):
            raise ValueError(f'Invalid value for hole_cards: {hole_cards}. Contains at least 1 invalid card.')
        if any(card not in CARDS for card in board):
            raise ValueError(f'Invalid value for board: {board}. Contains at least 1 invalid card.')
        if (unq := len(set(all_cards))) != (total := len(all_cards)):
            raise ValueError(f'Invalid input, contains duplicates: {unq} unique cards were found from {total} total.')

    def __repr__(self) -> str:
        enumerations = self.summary['Enumerations']
        intro = f'\nCalculated equities from evaluated hand strengths on all {enumerations:,} possible final boards.'
        if self.board:
            board = 'Board: ' + ' '.join(self.board) + '\n'
        else:
            board = 'Board: None.\n'
        pct_format = '{:.2%}'.format
        float_format = '{:.3f}'.format
        int_format = '{:,}'.format
        formatters = {
            'Win': int_format,
            'Win %': pct_format,
            'Tie': int_format,
            'Tie %': pct_format,
            'Lose': int_format,
            'Lose %': pct_format,
            'EV': float_format
        }
        df = self.dataframe.to_string(formatters=formatters, index=False, col_space=8)
        return '\n'.join([intro, board, df])
