#!/usr/bin/env python
"""composing_v1.py: composes music"""

__author__      = "Thomas Heller"
__copyright__   = "Copyright 2022, Thomas Heller"

import random as rn
from typing import Tuple

RHYM_FRAG = {
    2  : [[1,1]],
    3  : [[1,2], [2,1], [1,1,1]],
    4  : [[1,3], [2,2], [3,1], [1,1,1,1]],
    6  : [[4,2], [2,4], [2,2,2]],
    8  : [[4,4], [2,6], [6,2], [2,2,2,2]],
    16 : [[8,8]],
}

DUR   = [0,2,4,5,7,9,11]
BLUES = [0,3,5,6,7,10]


def create_beat_rhym(len_ticks:int=16, num_tones:int=5) -> list:
    '''Create the rhythm like a tree by splitting tones'''

    if type(len_ticks) != int or type(num_tones) != int or len_ticks < num_tones or len_ticks < 0 or num_tones < 0 or len_ticks not in RHYM_FRAG.keys():
        raise ValueError('input is not logical')

    r_rhym = [len_ticks]
    while len(r_rhym) < num_tones:
        all_splittable_values = [(idx,ii) for idx,ii in enumerate(r_rhym) if ii in RHYM_FRAG]
        chosen = rn.randrange(len(all_splittable_values))
        chosen_idx,chosen_val = all_splittable_values[chosen]
        split_into = rn.choice([ii for ii in RHYM_FRAG[chosen_val] if len(ii)+len(r_rhym)-1 <= num_tones])
        del r_rhym[chosen_idx]
        for ii in split_into:
            r_rhym.insert(chosen_idx, ii)
    return r_rhym

def create_melo(chord:list=[0,4,7], scale:list=[0], num_tones:int=5, melo_min:int=48, melo_max:int=72) -> list:
    '''Create the melody as random notes in scale with a higher likelyhood for steps'''

    scale_tones = [ii for ii in range(melo_min, melo_max+1) if ii % 12 in scale]
    chord_tones = [ii for ii in range(melo_min, melo_max+1) if ii % 12 in chord]
    all_tones = scale_tones + chord_tones + chord_tones
    r_melo = [rn.choice(all_tones)]
    for _ in range(num_tones-1):
        near_tones = [ii for ii in all_tones if abs(ii-r_melo[-1]) <= 5]
        r_melo.append(rn.choice(all_tones + near_tones + near_tones + near_tones + near_tones))
    return r_melo
    

def create_random_motif(chord:list=[0,4,7], scale:list=DUR, len_ticks:int=16, num_tones:int=5, melo_min:int=48, melo_max:int=72) -> Tuple[list]:
    '''Create a random motif with simple restrains > rhym is on beat > melo in scale and likes steps'''

    r_rhym = create_beat_rhym(len_ticks, num_tones)
    r_melo = create_melo(chord, scale, num_tones, melo_min, melo_max)

    return r_melo, r_rhym


def compose_n_bars(N_bars:int) -> Tuple[list]:
    '''Composes n bars of music as basic algorithmic improvisation'''

    total_melo = []
    total_rhym = []

    for ii in range(N_bars):
        tmp_m, tmp_r = create_random_motif()
        total_melo.extend(tmp_m)
        total_rhym.extend(tmp_r)
    
    return total_melo, total_rhym
