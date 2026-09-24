# Random walk on an n x m lattice

4-neighbor random walk on an n x m interior region with a 1-cell absorbing boundary ring around it (`shapes.rectangle(n, m)`).

num_trials = 20000, seed = 0

## Corners always have exit probability 0

A corner's only neighbors are two other boundary cells. A walk can't land on one directly; it's absorbed one step earlier. Holds for any n, m.

## 3 x 3 interior lattice

| starting point | (x, y) | expected stopping time |
|---|---|---|
| center | (2, 2) | 4.46 ± 0.02 |
| edge_horizontal | (1, 2) | 3.49 ± 0.02 |
| edge_vertical | (2, 1) | 3.49 ± 0.02 |
| corner | (1, 1) | 2.72 ± 0.02 |

### 3x3: center start (2, 2)

![lattice_3x3_center.png](lattice_3x3_center.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.062 | 0.121 | 0.065 | 0.000 (corner) |
| **3** | 0.063 | interior | interior | interior | 0.063 |
| **2** | 0.130 | interior | **start** | interior | 0.123 |
| **1** | 0.061 | interior | interior | interior | 0.063 |
| **0** | 0.000 (corner) | 0.063 | 0.124 | 0.061 | 0.000 (corner) |

### 3x3: edge_horizontal start (1, 2)

![lattice_3x3_edge_horizontal.png](lattice_3x3_edge_horizontal.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.099 | 0.064 | 0.028 | 0.000 (corner) |
| **3** | 0.097 | interior | interior | interior | 0.026 |
| **2** | 0.329 | **start** | interior | interior | 0.043 |
| **1** | 0.100 | interior | interior | interior | 0.028 |
| **0** | 0.000 (corner) | 0.096 | 0.062 | 0.028 | 0.000 (corner) |

### 3x3: edge_vertical start (2, 1)

![lattice_3x3_edge_vertical.png](lattice_3x3_edge_vertical.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.027 | 0.045 | 0.028 | 0.000 (corner) |
| **3** | 0.026 | interior | interior | interior | 0.027 |
| **2** | 0.063 | interior | interior | interior | 0.061 |
| **1** | 0.097 | interior | **start** | interior | 0.100 |
| **0** | 0.000 (corner) | 0.097 | 0.329 | 0.100 | 0.000 (corner) |

### 3x3: corner start (1, 1)

![lattice_3x3_corner.png](lattice_3x3_corner.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.030 | 0.027 | 0.013 | 0.000 (corner) |
| **3** | 0.031 | interior | interior | interior | 0.014 |
| **2** | 0.097 | interior | interior | interior | 0.029 |
| **1** | 0.303 | **start** | interior | interior | 0.031 |
| **0** | 0.000 (corner) | 0.293 | 0.102 | 0.029 | 0.000 (corner) |

## 5 x 5 interior lattice

| starting point | (x, y) | expected stopping time |
|---|---|---|
| center | (3, 3) | 10.40 ± 0.05 |
| edge_horizontal | (1, 3) | 6.15 ± 0.05 |
| edge_vertical | (3, 1) | 6.14 ± 0.05 |
| corner | (1, 1) | 3.76 ± 0.04 |

### 5x5: center start (3, 3)

![lattice_5x5_center.png](lattice_5x5_center.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **6** | 0.000 (corner) | 0.030 | 0.057 | 0.079 | 0.061 | 0.030 | 0.000 (corner) |
| **5** | 0.029 | interior | interior | interior | interior | interior | 0.030 |
| **4** | 0.057 | interior | interior | interior | interior | interior | 0.058 |
| **3** | 0.077 | interior | interior | **start** | interior | interior | 0.077 |
| **2** | 0.058 | interior | interior | interior | interior | interior | 0.054 |
| **1** | 0.027 | interior | interior | interior | interior | interior | 0.028 |
| **0** | 0.000 (corner) | 0.029 | 0.058 | 0.076 | 0.057 | 0.028 | 0.000 (corner) |

### 5x5: edge_horizontal start (1, 3)

![lattice_5x5_edge_horizontal.png](lattice_5x5_edge_horizontal.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **6** | 0.000 (corner) | 0.041 | 0.041 | 0.029 | 0.019 | 0.008 | 0.000 (corner) |
| **5** | 0.042 | interior | interior | interior | interior | interior | 0.008 |
| **4** | 0.117 | interior | interior | interior | interior | interior | 0.014 |
| **3** | 0.345 | **start** | interior | interior | interior | interior | 0.016 |
| **2** | 0.119 | interior | interior | interior | interior | interior | 0.013 |
| **1** | 0.041 | interior | interior | interior | interior | interior | 0.007 |
| **0** | 0.000 (corner) | 0.042 | 0.043 | 0.028 | 0.018 | 0.007 | 0.000 (corner) |

### 5x5: edge_vertical start (3, 1)

![lattice_5x5_edge_vertical.png](lattice_5x5_edge_vertical.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **6** | 0.000 (corner) | 0.007 | 0.014 | 0.017 | 0.013 | 0.007 | 0.000 (corner) |
| **5** | 0.007 | interior | interior | interior | interior | interior | 0.008 |
| **4** | 0.016 | interior | interior | interior | interior | interior | 0.018 |
| **3** | 0.029 | interior | interior | interior | interior | interior | 0.030 |
| **2** | 0.041 | interior | interior | interior | interior | interior | 0.041 |
| **1** | 0.041 | interior | interior | **start** | interior | interior | 0.041 |
| **0** | 0.000 (corner) | 0.041 | 0.121 | 0.346 | 0.120 | 0.042 | 0.000 (corner) |

### 5x5: corner start (1, 1)

![lattice_5x5_corner.png](lattice_5x5_corner.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| **6** | 0.000 (corner) | 0.006 | 0.008 | 0.008 | 0.006 | 0.003 | 0.000 (corner) |
| **5** | 0.006 | interior | interior | interior | interior | interior | 0.003 |
| **4** | 0.017 | interior | interior | interior | interior | interior | 0.005 |
| **3** | 0.039 | interior | interior | interior | interior | interior | 0.007 |
| **2** | 0.104 | interior | interior | interior | interior | interior | 0.009 |
| **1** | 0.304 | **start** | interior | interior | interior | interior | 0.006 |
| **0** | 0.000 (corner) | 0.302 | 0.102 | 0.042 | 0.018 | 0.005 | 0.000 (corner) |

## 3 x 4 interior lattice

| starting point | (x, y) | expected stopping time |
|---|---|---|
| center | (2, 2) | 5.34 ± 0.03 |
| edge_horizontal | (1, 2) | 3.87 ± 0.03 |
| edge_vertical | (2, 1) | 4.11 ± 0.03 |
| corner | (1, 1) | 2.99 ± 0.02 |

### 3x4: center start (2, 2)

![lattice_3x4_center.png](lattice_3x4_center.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.066 | 0.132 | 0.081 | 0.033 | 0.000 (corner) |
| **3** | 0.064 | interior | interior | interior | interior | 0.032 |
| **2** | 0.127 | interior | **start** | interior | interior | 0.056 |
| **1** | 0.064 | interior | interior | interior | interior | 0.033 |
| **0** | 0.000 (corner) | 0.066 | 0.134 | 0.081 | 0.031 | 0.000 (corner) |

### 3x4: edge_horizontal start (1, 2)

![lattice_3x4_edge_horizontal.png](lattice_3x4_edge_horizontal.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.097 | 0.064 | 0.033 | 0.014 | 0.000 (corner) |
| **3** | 0.102 | interior | interior | interior | interior | 0.013 |
| **2** | 0.332 | **start** | interior | interior | interior | 0.021 |
| **1** | 0.099 | interior | interior | interior | interior | 0.013 |
| **0** | 0.000 (corner) | 0.099 | 0.066 | 0.034 | 0.014 | 0.000 (corner) |

### 3x4: edge_vertical start (2, 1)

![lattice_3x4_edge_vertical.png](lattice_3x4_edge_vertical.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.027 | 0.050 | 0.038 | 0.017 | 0.000 (corner) |
| **3** | 0.029 | interior | interior | interior | interior | 0.015 |
| **2** | 0.065 | interior | interior | interior | interior | 0.031 |
| **1** | 0.103 | interior | **start** | interior | interior | 0.036 |
| **0** | 0.000 (corner) | 0.103 | 0.335 | 0.113 | 0.036 | 0.000 (corner) |

### 3x4: corner start (1, 1)

![lattice_3x4_corner.png](lattice_3x4_corner.png)

Exit probability by (x, y), y increasing upward:

| y \ x | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **4** | 0.000 (corner) | 0.032 | 0.028 | 0.016 | 0.009 | 0.000 (corner) |
| **3** | 0.033 | interior | interior | interior | interior | 0.008 |
| **2** | 0.100 | interior | interior | interior | interior | 0.012 |
| **1** | 0.294 | **start** | interior | interior | interior | 0.013 |
| **0** | 0.000 (corner) | 0.306 | 0.099 | 0.038 | 0.013 | 0.000 (corner) |

