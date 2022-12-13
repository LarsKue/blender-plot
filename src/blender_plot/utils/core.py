
import blender_plot as bp

import bpy
import mathutils
import numpy as np


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


def vertices_to_array(vertices) -> np.ndarray:
    """ Convert the coords of all vertices of a mesh to a numpy array """
    count = len(vertices)
    shape = (count, 3)
    verts = np.empty(count * 3, dtype=np.float64)
    vertices.foreach_get('co', verts)
    verts.shape = shape
    return verts


def normalize(x: np.ndarray, axis: int = None) -> np.ndarray:
    """ Normalize x to [0, 1] """
    x = x - np.min(x, axis=axis, keepdims=True)
    x = x / np.max(x, axis=axis, keepdims=True)
    return x



