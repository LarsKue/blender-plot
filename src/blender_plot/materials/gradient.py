
from .base import Material
from .color import Color

import bpy
import numpy as np


class GradientMaterial(Material):
    def __init__(self, colors: list[Color], name: str = "Gradient"):
        blender_material = bpy.data.materials.new(name)
        blender_material.use_nodes = True
        nodes = blender_material.node_tree.nodes

        mix_node = nodes.new("ShaderNodeMix")
        mix_node.location = (-200, 0)
        mix_node.data_type = "RGBA"

        mix_node.inputs[6].default_value = colors[0]
        mix_node.inputs[7].default_value = colors[1]

        bsdf_node = nodes.get("Principled BSDF")

        attribute_hue_node = nodes.new("ShaderNodeAttribute")
        attribute_hue_node.location = (-400, 0)
        attribute_hue_node.attribute_name = "hue"
        attribute_hue_node.attribute_type = "INSTANCER"

        attribute_alpha_node = nodes.new("ShaderNodeAttribute")
        attribute_alpha_node.location = (-400, -200)
        attribute_alpha_node.attribute_name = "alpha"
        attribute_alpha_node.attribute_type = "INSTANCER"

        blender_material.node_tree.links.new(attribute_hue_node.outputs["Fac"], mix_node.inputs["Factor"])
        blender_material.node_tree.links.new(attribute_alpha_node.outputs["Fac"], bsdf_node.inputs["Alpha"])
        blender_material.node_tree.links.new(mix_node.outputs[2], bsdf_node.inputs["Base Color"])

        super().__init__(blender_material)

    def apply_to(self, obj: bpy.types.Object, hue: np.ndarray, alpha: float | np.ndarray):
        # Add hue attribute to the objects vertices
        vertices = obj.data.attributes.new("hue", "FLOAT", "POINT")
        vertices.data.foreach_set("value", hue)

        # Add alpha attribute to the objects vertices
        vertices = obj.data.attributes.new("alpha", "FLOAT", "POINT")
        vertices.data.foreach_set("value", np.full_like(hue, fill_value=alpha))
