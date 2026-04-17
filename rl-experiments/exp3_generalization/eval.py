"""Evaluate held-out generalization of token vs decomposition conditioning."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))

import numpy as np
import env
import profiles as P
import train as T
from utils import set_seed, summarize, fmt


N_SEEDS = 5
STEPS = 6000
EPS = 0.1
LR = 0.1
EVAL_EPISODES = 500


def expected_return(arm, profile):
    """Deterministic expected return (ignores 0-mean noise)."""
    w = np.array(P.weight_vec(profile))
    return float(np.dot(env.ARMS[arm], w))


def run_seed(seed):
    rng = set_seed(seed)
    Q_token, train_names, Q_comp = T.train_both(STEPS, EPS, LR, rng)
    out = {}
    for name, prof in P.EVAL.items():
        wvec = P.weight_vec(prof)
        a_tok = T.token_action(Q_token, train_names, wvec)
        a_dec = T.decomp_action(Q_comp, wvec)
        out[("token", name)] = expected_return(a_tok, prof)
        out[("decomp", name)] = expected_return(a_dec, prof)
        out[("optimal", name)] = P.optimal_return(prof)
    return out


def main():
    results = {}
    for seed in range(N_SEEDS):
        r = run_seed(seed)
        for k, v in r.items():
            results.setdefault(k, []).append(v)
    print("\n=== exp3 held-out generalization: expected return per eval profile ===")
    print(f"{'scheme':<10}{'eval profile':<16}{'stats':<55}{'optimal'}")
    for name in P.EVAL:
        opt = results[("optimal", name)][0]
        for scheme in ["token", "decomp"]:
            s = fmt(summarize(results[(scheme, name)]))
            print(f"{scheme:<10}{name:<16}{s:<55}{opt:.3f}")
        print()


if __name__ == "__main__":
    main()
