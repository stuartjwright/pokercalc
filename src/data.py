import os
import numpy as np


DATA_PATH = os.path.join(os.path.dirname(__file__), '../data')
HAND_RANKS_FILENAME = 'hand_ranks.npz'
BOARDS_FILENAME = 'boards.npz'


def load_hand_ranks():
    return np.load(os.path.join(DATA_PATH, HAND_RANKS_FILENAME))['arr_0']


def load_board_combos():
    zip_file = np.load(os.path.join(DATA_PATH, BOARDS_FILENAME))
    filenames = zip_file.files
    return {i: a for i, a in enumerate([zip_file[f] for f in filenames], 1)}


HAND_RANKS = load_hand_ranks()
BOARDS = load_board_combos()
