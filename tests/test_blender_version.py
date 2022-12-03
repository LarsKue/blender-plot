
import bpy


def test_blender_version():
    assert bpy.app.version == (3, 4, 0)
