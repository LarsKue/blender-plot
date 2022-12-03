
import bpy
import mathutils


def look_at(focus: mathutils.Vector, camera: bpy.types.Camera = None):
    """ Rotate the camera to look at a target point """
    if camera is None:
        camera = bpy.context.scene.camera
    direction = camera.location - focus
    q = direction.to_track_quat("Z", "Y")

    camera.rotation_euler = q.to_euler()


def load_material(path):
    bpy.ops.wm.append(
        filepath=str(path / "Material" / path.stem),
        directory=str(path / "Material"),
        filename=path.stem,
        active_collection=False,
        set_fake=True,
    )
    material = bpy.data.materials.get(path.stem)

    return material
