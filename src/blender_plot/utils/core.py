
import blender_plot as bp

import bpy
import mathutils


def look_at(focus: mathutils.Vector, camera: bpy.types.Camera | None = None):
    """ Rotate the camera to look at a target point """
    if camera is None:
        camera = bpy.context.scene.camera
    # this is consistent with the blender built-in TrackTo constraint
    direction = focus - camera.location
    q = direction.to_track_quat("-Z", "Y")

    camera.rotation_euler = q.to_euler()


def get_material(material: str) -> bp.materials.Material:
    try:
        return getattr(bp.materials.collection, material)
    except AttributeError:
        raise ValueError(f"No such material: {material}")
