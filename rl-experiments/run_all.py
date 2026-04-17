"""Run all experiments and print their results to stdout."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

experiments = [
    ("exp1_gridworld", "eval.py"),
    ("exp2_bandit", "eval.py"),
    ("exp3_generalization", "eval.py"),
]

for folder, script in experiments:
    path = os.path.join(HERE, folder)
    print(f"\n--- Running {folder}/{script} ---")
    subprocess.run([sys.executable, script], cwd=path, check=True)
