

def test_import():
    import blender_plot as bp
    import bpy


def test_blender_version():
    import bpy
    assert bpy.app.version == (3, 4, 0)


def test_pip_install():
    import pip
    failed = pip.main(["install", "blender-plot"])

    assert not failed
