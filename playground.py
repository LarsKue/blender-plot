
import blender_plot as bp

import numpy as np

r = 1.0
phi = np.linspace(0, 2 * np.pi, 100)
theta = np.linspace(0, np.pi, 100)

rr, pp, tt = np.meshgrid(r, phi, theta)
rr = rr.flatten()
pp = pp.flatten()
tt = tt.flatten()

x = rr * np.sin(tt) * np.cos(pp)
y = rr * np.sin(tt) * np.sin(pp)
z = rr * np.cos(tt)

data = np.stack([x, y, z], axis=1)

s = bp.DefaultScene()
s.scatter(data, radius=0.01)
s.save("blendfiles/standard_normal.blend")
s.render("renders/standard_normal.png")


