# blender-plot
A High-Level Plotting Interface for Blender in Python.

## Install:
`pip install blender-plot`

## Example:

```python
import blender_plot as bp
import numpy as np

# create 512 normally distributed 3d points
data = np.random.standard_normal((512, 3))

s = bp.DefaultScene()
s.scatter(data)

# render the scene to an image
s.render("standard_normal.png", resolution=(1200, 1200))

# save the scene to a .blend file
s.save("standard_normal.blend")
```

### Output:

![Output Image](examples/standard_normal.png)
