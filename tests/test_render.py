

import blenderplot as bp
import bpy
import pathlib
import os


def test_render():
    path = pathlib.Path(os.getcwd()) / "renders" / "render.png"
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
