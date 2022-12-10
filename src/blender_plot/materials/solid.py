
from .base import Material
from .color import Color

import bpy


class SolidColorMaterial(Material):
    def __init__(self, color: Color, name: str = "Solid"):
        blender_material = bpy.data.materials.new(name)
        blender_material.use_nodes = True
        nodes = blender_material.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = color

        super().__init__(blender_material)
