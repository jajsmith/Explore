"""Bandit with 3 reward components for held-out profile generalization.

Arms 0, 1, 2 each maximize one component. Arm 3 is a weak compromise.
"""
import numpy as np

COMPONENTS = ("c0", "c1", "c2")

ARMS = np.array(
    [
        [1.0, 0.0, 0.0],  # arm 0
        [0.0, 1.0, 0.0],  # arm 1
        [0.0, 0.0, 1.0],  # arm 2
        [0.4, 0.4, 0.4],  # arm 3: dominated compromise
    ]
)
NOISE = 0.1


def step(arm: int, rng: np.random.Generator):
    mean = ARMS[arm]
    noise = rng.normal(0.0, NOISE, size=mean.shape)
    r = mean + noise
    return {name: float(x) for name, x in zip(COMPONENTS, r)}


def num_arms() -> int:
    return ARMS.shape[0]
