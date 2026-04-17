"""Two conditioning schemes:

  - token: Q[profile_id, arm] for profiles in TRAIN. At inference, the
    scheme picks the Q row whose profile is closest (cosine) to the
    eval profile's weight vector. This is the "one-hot token" scheme —
    it cannot represent profiles it never saw.

  - decomp: learn Q_c[arm] for every reward component c independently,
    using env rewards (which are always fully observed). At inference,
    for any weight vector w, pick argmax_a sum_c w_c * Q_c[a]. This is
    the multi-objective decomposition scheme — it can generalize to any
    weight vector in R^C, including unseen axes, as long as the training
    behavioral policy gave every arm enough exploration.

The behavioral policy during training is eps-greedy w.r.t. the current
*training-profile* scalarized Q, with profile sampled uniformly from TRAIN.
"""
import numpy as np
import env
from profiles import TRAIN, COMPONENTS


def train_both(steps: int, eps: float, lr: float, rng: np.random.Generator):
    K = env.num_arms()
    train_names = list(TRAIN.keys())
    C = len(COMPONENTS)

    # Token-scheme Q: one row per training profile, indexed by arm.
    Q_token = np.zeros((len(train_names), K))

    # Decomposition Q: one value per (component, arm).
    Q_comp = np.zeros((C, K))

    comp_idx = {c: i for i, c in enumerate(COMPONENTS)}

    for _ in range(steps):
        # Sample a training profile.
        pi = int(rng.integers(0, len(train_names)))
        pname = train_names[pi]
        w = np.array([TRAIN[pname][c] for c in COMPONENTS])

        # Eps-greedy w.r.t. the current token Q for this profile.
        if rng.random() < eps:
            a = int(rng.integers(0, K))
        else:
            a = int(np.argmax(Q_token[pi]))

        r_dict = env.step(a, rng)
        r_vec = np.array([r_dict[c] for c in COMPONENTS])

        # Token update: scalarize using the sampling profile.
        r_scalar = float(np.dot(w, r_vec))
        Q_token[pi, a] += lr * (r_scalar - Q_token[pi, a])

        # Decomp update: one per component, regardless of profile.
        for ci, c in enumerate(COMPONENTS):
            Q_comp[ci, a] += lr * (r_vec[ci] - Q_comp[ci, a])

    return Q_token, train_names, Q_comp


def token_action(Q_token, train_names, eval_weight_vec):
    """Pick the training profile whose weight vector is most cosine-aligned,
    then take its greedy arm."""
    w = np.array(eval_weight_vec, dtype=float)
    if np.linalg.norm(w) == 0:
        return int(np.argmax(Q_token[0]))
    best_i = 0
    best_cos = -np.inf
    for i, name in enumerate(train_names):
        wi = np.array([TRAIN[name][c] for c in COMPONENTS])
        denom = np.linalg.norm(w) * np.linalg.norm(wi)
        cos = 0.0 if denom == 0 else float(np.dot(w, wi) / denom)
        if cos > best_cos:
            best_cos = cos
            best_i = i
    return int(np.argmax(Q_token[best_i]))


def decomp_action(Q_comp, eval_weight_vec):
    w = np.array(eval_weight_vec, dtype=float)
    scores = w @ Q_comp  # [K]
    return int(np.argmax(scores))
