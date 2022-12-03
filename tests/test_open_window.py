
import bpy


def test_open_window():
    bpy.ops.wm.save_as_mainfile(filepath="/tmp/blend.blend")

    # bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)
