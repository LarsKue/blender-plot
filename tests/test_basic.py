

def test_import():
    import blender_plot as bp
    import bpy


def test_blender_version():
    import bpy
    assert bpy.app.version == (3, 4, 0)


def test_install():
    import sys
    import os

    os.system(" ".join([sys.executable, "-m", "venv", ".test_venv"]))
    os.system(" ".join(["source", ".test_venv/bin/activate"]))
    os.system(" ".join(["pip", "install", "-U", "pip", "setuptools", "wheel"]))
    failed = os.system(" ".join(["pip", "install", "."]))
    os.system(" ".join(["deactivate"]))
    os.system(" ".join(["rm", "-rf", ".test_venv"]))

    assert not failed


def test_pip_install():
    import pip
    failed = pip.main(["install", "blender-plot"])

    assert not failed
