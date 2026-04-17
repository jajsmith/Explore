"""Evaluate gridworld schemes. Reports per-profile greedy return."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import env
import profiles as P
import train as T
from utils import summarize, fmt


PROFILES = ["throughput_first", "safety_first", "balanced"]
GAMMA = 1.0


def greedy_rollout(Q_row_fn, profile):
    e = env.GridEnv()
    pos = e.reset()
    total = {"throughput": 0.0, "safety": 0.0}
    for _ in range(env.MAX_STEPS + 1):
        s = env.state_idx(pos)
        a = int(np.argmax(Q_row_fn(s)))
        pos, r_dict, done = e.step(a)
        for k, v in r_dict.items():
            total[k] += v
        if done:
            break
    return P.scalarize(total, profile), total


def main():
    Q_agg = T.train_aggregated(PROFILES, gamma=GAMMA)
    Qs_per = T.train_per_profile(PROFILES, gamma=GAMMA)
    Q_cond, idx = T.train_conditioned(PROFILES, gamma=GAMMA)

    print("\n=== exp1 gridworld: per-profile greedy return (value iteration) ===")
    print(f"{'scheme':<16}{'profile':<20}{'scalarized':>12}{'    components'}")
    for scheme, get_Q in [
        ("aggregated",   lambda p: (lambda s: Q_agg[s])),
        ("per_profile",  lambda p: (lambda s: Qs_per[p][s])),
        ("conditioned",  lambda p: (lambda s, _p=p: Q_cond[idx[_p], s])),
    ]:
        for p in PROFILES:
            sc, comps = greedy_rollout(get_Q(p), p)
            print(f"{scheme:<16}{p:<20}{sc:>12.3f}    {comps}")


if __name__ == "__main__":
    main()
