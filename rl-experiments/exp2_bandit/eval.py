"""Evaluate the three trainers: report per-profile return of each scheme."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import env
import profiles as P
import train as T
from utils import set_seed, summarize, fmt


PROFILE_NAMES = ["safety_first", "throughput_first", "balanced"]
PROFILE_MIX = {p: 1.0 for p in PROFILE_NAMES}
N_SEEDS = 5
TRAIN_STEPS = 3000
EVAL_EPISODES = 500
EPS = 0.1
LR = 0.1


def greedy_return(q_row, profile_name, n, rng):
    a = int(np.argmax(q_row))
    total = 0.0
    for _ in range(n):
        total += P.scalarize(env.step(a, rng), profile_name)
    return total / n


def run_seed(seed):
    rng = set_seed(seed)
    q_uncond = T.train_unconditioned(TRAIN_STEPS, EPS, LR, rng, PROFILE_MIX)
    qs_per = T.train_per_profile(TRAIN_STEPS, EPS, LR, rng, PROFILE_NAMES)
    q_cond, idx = T.train_conditioned(TRAIN_STEPS, EPS, LR, rng, PROFILE_NAMES)
    out = {}
    for p in PROFILE_NAMES:
        eval_rng = set_seed(seed + 10_000)
        out[("unconditioned", p)] = greedy_return(q_uncond, p, EVAL_EPISODES, eval_rng)
        eval_rng = set_seed(seed + 20_000)
        out[("per_profile", p)] = greedy_return(qs_per[p], p, EVAL_EPISODES, eval_rng)
        eval_rng = set_seed(seed + 30_000)
        out[("conditioned", p)] = greedy_return(q_cond[idx[p]], p, EVAL_EPISODES, eval_rng)
    return out


def main():
    results = {}
    for seed in range(N_SEEDS):
        r = run_seed(seed)
        for k, v in r.items():
            results.setdefault(k, []).append(v)
    print("\n=== exp2 bandit: per-profile greedy return ===")
    schemes = ["unconditioned", "per_profile", "conditioned"]
    print(f"{'scheme':<16}{'profile':<20}{'stats'}")
    for scheme in schemes:
        for p in PROFILE_NAMES:
            print(f"{scheme:<16}{p:<20}{fmt(summarize(results[(scheme, p)]))}")


if __name__ == "__main__":
    main()
