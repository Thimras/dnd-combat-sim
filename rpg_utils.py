from typing import Optional

import numpy as np

def roll_d4():
    return np.random.randint(1, 5)

def roll_d6():
    return np.random.randint(1, 7)

def roll_d8():
    return np.random.randint(1, 9)

def roll_d10():
    return np.random.randint(1, 11)

def roll_d12():
    return np.random.randint(1, 13)

def roll_d20():
    return np.random.randint(1, 21)


def roll_xd6_into_list(num_dice: int = 4):
    return [roll_d6() for i in range(num_dice)]


def sum_highest_3_of_4d6():
    all_rolls = roll_xd6_into_list()
    sum_highest_3: Optional[int] = sum(all_rolls) - min(all_rolls)
    return sum_highest_3

def get_modifier(stat: int = None):
    modifier = np.floor((stat - 10) / 2).astype(np.int)
    return modifier