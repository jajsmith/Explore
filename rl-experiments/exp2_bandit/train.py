"""Three trainers for the bandit: unconditioned, per-profile, profile-conditioned.

All use epsilon-greedy over Q-value estimates, with the scalarized reward
specified by the trainer (not the env).
"""
import numpy as np
import env
import profiles as P


def eps_greedy(q_row: np.ndarray, eps: float, rng: np.random.Generator) -> int:
    if rng.random() < eps:
        return int(rng.integers(0, q_row.shape[0]))
    return int(np.argmax(q_row))


def train_unconditioned(steps: int, eps: float, lr: float, rng, profile_mix):
    """Trains one Q-table ignoring profile; reward is avg-scalarized over mix."""
    K = env.num_arms()
    q = np.zeros(K)
    counts = np.zeros(K)
    mix_names = list(profile_mix.keys())
    mix_probs = np.array([profile_mix[n] for n in mix_names])
    mix_probs /= mix_probs.sum()
    for _ in range(steps):
        a = eps_greedy(q, eps, rng)
        r_dict = env.step(a, rng)
        pname = rng.choice(mix_names, p=mix_probs)
        r = P.scalarize(r_dict, pname)
        counts[a] += 1
        q[a] += lr * (r - q[a])
    return q


def train_per_profile(steps: int, eps: float, lr: float, rng, profile_names):
    """One Q-table per profile, trained on its own scalarized reward."""
    K = env.num_arms()
    qs = {p: np.zeros(K) for p in profile_names}
    per_p_steps = steps // len(profile_names)
    for p in profile_names:
        q = qs[p]
        for _ in range(per_p_steps):
            a = eps_greedy(q, eps, rng)
            r_dict = env.step(a, rng)
            r = P.scalarize(r_dict, p)
            q[a] += lr * (r - q[a])
    return qs


def train_conditioned(steps: int, eps: float, lr: float, rng, profile_names):
    """Single Q-table indexed by (profile, arm)."""
    K = env.num_arms()
    q = np.zeros((len(profile_names), K))
    idx = {p: i for i, p in enumerate(profile_names)}
    for _ in range(steps):
        p = profile_names[rng.integers(0, len(profile_names))]
        i = idx[p]
        a = eps_greedy(q[i], eps, rng)
        r_dict = env.step(a, rng)
        r = P.scalarize(r_dict, p)
        q[i, a] += lr * (r - q[i, a])
    return q, idx
