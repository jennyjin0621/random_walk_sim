"""Plotting helpers. Just draws results computed elsewhere, no simulation here."""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

# sequential blue ramp (light to dark) + neutral chart colors
_SEQUENTIAL_BLUE_HEX = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
SEQUENTIAL_BLUE = mcolors.LinearSegmentedColormap.from_list(
    "seq_blue", _SEQUENTIAL_BLUE_HEX
)

_SURFACE = "#fcfcfb"
_INTERIOR_FILL = "#e9e7e1"
_OUTSIDE_FILL = "#ffffff"
_GRIDLINE = "#c9c8c1"
_INK_PRIMARY = "#0b0b0b"
_INK_MUTED = "#7a7972"


def _label_ink(rgba):
    """White or dark ink, whichever clears contrast against this fill."""
    r, g, b = rgba[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#ffffff" if luminance < 0.55 else _INK_PRIMARY


def _bounding_box(mask):
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    return int(rows.min()), int(rows.max()), int(cols.min()), int(cols.max())


def _draw_boundary_gradient(ax, mask, boundary_mask, boundary_probs, start,
                             vmax=None, cmap=SEQUENTIAL_BLUE):
    """
    Draw the shape cropped to its bounding box: interior cells shaded flat
    gray, boundary cells colored by exit probability and labeled with the
    value, start cell marked with a star. Axis ticks are mask coordinates.
    """
    r0, r1, c0, c1 = _bounding_box(mask)
    sub_mask = mask[r0:r1 + 1, c0:c1 + 1]
    sub_boundary = boundary_mask[r0:r1 + 1, c0:c1 + 1]
    nrows, ncols = sub_mask.shape

    if vmax is None:
        vmax = max(boundary_probs.values()) if boundary_probs else 1.0
        vmax = vmax if vmax > 0 else 1.0
    norm = mcolors.Normalize(vmin=0.0, vmax=vmax)

    rgb = np.full((nrows, ncols, 3), mcolors.to_rgb(_OUTSIDE_FILL))
    for i in range(nrows):
        for j in range(ncols):
            if not sub_mask[i, j]:
                continue
            rgb[i, j] = (
                mcolors.to_rgb(_INTERIOR_FILL) if not sub_boundary[i, j]
                else cmap(norm(boundary_probs.get((r0 + i, c0 + j), 0.0)))[:3]
            )

    ax.imshow(rgb, origin="upper", extent=(-0.5, ncols - 0.5, nrows - 0.5, -0.5))

    for i in range(nrows):
        for j in range(ncols):
            if sub_boundary[i, j]:
                p = boundary_probs.get((r0 + i, c0 + j), 0.0)
                ax.text(j, i, f"{p:.3f}", ha="center", va="center",
                        fontsize=7.5, family="monospace",
                        color=_label_ink(cmap(norm(p))))

    sr, sc = start[0] - r0, start[1] - c0
    ax.scatter([sc], [sr], marker="*", s=260, facecolor=_INK_PRIMARY,
               edgecolor="white", linewidths=1.2, zorder=5)

    ax.set_xticks(np.arange(-0.5, ncols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, nrows, 1), minor=True)
    ax.grid(which="minor", color=_GRIDLINE, linewidth=1)
    ax.tick_params(which="minor", length=0)

    ax.set_xticks(np.arange(ncols))
    ax.set_xticklabels(np.arange(c0, c1 + 1), fontsize=8, color=_INK_MUTED)
    ax.set_yticks(np.arange(nrows))
    ax.set_yticklabels(np.arange(r0, r1 + 1), fontsize=8, color=_INK_MUTED)
    ax.tick_params(which="major", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xlim(-0.5, ncols - 0.5)
    ax.set_ylim(nrows - 0.5, -0.5)
    ax.set_aspect("equal")

    return plt.cm.ScalarMappable(cmap=cmap, norm=norm)


def plot_boundary_gradient(mask, boundary_mask, boundary_probs, start, title=None):
    """Color each boundary cell by its probability of being the exit point."""
    fig, ax = plt.subplots(figsize=(5.5, 5.2))
    fig.patch.set_facecolor(_SURFACE)
    sm = _draw_boundary_gradient(ax, mask, boundary_mask, boundary_probs, start)
    cbar = fig.colorbar(sm, ax=ax, label="exit probability", shrink=0.85)
    cbar.outline.set_visible(False)
    if title:
        ax.set_title(title, fontsize=12, color=_INK_PRIMARY, pad=10)
    fig.tight_layout()
    return fig
