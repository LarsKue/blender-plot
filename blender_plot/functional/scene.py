
import blender_plot as bp

_active_scene = None


def scene():
    global _active_scene
    if _active_scene is None:
        _active_scene = bp.DefaultScene()

    return _active_scene


def clear():
    return scene().clear()


def render(*args, **kwargs):
    return scene().render(*args, **kwargs)


def save(*args, **kwargs):
    return scene().save(*args, **kwargs)
