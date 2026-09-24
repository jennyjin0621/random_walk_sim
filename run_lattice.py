"""
Monte Carlo random walk on an n x m lattice.

n, m are the interior dimensions; the boundary ring sits outside them
(see shapes.rectangle). Edit CONFIGS to change what runs.
"""

import numpy as np

import shapes
import random_walk as rw
import visualize as viz

NUM_TRIALS = 20_000
SEED = 0
PAD = 1

# Every (n, m) interior lattice to analyze. n = interior rows, m = interior
# columns. Add/remove/edit entries here to change what gets run.
CONFIGS = [
    (3, 3),
    (5, 5),
    (3, 4),
]


def to_mask_coords(i, j):
    """(i, j) 1-indexed within the n x m interior grid -> mask coordinates."""
    return (i + PAD, j + PAD)


def representative_starts(n, m):
    """Center, corner, one edge point per axis. Edge points match when n == m."""
    center_i, center_j = (n + 1) // 2, (m + 1) // 2
    return [
        ("center", (center_i, center_j)),
        ("edge_horizontal", (center_i, 1)),  # next to the left/right side
        ("edge_vertical", (1, center_j)),    # next to the top/bottom side
        ("corner", (1, 1)),
    ]


def corner_cells(mask):
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    r0, r1, c0, c1 = rows.min(), rows.max(), cols.min(), cols.max()
    return {(r0, c0), (r0, c1), (r1, c0), (r1, c1)}


def grid_markdown_table(mask, boundary, probs, start, corners):
    """Table laid out like the grid, (x, y) labels, largest y on top to match the plot."""
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    r0, r1, c0, c1 = rows.min(), rows.max(), cols.min(), cols.max()

    header = ["y \\ x"] + [str(c - PAD) for c in range(c0, c1 + 1)]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in range(r1, r0 - 1, -1):
        row_cells = [f"**{r - PAD}**"]
        for c in range(c0, c1 + 1):
            cell = (r, c)
            if not mask[cell]:
                text = ""
            elif boundary[cell]:
                text = f"{probs.get(cell, 0.0):.3f}"
                if cell in corners:
                    text += " (corner)"
            elif cell == start:
                text = "**start**"
            else:
                text = "interior"
            row_cells.append(text)
        lines.append("| " + " | ".join(row_cells) + " |")
    return "\n".join(lines)


def run_config(n, m, rng):
    mask = shapes.rectangle(n, m, pad=PAD)
    interior, boundary = shapes.classify(mask)
    corners = corner_cells(mask)

    runs = []
    for label, (i, j) in representative_starts(n, m):
        start = to_mask_coords(i, j)
        point = shapes.mask_to_point(start, PAD)
        if not interior[start]:
            raise ValueError(f"{start} ({label}) is not an interior cell "
                              f"for a {n}x{m} lattice")

        exit_rows, exit_cols, exit_steps = rw.simulate_walks(
            boundary, start, NUM_TRIALS, rng=rng
        )
        mean_time, sem_time = rw.expected_stopping_time(exit_steps)
        probs = rw.exit_distribution(exit_rows, exit_cols)

        print(f"  {label} {point}: stopping time = {mean_time:.2f} +/- {sem_time:.2f}")

        image = f"lattice_{n}x{m}_{label}.png"
        fig = viz.plot_boundary_gradient(
            mask, boundary, probs, start,
            title=f"{n}x{m} lattice: exit probability from {label} {point}"
        )
        fig.savefig(image, dpi=200, bbox_inches="tight")

        runs.append({
            "label": label, "start": start, "point": point,
            "mean_time": mean_time, "sem_time": sem_time,
            "grid_table": grid_markdown_table(mask, boundary, probs, start, corners),
            "image": image,
        })

    return runs


def write_report(all_results, path="RESULTS.md"):
    lines = [
        "# Random walk on an n x m lattice\n",
        "4-neighbor random walk on an n x m interior region with a 1-cell "
        "absorbing boundary ring around it (`shapes.rectangle(n, m)`).\n",
        f"num_trials = {NUM_TRIALS}, seed = {SEED}\n",
        "## Corners always have exit probability 0\n",
        "A corner's only neighbors are two other boundary cells. A walk "
        "can't land on one directly; it's absorbed one step earlier. "
        "Holds for any n, m.\n",
    ]

    for (n, m), runs in all_results.items():
        lines.append(f"## {n} x {m} interior lattice\n")
        lines.append("| starting point | (x, y) | expected stopping time |")
        lines.append("|---|---|---|")
        for r in runs:
            lines.append(f"| {r['label']} | {r['point']} | "
                          f"{r['mean_time']:.2f} ± {r['sem_time']:.2f} |")
        lines.append("")

        for r in runs:
            lines.append(f"### {n}x{m}: {r['label']} start {r['point']}\n")
            lines.append(f"![{r['image']}]({r['image']})\n")
            lines.append("Exit probability by (x, y), y increasing upward:\n")
            lines.append(r["grid_table"])
            lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {path}")


def main():
    rng = np.random.default_rng(SEED)
    all_results = {}
    for n, m in CONFIGS:
        print(f"{n}x{m}:")
        all_results[(n, m)] = run_config(n, m, rng)
    write_report(all_results)


if __name__ == "__main__":
    main()
