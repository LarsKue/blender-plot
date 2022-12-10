
import bpy


class Material:
    def __init__(self, blender_material: bpy.types.Material):
        self.blender_material = blender_material
