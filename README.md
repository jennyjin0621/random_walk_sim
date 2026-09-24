# Random walk on Z^2 - simulation

Monte Carlo side of the 18.821 project on random walks on the integer
lattice. Alan and Pravan are working the analytical side; this checks
their results numerically and lets us sweep over shapes/starting points
that are annoying to do by hand.

## Setup

Simple random walk on an n x m grid, 4 neighbors, 1/4 each. The walk
starts somewhere in the interior and stops the first time it hits the
boundary (a 1-cell ring around the n x m region, not part of n or m).
For a handful of starting points we estimate the expected stopping time
and the exit-probability distribution over the boundary.

## Files

- `shapes.py` - builds the grid + boundary ring, splits interior/boundary
- `random_walk.py` - runs the walks, computes stopping time and exit distribution
- `visualize.py` - exit-probability heatmap plot
- `run_lattice.py` - runs everything, writes `RESULTS.md`

## Running it

Edit `CONFIGS` at the top of `run_lattice.py`:

```python
CONFIGS = [(3, 3), (5, 5), (3, 4)]
```

then

```
python run_lattice.py
```

Overwrites `RESULTS.md` and the `lattice_*.png` plots.
