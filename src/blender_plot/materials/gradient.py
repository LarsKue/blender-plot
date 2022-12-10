
from .base import Material
from .color import Color

import bpy


class GradientMaterial(Material):
    def __init__(self, colors: list[Color], name: str = "Gradient"):
        blender_material = bpy.data.materials.new(name)
        blender_material.use_nodes = True
        nodes = blender_material.node_tree.nodes
        mix_node = nodes.new("ShaderNodeMix")
        mix_node.data_type = "RGBA"

        mix_node.inputs[6].default_value = colors[0]
        mix_node.inputs[7].default_value = colors[1]

        super().__init__(blender_material)
