"""n x m lattice: an n x m interior region with its own absorbing boundary ring."""

import numpy as np

NEIGHBOR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def rectangle(n, m, pad=1):
    """n, m are the interior dimensions; the boundary ring sits outside them."""
    rows = n + 2 + 2 * pad
    cols = m + 2 + 2 * pad
    mask = np.zeros((rows, cols), dtype=bool)
    mask[pad:pad + n + 2, pad:pad + m + 2] = True
    return mask


def mask_to_point(cell, pad=1):
    """Array (row, col) -> lattice point (x, y), 0-indexed from the boundary's outer edge."""
    row, col = cell
    return (col - pad, row - pad)


def point_to_mask(point, pad=1):
    """Inverse of mask_to_point."""
    x, y = point
    return (y + pad, x + pad)


def classify(mask):
    """Split into interior cells (all 4 neighbors in-shape) and boundary cells."""
    rows, cols = mask.shape
    interior = np.zeros_like(mask, dtype=bool)
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c]:
                continue
            all_neighbors_in = True
            for dr, dc in NEIGHBOR_OFFSETS:
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols or not mask[nr, nc]:
                    all_neighbors_in = False
                    break
            interior[r, c] = all_neighbors_in
    boundary = mask & ~interior
    return interior, boundary
