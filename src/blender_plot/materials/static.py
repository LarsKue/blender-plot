
from .base import Material

import bpy
import pathlib


class StaticMaterial(Material):
    """ Static Material that is loaded from a file """
    def __init__(self, filepath: pathlib.Path, name: str = None):
        if name is None:
            name = filepath.stem

        bpy.ops.wm.append(
            filepath=str(filepath / "Material" / name),
            directory=str(filepath / "Material"),
            filename=name,
            active_collection=False,
            set_fake=True,
        )
        blender_material = bpy.data.materials.get(name)

        super().__init__(blender_material)

    def apply_to(self, obj: bpy.types.Object, *args, **kwargs):
        pass
