
import blender_plot as bp
import blender_plot.functional as bpf


import numpy as np


data = np.random.standard_normal((128, 3))

bpf.scatter(data)
bpf.render("renders/standard_normal.png")
bpf.save("blendfiles/standard_normal.blend")

