"""
Reservoir research.
"""
###############################################################################
# read data
lines = [line.strip().split(',') for line in open("data/input17").readlines()]

# scan each line and update min max bounds
xmin, xmax, ymin, ymax = None, None, None, None


def update(before, new, operation):
    if before is None:
        after = new
    else:
        after = operation(before, new)
    return after


for line in lines:
    for part in line:
        if '..' in part:
            val1, val2 =  [int(val) for val in part[3:].split('..')]
            if 'x' in part:
                xmin = update(xmin, val1, min)
                xmax = update(xmax, val2, max)
            else:
                ymin = update(ymin, val1, min)
                ymax = update(ymax, val2, max)
        else:
            # there are no ..
            val = int(part.split('=')[1])
            if 'x' in part:
                xmin = update(xmin, val, min)
                xmax = update(xmax, val, max)
            else:
                ymin = update(ymin, val, min)
                ymax = update(ymax, val, max)

###############################################################################
# create grid and fill it
import numpy as np

grid = np.zeros((ymax+1, xmax+1))

for first, second in lines:
    if 'x' in first:
        # x=301, y=218..246
        x = int(first.split('=')[1])
        ys = [int(val) for val in second[3:].split('..')]
        y1 = ys[0]
        y2 = ys[1]
        grid[y1:y2+1, x] = 1
    else:
        # y=1424, x=368..830
        y = int(first.split('=')[1])
        xs = [int(val) for val in second[3:].split('..')]
        x1 = xs[0]
        x2 = xs[1]
        grid[y, x1:x2+1] = 1

###############################################################################
import matplotlib.pyplot as plt

plt.matshow(grid)

###############################################################################

