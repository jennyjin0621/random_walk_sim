"""
Expected time to first reach L1 distance d from the origin.

A truly unbounded walk has infinite expected first-passage time to any
fixed distance (2D simple random walk is null recurrent: it gets there
eventually with probability 1, but the tail is heavy enough that the
mean diverges). So we put a wide absorbing wall far past any distance
we actually report, and read off each trial's running-max distance as
it passes through every smaller shell on the way out. One batch of
walks gives every d at once, since L1 distance from the origin changes
by exactly +-1 per step and can't skip a shell.
"""

import numpy as np

MAX_D_REPORT = 20
D_MAX = 3 * MAX_D_REPORT
NUM_TRIALS = 50_000
SEED = 0
MAX_STEPS = 200_000

DIRECTIONS = np.array([(-1, 0), (1, 0), (0, -1), (0, 1)])


def simulate_distance_growth(d_max, num_trials, max_steps=MAX_STEPS, rng=None):
    """
    Returns first_time, shape (num_trials, d_max + 1): first_time[i, d] is
    the step at which trial i's L1 distance from the origin first reached
    d (-1 if the wall at d_max was hit before that, which shouldn't happen
    for d < d_max).
    """
    if rng is None:
        rng = np.random.default_rng()

    x = np.zeros(num_trials, dtype=np.int64)
    y = np.zeros(num_trials, dtype=np.int64)
    steps = np.zeros(num_trials, dtype=np.int64)
    current_max = np.zeros(num_trials, dtype=np.int64)
    active = np.ones(num_trials, dtype=bool)

    first_time = np.full((num_trials, d_max + 1), -1, dtype=np.int64)
    first_time[:, 0] = 0

    for _ in range(max_steps):
        if not active.any():
            break
        idx = np.where(active)[0]
        moves = DIRECTIONS[rng.integers(0, 4, size=idx.size)]
        x[idx] += moves[:, 0]
        y[idx] += moves[:, 1]
        steps[idx] += 1

        dist = np.abs(x[idx]) + np.abs(y[idx])
        advanced = dist > current_max[idx]
        adv_idx = idx[advanced]
        if adv_idx.size:
            new_d = dist[advanced]
            first_time[adv_idx, new_d] = steps[adv_idx]
            current_max[adv_idx] = new_d
            active[adv_idx[new_d >= d_max]] = False

    n_unfinished = int(active.sum())
    if n_unfinished:
        print(f"warning: {n_unfinished} trial(s) never reached the wall "
              f"within {max_steps} steps")

    return first_time


def summarize(first_time, max_d_report):
    results = []
    for d in range(2, max_d_report + 1):
        times = first_time[:, d]
        times = times[times >= 0]
        mean = times.mean()
        sem = times.std(ddof=1) / np.sqrt(len(times))
        results.append((d, mean, sem))
    return results


def main():
    rng = np.random.default_rng(SEED)
    first_time = simulate_distance_growth(D_MAX, NUM_TRIALS, rng=rng)
    assert np.all(first_time[:, 1] == 1), "distance 1 should always take exactly 1 step"

    results = summarize(first_time, MAX_D_REPORT)

    print(f"{'d':>4} {'E[time]':>10} {'SEM':>8} {'time/d^2':>10}")
    for d, mean, sem in results:
        print(f"{d:>4} {mean:>10.2f} {sem:>8.2f} {mean / d**2:>10.4f}")

    lines = [
        "# Expected time to reach L1 distance d\n",
        f"First-passage time to L1 distance d from the origin, unbounded "
        f"except for a safety wall at d = {D_MAX} (well past anything "
        "reported here, so it doesn't bias these numbers).\n",
        f"num_trials = {NUM_TRIALS}, seed = {SEED}\n",
        "| d | E[time] | SEM | time / d^2 |",
        "|---|---|---|---|",
    ]
    for d, mean, sem in results:
        lines.append(f"| {d} | {mean:.2f} | {sem:.2f} | {mean / d**2:.4f} |")

    with open("DISTANCE_GROWTH.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote DISTANCE_GROWTH.md")


if __name__ == "__main__":
    main()
