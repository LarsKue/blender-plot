#
# import blender_plot as bp
#
# import numpy as np
#
# r = 1.0
# phi = np.linspace(0, 2 * np.pi, 100)
# theta = np.linspace(0, np.pi, 100)
#
# rr, pp, tt = np.meshgrid(r, phi, theta)
# rr = rr.flatten()
# pp = pp.flatten()
# tt = tt.flatten()
#
# x = rr * np.sin(tt) * np.cos(pp)
# y = rr * np.sin(tt) * np.sin(pp)
# z = rr * np.cos(tt)
#
# data = np.stack([x, y, z], axis=1)
#
# data = np.random.standard_normal((1024, 3))
#
# s = bp.DefaultScene()
# # s.scatter(data, radius=0.01, material="rainbow", alpha=0.05)
# # s.scatter(data)
# # s.render("renders/standard_normal.png", resolution=(1200, 1200))
# # s.save("blendfiles/standard_normal.blend")
#
#


import bpy
from functools import wraps


def activates(f):
    @wraps(f)
    def inner(*args, **kwargs):
        print(self)
        self.activate()
        return f(self, *args, **kwargs)

    return inner


class Scene:
    """ Base Scene, empty by default """

    def __init__(self):
        # create new blender scene
        self.blender_scene = bpy.data.scenes.new(self.__class__.__name__)
        self.clear()

    def activate(self):
        bpy.context.window.scene = self.blender_scene

    @property
    def active(self):
        return bpy.context.window.scene is self.blender_scene

    @activates
    def clear(self):
        print("Base Clear")


print("construct")
b1 = Scene()

print("set scene")
s1 = b1.blender_scene

print("assert1")
assert bpy.context.window.scene is s1

print("construct")
b2 = Scene()
print("set scene")
s2 = b2.blender_scene

print("assert2")
assert bpy.context.window.scene is s2

print("do stuff")
b1.clear()

print("assert3")
assert bpy.context.window.scene is s1

