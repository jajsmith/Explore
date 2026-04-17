"""Two-objective gridworld with unaggregated reward components.

Grid: 5x5. Start (0,0). Goal (4,4).

There's a "hazard shortcut" at (2,2): entering it teleports the agent to the
goal (episode ends with the goal bonus) BUT incurs a safety penalty.

Per-step reward components:
  - throughput: -1 per step; +10 on reaching goal (incl. via shortcut)
  - safety:     -5 if entering the hazard cell; 0 otherwise

This forces a genuine tradeoff:
  - shortcut path (0,0)->(0,1)->(0,2)->(1,2)->(2,2): 4 steps, throughput=+6, safety=-5
  - long safe path avoiding (2,2): 8 steps,             throughput=+2, safety= 0

Action space: 0=up, 1=right, 2=down, 3=left. Invalid moves are no-ops.
"""
import numpy as np

SIZE = 5
START = (0, 0)
GOAL = (4, 4)
HAZARD_SHORTCUT = (2, 2)
MAX_STEPS = 40

COMPONENTS = ("throughput", "safety")

_MOVES = {
    0: (-1, 0),  # up
    1: (0, 1),   # right
    2: (1, 0),   # down
    3: (0, -1),  # left
}
NUM_ACTIONS = 4


class GridEnv:
    def __init__(self):
        self.pos = START
        self.t = 0

    def reset(self):
        self.pos = START
        self.t = 0
        return self.pos

    def step(self, action: int):
        dr, dc = _MOVES[action]
        r, c = self.pos
        nr, nc = r + dr, c + dc
        if 0 <= nr < SIZE and 0 <= nc < SIZE:
            self.pos = (nr, nc)
        self.t += 1
        throughput = -1.0
        safety = 0.0
        done = False
        if self.pos == HAZARD_SHORTCUT:
            safety = -5.0
            throughput += 10.0  # teleport to goal, collect bonus
            self.pos = GOAL
            done = True
        elif self.pos == GOAL:
            throughput += 10.0
            done = True
        if self.t >= MAX_STEPS:
            done = True
        rewards = {"throughput": throughput, "safety": safety}
        return self.pos, rewards, done


def num_states() -> int:
    return SIZE * SIZE


def state_idx(pos) -> int:
    r, c = pos
    return r * SIZE + c
