# RL Experiments: Initial Pluralistic Alignment

Scratch space for reinforcement-learning experiments that probe *pluralistic*
alignment — training and evaluating policies against multiple, potentially
conflicting reward signals that represent distinct human value profiles,
rather than collapsing to a single scalar reward.

## Motivation

Standard RLHF optimizes a single reward model fit to aggregated preferences.
This bakes in majority preferences and erases disagreement. Pluralistic
alignment treats the population of value profiles as first-class: the policy
should be legible to, and steerable toward, different value sets without
retraining.

Questions we want the experiments here to answer:

- Can a single policy condition on a value profile and produce behavior that
  a holder of that profile actually prefers?
- What happens under value conflicts — do we get averaging, mode collapse, or
  coherent profile-conditional behavior?
- How does distributional shift in the profile mixture at inference time
  compare to shift in the task distribution?

## Experiment Scaffolding

Each experiment lives in its own subdirectory with:

- `env.py` — environment or task definition, including a way to emit
  per-profile reward components (not a pre-aggregated scalar).
- `profiles.py` — the set of value profiles under test. Start with 2–3
  hand-crafted profiles that disagree on at least one axis.
- `train.py` — training entry point. Must log per-profile returns separately.
- `eval.py` — evaluation against held-out profile mixtures, including
  profiles not seen at training time.
- `README.md` — hypothesis, setup, and observed results.

Do not aggregate rewards inside the environment. Aggregation (if any) belongs
in the trainer, so we can swap schemes without touching the env.

## Initial Experiments (planned)

1. **Two-objective gridworld.** Toy env with a "safety" reward and a
   "throughput" reward that trade off. Compare: scalarized RLHF,
   profile-conditioned policy, and a mixture-of-experts head per profile.
2. **Preference-conditioned bandit.** Contextual bandit where the optimal
   arm depends on a profile token. Sanity check that conditioning works at
   all before moving to sequential tasks.
3. **Held-out profile generalization.** Train on profiles A, B; evaluate on
   a convex combination and on a genuinely new C. Look for interpolation vs.
   extrapolation failure modes.

## Conventions

- Seeds: log and fix. Report medians across ≥5 seeds before claiming a
  result.
- Reward components are always named, never positional.
- No silent reward clipping or normalization — if applied, it is a logged
  trainer hyperparameter.
- Profiles are data, not code paths. Adding a profile should not require
  editing the trainer.

## Non-goals (for now)

- Learning profiles from real human data. We start with synthetic profiles to
  keep the alignment signal clean.
- Scaling. These are small experiments; correctness and clarity over speed.
- Deployment-shaped safety claims. This is a research sandbox.
