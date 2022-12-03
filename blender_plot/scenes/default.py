
from .base import Scene

import bpy
import numpy as np


class DefaultScene(Scene):
    """
    This is the default scene used for plotting - not to be confused with the default Blender scene (for that use the base Scene)
    """
    def clear(self):
        super().clear()

        # use a sun as the light source
        light_data = bpy.data.lights.new("Light", type="SUN")
        light_data.angle = np.deg2rad(45)
        light_data.energy = 5.0

        # make object from data
        light_object = bpy.data.objects.new(light_data.name, light_data)
        light_object.rotation_euler = tuple(np.deg2rad((20, 20, 90)))

        # link the object
        bpy.context.collection.objects.link(light_object)

        # add shadow catcher
        bpy.ops.mesh.primitive_plane_add(
            size=10000,
            location=(0, 0, -3),
        )
        floor = bpy.data.objects.get("Plane")
        floor.is_shadow_catcher = True

