# Initial Results

Reproduce with `python3 run_all.py` from `rl-experiments/`. Numpy only, no
torch. Seeds fixed at 0..4 for stochastic experiments (exp2, exp3); exp1 is
solved exactly by value iteration.

## exp1_gridworld — genuine multi-objective tradeoff

5x5 grid with a hazard shortcut at (2,2): entering it teleports to the goal
(+10 throughput) but costs -5 safety. Safe path avoids (2,2) and takes 8 steps.

| scheme         | throughput_first | safety_first | balanced |
|----------------|------------------|--------------|----------|
| aggregated     | 2.000            | 0.400        | 1.200    |
| per_profile    | **6.000**        | 0.400        | 1.200    |
| conditioned    | **6.000**        | 0.400        | 1.200    |

Scalarized returns using each row's profile. Aggregated trains one policy on
the average reward and loses 4 points on `throughput_first` (refuses the
shortcut). Per-profile and conditioned behave identically in tabular VI — the
conditioned policy correctly selects shortcut-vs-safe based on the profile
token it is given.

## exp2_bandit — profile-conditioning sanity check

Four arms with (safety, throughput) reward vectors. Three profiles weighted
over those components. Greedy return after 3000 eps-greedy steps, 5 seeds.

| scheme         | safety_first | throughput_first | balanced |
|----------------|--------------|------------------|----------|
| unconditioned  | 0.60         | 0.60             | 0.60     |
| per_profile    | **1.00**     | **1.00**         | 0.60     |
| conditioned    | **1.00**     | **1.00**         | 0.60     |

Unconditioned collapses to the arm-2 compromise (0.6 for everyone, independent
of profile). Per-profile and conditioned both hit 1.0 on single-objective
profiles. All three hit ~0.6 on `balanced` because the compromise arm
**is** optimal there — this is a feature of the env, not a failure.

## exp3_generalization — interpolation vs. held-out axis

Bandit with 3 reward components. Train on profiles A=[1,0,0] and B=[0,1,0]
only. Evaluate zero-shot on: the seen profiles, their convex combination
`interp_AB`=[0.5,0.5,0], and a never-seen axis `heldout_C`=[0,0,1].

| scheme   | A_seen | B_seen | interp_AB | heldout_C    |
|----------|--------|--------|-----------|--------------|
| token    | 1.00   | 1.00   | 0.50      | **0.00**     |
| decomp   | 1.00   | 1.00   | 0.50      | **1.00**     |
| optimal  | 1.00   | 1.00   | 0.50      | 1.00         |

Token-conditioning (one-hot profile ID, nearest-seen at inference) fails
cold on `heldout_C`: it picks an arm optimized for A or B, which gives zero
reward on the unseen axis. Decomposition-conditioning learns per-component
Q values and reconstructs the policy for any weight vector at inference —
it matches optimal on all four evaluations, **including the held-out axis**,
because eps-greedy exploration pulled every arm enough to estimate every
component's Q.

## Takeaways

1. Aggregating rewards across profiles does not merely pick a "compromise" —
   it can silently refuse behaviors that some profiles prefer (exp1:
   `throughput_first` never sees the shortcut).
2. Profile-conditioned tabular policies recover per-profile optima, as
   expected (exp2, exp1).
3. The *form* of conditioning matters for generalization. One-hot tokens
   cannot extrapolate off the training simplex; vector conditioning via
   multi-objective decomposition handles arbitrary weight vectors as long as
   exploration covered every reward axis (exp3).
4. Keeping reward components unaggregated in the environment was essential
   for the decomposition scheme in exp3 — a scalarized-at-source env would
   have made this scheme impossible to train.

## Caveats

- Gridworld uses value iteration, not learned Q-learning, so results are
  deterministic and do not exercise sample-efficiency differences. An earlier
  Q-learning version got stuck in a local shortcut attractor for the
  `balanced` profile and failed to propagate values along the longer safe
  detour — not a pluralistic-alignment issue, but a reminder that
  exploration coverage is a prerequisite for any of these schemes.
- All experiments are synthetic and discrete. The bandit setting cleanly
  isolates the conditioning question but does not exercise sequential
  credit assignment with conditioning.
- Decomposition relies on linear scalarization. Non-linear value aggregation
  (e.g. leximin, Nash) would break the decomposition trick.
