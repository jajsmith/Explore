"""Three schemes, all solved by value iteration on the tabular MDP.

  - aggregated:      one V over states trained on mean-profile reward
  - per_profile:     one V per profile (upper bound / reference)
  - conditioned:     V indexed by (profile, state) -- a single policy that
                     takes the profile token as part of the input

Value iteration is exact for this finite MDP, so results are deterministic
across seeds. The seed still gates tie-breaking in the policy.
"""
import numpy as np
import env
import profiles as P


ACTIONS = list(range(env.NUM_ACTIONS))


def _transition(pos, action):
    """Returns (next_pos, rewards_dict, done) — env dynamics are deterministic."""
    e = env.GridEnv()
    e.pos = pos
    e.t = 0
    return e.step(action)


def _build_tables():
    """Precompute transitions for every (state, action)."""
    S = env.num_states()
    next_s = np.zeros((S, env.NUM_ACTIONS), dtype=int)
    r_through = np.zeros((S, env.NUM_ACTIONS))
    r_safety = np.zeros((S, env.NUM_ACTIONS))
    done = np.zeros((S, env.NUM_ACTIONS), dtype=bool)
    for r in range(env.SIZE):
        for c in range(env.SIZE):
            s = env.state_idx((r, c))
            if (r, c) == env.GOAL:
                # absorbing: stay, zero reward
                for a in ACTIONS:
                    next_s[s, a] = s
                    done[s, a] = True
                continue
            for a in ACTIONS:
                pos2, rew, d = _transition((r, c), a)
                next_s[s, a] = env.state_idx(pos2)
                r_through[s, a] = rew["throughput"]
                r_safety[s, a] = rew["safety"]
                done[s, a] = d
    return next_s, r_through, r_safety, done


_TABLES = None


def tables():
    global _TABLES
    if _TABLES is None:
        _TABLES = _build_tables()
    return _TABLES


def value_iteration(scalarize_r, gamma=1.0, iters=200):
    next_s, r_t, r_s, done = tables()
    S = next_s.shape[0]
    R = scalarize_r(r_t, r_s)  # [S, A] scalar rewards
    V = np.zeros(S)
    for _ in range(iters):
        Q = R + gamma * np.where(done, 0.0, V[next_s])
        V = Q.max(axis=1)
    return Q  # [S, A] final Q table


def train_aggregated(profile_names, gamma=1.0):
    def scalarize(rt, rs):
        acc = np.zeros_like(rt)
        for p in profile_names:
            w = P.PROFILES[p]
            acc += w["throughput"] * rt + w["safety"] * rs
        return acc / len(profile_names)

    return value_iteration(scalarize, gamma=gamma)


def train_per_profile(profile_names, gamma=1.0):
    Qs = {}
    for p in profile_names:
        w = P.PROFILES[p]
        scalarize = lambda rt, rs, _w=w: _w["throughput"] * rt + _w["safety"] * rs
        Qs[p] = value_iteration(scalarize, gamma=gamma)
    return Qs


def train_conditioned(profile_names, gamma=1.0):
    """Same as per_profile but packaged as a single (profile-indexed) table.

    A true 'conditioned policy' with function approximation would share
    parameters across profiles; here the tabular case makes the two
    equivalent. Kept separate because the *interface* matters — at
    inference we pass a profile token, not a profile-specific model.
    """
    idx = {p: i for i, p in enumerate(profile_names)}
    Qs = train_per_profile(profile_names, gamma=gamma)
    Q = np.stack([Qs[p] for p in profile_names], axis=0)
    return Q, idx
