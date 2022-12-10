
import bpy


class Material:
    def __init__(self, blender_material: bpy.types.Material):
        self.blender_material = blender_material

    def apply_to(self, obj: bpy.types.Object, *args, **kwargs):
        raise NotImplementedError
