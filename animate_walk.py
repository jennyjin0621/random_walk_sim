"""
One random walk trajectory on the 3x3 lattice, animated for the slides.
Same example as the paper. Not part of the run_lattice.py pipeline, just
a single path, step by step, from start to absorption.
"""

import matplotlib.animation as animation
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

import shapes

N = M = 3  # interior dimensions; the paper's "5x5 lattice" is this + the boundary ring
PAD = 1
START_POINT = (2, 2)  # lattice point (x, y), matches the paper's center start
SEED = 5  # fixed for a reproducible, presentation-length path (12 steps)

_SURFACE = "#fcfcfb"
_INTERIOR_FILL = "#e9e7e1"
_BOUNDARY_FILL = "#cde2fb"
_GRIDLINE = "#c9c8c1"
_INK_PRIMARY = "#0b0b0b"
_INK_MUTED = "#7a7972"
_BALL_COLOR = "#e34948"

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def walk_path(boundary, start, rng):
    path = [start]
    pos = start
    while not boundary[pos]:
        dr, dc = DIRECTIONS[rng.integers(4)]
        pos = (pos[0] + dr, pos[1] + dc)
        path.append(pos)
    return path


def main():
    rng = np.random.default_rng(SEED)
    mask = shapes.rectangle(N, M, pad=PAD)
    interior, boundary = shapes.classify(mask)
    start = shapes.point_to_mask(START_POINT, PAD)
    if not interior[start]:
        raise ValueError(f"{START_POINT} is not an interior lattice point")

    path = walk_path(boundary, start, rng)
    exit_point = shapes.mask_to_point(path[-1], PAD)
    print(f"steps to absorption: {len(path) - 1}, exit point: {exit_point}")

    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    r0, r1, c0, c1 = rows.min(), rows.max(), cols.min(), cols.max()
    nrows, ncols = r1 - r0 + 1, c1 - c0 + 1

    fig, ax = plt.subplots(figsize=(5.5, 6))
    fig.patch.set_facecolor(_SURFACE)

    rgb = np.ones((nrows, ncols, 3))
    for i in range(nrows):
        for j in range(ncols):
            cell = (r0 + i, c0 + j)
            if not mask[cell]:
                continue
            rgb[i, j] = mcolors.to_rgb(_BOUNDARY_FILL if boundary[cell] else _INTERIOR_FILL)
    ax.imshow(rgb, origin="lower", extent=(-0.5, ncols - 0.5, -0.5, nrows - 0.5))

    ax.set_xticks(np.arange(-0.5, ncols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, nrows, 1), minor=True)
    ax.grid(which="minor", color=_GRIDLINE, linewidth=1)
    ax.tick_params(which="minor", length=0)
    ax.set_xticks(np.arange(ncols))
    ax.set_xticklabels(np.arange(c0, c1 + 1) - PAD, fontsize=8, color=_INK_MUTED)
    ax.set_yticks(np.arange(nrows))
    ax.set_yticklabels(np.arange(r0, r1 + 1) - PAD, fontsize=8, color=_INK_MUTED)
    ax.tick_params(which="major", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("x", fontsize=9, color=_INK_MUTED)
    ax.set_ylabel("y", fontsize=9, color=_INK_MUTED, rotation=0, labelpad=8)
    ax.set_xlim(-0.5, ncols - 0.5)
    ax.set_ylim(-0.5, nrows - 0.5)
    ax.set_aspect("equal")
    ax.set_title(f"Random walk on a {N}x{M} lattice", fontsize=13,
                 color=_INK_PRIMARY, pad=10)

    def to_xy(cell):
        return cell[1] - c0, cell[0] - r0

    trail_line, = ax.plot([], [], color=_BALL_COLOR, linewidth=1.5, alpha=0.5, zorder=3)
    visited = ax.scatter([], [], s=40, facecolor=_BALL_COLOR, alpha=0.35, zorder=3)
    ball = ax.scatter([], [], s=220, facecolor=_BALL_COLOR, edgecolor="white",
                       linewidths=1.5, zorder=5)
    step_text = fig.text(0.5, 0.03, "", ha="center", fontsize=12, color=_INK_PRIMARY)
    fig.subplots_adjust(bottom=0.12)

    def update(frame):
        xs = [to_xy(c)[0] for c in path[:frame + 1]]
        ys = [to_xy(c)[1] for c in path[:frame + 1]]
        trail_line.set_data(xs, ys)
        visited.set_offsets(np.column_stack([xs[:-1], ys[:-1]]) if frame > 0 else np.empty((0, 2)))
        ball.set_offsets([[xs[-1], ys[-1]]])
        if frame == len(path) - 1:
            step_text.set_text(f"step {frame}, absorbed at {exit_point}")
        else:
            step_text.set_text(f"step {frame}")
        return trail_line, visited, ball, step_text

    hold_frames = 8
    frame_indices = list(range(len(path))) + [len(path) - 1] * hold_frames

    anim = animation.FuncAnimation(fig, update, frames=frame_indices, interval=400)

    anim.save(f"random_walk_{N}x{M}.gif", writer=animation.PillowWriter(fps=2.5))
    print(f"saved random_walk_{N}x{M}.gif")

    anim.save(f"random_walk_{N}x{M}.mp4", writer=animation.FFMpegWriter(fps=2.5))
    print(f"saved random_walk_{N}x{M}.mp4")


if __name__ == "__main__":
    main()
