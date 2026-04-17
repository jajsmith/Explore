"""Contextual bandit with named, unaggregated reward components.

Four arms, two reward components per arm: (safety, throughput). The env emits
both components; aggregation (if any) is the trainer's job.
"""
import numpy as np

ARMS = np.array(
    [
        [1.0, 0.0],   # arm 0: pure safety
        [0.0, 1.0],   # arm 1: pure throughput
        [0.6, 0.6],   # arm 2: compromise
        [0.2, 0.2],   # arm 3: dominated, never optimal
    ]
)

COMPONENTS = ("safety", "throughput")


def step(arm: int, rng: np.random.Generator):
    mean = ARMS[arm]
    noise = rng.normal(0.0, 0.1, size=mean.shape)
    rewards = mean + noise
    return {name: float(r) for name, r in zip(COMPONENTS, rewards)}


def num_arms() -> int:
    return ARMS.shape[0]
