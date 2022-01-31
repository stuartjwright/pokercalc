import os
import numpy as np


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
HAND_RANKS_FILENAME = 'hand_ranks.npz'
HAND_RANKS = np.load(os.path.join(DATA_PATH, HAND_RANKS_FILENAME))['array']
