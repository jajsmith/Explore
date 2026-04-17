"""Training profiles (seen) and evaluation profiles (including held-out)."""
from env import COMPONENTS


# Training profiles: two axis-aligned value profiles.
TRAIN = {
    "A": {"c0": 1.0, "c1": 0.0, "c2": 0.0},
    "B": {"c0": 0.0, "c1": 1.0, "c2": 0.0},
}

# Evaluation profiles.
EVAL = {
    "A_seen":         {"c0": 1.0, "c1": 0.0, "c2": 0.0},   # in-distribution
    "B_seen":         {"c0": 0.0, "c1": 1.0, "c2": 0.0},   # in-distribution
    "interp_AB":      {"c0": 0.5, "c1": 0.5, "c2": 0.0},   # convex combo of seen
    "heldout_C":      {"c0": 0.0, "c1": 0.0, "c2": 1.0},   # unseen axis
}


def weight_vec(profile: dict):
    return [profile[c] for c in COMPONENTS]


def scalarize(reward_dict, profile: dict) -> float:
    return sum(reward_dict[c] * profile[c] for c in reward_dict)


def optimal_return(profile: dict):
    """Best expected scalarized return, assuming we know ARMS.

    Noise is zero-mean, so expected reward equals ARM[a] dot w.
    """
    from env import ARMS
    import numpy as np
    w = np.array(weight_vec(profile))
    return float(np.max(ARMS @ w))
