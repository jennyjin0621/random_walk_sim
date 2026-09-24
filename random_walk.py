"""
Monte Carlo simulation of a random walk confined to a lattice shape.

Each step moves to one of 4 neighbors with equal probability. The walk
stops once it lands on a boundary cell (see shapes.classify).
"""

from collections import Counter

import numpy as np

DIRECTIONS = np.array([(-1, 0), (1, 0), (0, -1), (0, 1)])


def simulate_walks(boundary, start, num_trials, max_steps=200_000, rng=None):
    """
    Run num_trials walks from `start` (an interior cell) until each hits
    the boundary. Returns exit_rows, exit_cols, exit_steps, each length
    num_trials. A trial still unfinished at max_steps gets -1.
    """
    if rng is None:
        rng = np.random.default_rng()

    rows = np.full(num_trials, start[0], dtype=np.int64)
    cols = np.full(num_trials, start[1], dtype=np.int64)
    steps = np.zeros(num_trials, dtype=np.int64)
    active = np.ones(num_trials, dtype=bool)

    exit_rows = np.full(num_trials, -1, dtype=np.int64)
    exit_cols = np.full(num_trials, -1, dtype=np.int64)
    exit_steps = np.full(num_trials, -1, dtype=np.int64)

    for _ in range(max_steps):
        if not active.any():
            break

        active_idx = np.where(active)[0]
        moves = DIRECTIONS[rng.integers(0, 4, size=active_idx.size)]
        rows[active_idx] += moves[:, 0]
        cols[active_idx] += moves[:, 1]
        steps[active_idx] += 1

        landed_on_boundary = boundary[rows[active_idx], cols[active_idx]]
        finished_idx = active_idx[landed_on_boundary]
        exit_rows[finished_idx] = rows[finished_idx]
        exit_cols[finished_idx] = cols[finished_idx]
        exit_steps[finished_idx] = steps[finished_idx]
        active[finished_idx] = False

    n_unfinished = int(active.sum())
    if n_unfinished:
        print(f"warning: {n_unfinished} trial(s) did not reach the boundary "
              f"within {max_steps} steps, try raising max_steps")

    return exit_rows, exit_cols, exit_steps


def expected_stopping_time(exit_steps):
    """Mean and standard error of the exit times (ignores unfinished trials)."""
    steps = np.asarray(exit_steps)
    steps = steps[steps >= 0]
    mean = steps.mean()
    sem = steps.std(ddof=1) / np.sqrt(len(steps))
    return mean, sem


def exit_distribution(exit_rows, exit_cols):
    """Empirical probability of exiting at each boundary cell, as a dict."""
    pairs = [p for p in zip(exit_rows.tolist(), exit_cols.tolist()) if p[0] >= 0]
    counts = Counter(pairs)
    total = sum(counts.values())
    return {cell: n / total for cell, n in counts.items()}


def interior_cells(interior_mask):
    """List of (row, col) coordinates that are valid starting points."""
    return list(zip(*np.where(interior_mask)))
