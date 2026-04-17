"""Shared utilities for RL experiments."""
import numpy as np


def set_seed(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def summarize(values):
    arr = np.asarray(values, dtype=float)
    return {
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        "n": int(arr.size),
    }


def fmt(d):
    return f"median={d['median']:.3f} mean={d['mean']:.3f} std={d['std']:.3f} (n={d['n']})"
