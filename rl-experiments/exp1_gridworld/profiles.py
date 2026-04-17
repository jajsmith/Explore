"""Value profiles for gridworld."""
from env import COMPONENTS


PROFILES = {
    "throughput_first": {"throughput": 1.0, "safety": 0.0},
    "safety_first":     {"throughput": 0.2, "safety": 1.0},
    "balanced":         {"throughput": 0.6, "safety": 0.6},
}


def scalarize(reward_dict, profile_name: str) -> float:
    p = PROFILES[profile_name]
    return sum(reward_dict[c] * p[c] for c in reward_dict)
