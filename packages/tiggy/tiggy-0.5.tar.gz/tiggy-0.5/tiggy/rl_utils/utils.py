import numpy as np
import numba as nb
from typing import List, Dict
from collections.abc import Iterable
import torch
import random


# @nb.njit
def get_moves(p):
    moves = np.zeros(len(p))
    for i, moveset in enumerate(p):
        chance = random.random()
        for j in range(len(moveset)):
            chance -= moveset[j]
            if chance <= 0:
                moves[i] = j
                break
    return moves

type_dict = {np.ndarray: np.array}


def unpack(env_outputs: List[Dict]) -> Dict[str, List]:
    keywords = env_outputs[0].keys()
    rewrite = {keyword:[] for keyword in keywords}
    for env_output in env_outputs:
        for key, value in env_output.items():
            rewrite[key] += [value]

    for key, value in rewrite.items():
        if isinstance(value[0], Iterable):
            rewrite[key] = type_dict[type(value[0])](value)
    return rewrite


def decay_rewards(env_outputs: List[List[Dict]], decay_factor) -> List[Dict]:
    for env_output in env_outputs:
        unpacked_env_output = unpack(env_output)
        rewards = unpacked_env_output['reward']
        decayed_rewards = np.array(rewards, dtype=np.float64)
        for i in reversed(range(len(rewards) - 1)):
            decayed_rewards[i] = rewards[i] + decay_factor * decayed_rewards[i+1]

        for i, moment in enumerate(env_output):
            moment['reward'] = decayed_rewards[i]

    return env_outputs
