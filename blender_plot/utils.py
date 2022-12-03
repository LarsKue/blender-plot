
import bpy
import mathutils
import pathlib


def look_at(focus: mathutils.Vector, camera: bpy.types.Camera = None):
    """ Rotate the camera to look at a target point """
    if camera is None:
        camera = bpy.context.scene.camera
    # this is consistent with the blender built-in TrackTo constraint
    direction = focus - camera.location
    q = direction.to_track_quat("-Z", "Y")

    camera.rotation_euler = q.to_euler()


def load_material(name):
    # TODO: find package folder
    path = pathlib.Path.cwd() / "materials" / name
    path = path.with_suffix(".blend")
    if not path.is_file():
        raise ValueError(f"Unknown material: {name}")

    bpy.ops.wm.append(
        filepath=str(path / "Material" / path.stem),
        directory=str(path / "Material"),
        filename=path.stem,
        active_collection=False,
        set_fake=True,
    )
    material = bpy.data.materials.get(path.stem)

    return material
