# PhaseDiagram
Adaptive-grid phase diagram calculation and plotting routines

## 2D phase diagrams
A small piece of code for plotting integer-valued functions over strangely shaped regions.

The general idea:
1. Define an initial series of points, and evaluate the phase function at those points.
2. Compute the Delaunay triangulation of this grid.
3. For every triangle with disagreeing edges, add an extra point in its centre.
4. Repeat.

This is defined for both 2D phase digrams, and for 3D unit sphere projections where 3 competing parameters are show normalised, e.g. to an overall energy scale.

Example usage, with a directory structure as follows:
```
test/PhaseDiagram.py
test/test.py
```

```python3
import numpy as np                 
import matplotlib.pyplot as plt

from PhaseDiagram import PhasePlane


def phase(X, Y):
    return np.where(X**2 + 4*Y**2 > 1, 1, 0) + np.where(X + Y > 0, 1, 0) 

p = PhasePlane(phase, ['A','B','C'], ['x1','x2'])
p.set_initpts(np.linspace(-1.5,1.5,10),np.linspace(-1.5,1.5,10))
           
p.refine(6)

p.plot()

plt.show()
```

`p.refine()` may be called any number of times. This is particularly useful in e.g. jupyter notebooks or ipython.


More examples are present in te `examples` folder, which I will gradually add to.
