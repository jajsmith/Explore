"""Value profiles: named weight vectors over reward components."""
from env import COMPONENTS


PROFILES = {
    "safety_first": {"safety": 1.0, "throughput": 0.0},
    "throughput_first": {"safety": 0.0, "throughput": 1.0},
    "balanced": {"safety": 0.5, "throughput": 0.5},
}


def weight_vector(profile_name: str):
    p = PROFILES[profile_name]
    return [p[c] for c in COMPONENTS]


def scalarize(reward_dict, profile_name: str) -> float:
    p = PROFILES[profile_name]
    return sum(reward_dict[c] * p[c] for c in reward_dict)
