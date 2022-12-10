
import blender_plot as bp

import bpy
import pathlib
import mathutils
import subprocess
import tempfile


class Scene:
    """ Base Scene, empty by default """

    def __init__(self):
        # create new blender scene
        self.blender_scene = bpy.data.scenes.new(self.__class__.__name__)
        self.clear()

    def __del__(self):
        # delete the blender scene
        bpy.data.scenes.remove(self.blender_scene)

    def activate(self):
        """ Activate the scene in blender """
        bpy.context.window.scene = self.blender_scene

    @property
    def active(self):
        """ Returns if the current scene is the active one """
        return bpy.context.window.scene is self.blender_scene

    def clear(self):
        """ Return the Scene to its default state """
        self.activate()
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)

        # create a new camera
        camera_data = bpy.data.cameras.new("Camera")
        camera_data.type = "ORTHO"
        camera_data.ortho_scale = 10.0
        camera_object = bpy.data.objects.new(camera_data.name, camera_data)

        # look at data from positive quadrant
        camera_object.location = (10, 10, 10)

        # link the object
        bpy.context.collection.objects.link(camera_object)

        # set as active camera
        bpy.context.scene.camera = camera_object

        # look at origin
        origin = mathutils.Vector()
        bp.utils.look_at(origin)

    def render(self, filepath="render.png", resolution=(800, 600), device="gpu", samples=16):
        """ Render the scene to an image or video """
        self.activate()

        filepath = pathlib.Path(filepath).resolve()

        bpy.context.scene.render.engine = "CYCLES"
        bpy.context.scene.cycles.device = device.upper()
        bpy.context.scene.cycles.samples = samples
        bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "OPTIX"
        bpy.context.scene.render.film_transparent = True

        # turn on for improved performance when rendering multiple similar images
        bpy.context.scene.render.use_persistent_data = True

        bpy.context.scene.render.filepath = str(filepath)
        bpy.context.scene.render.image_settings.file_format = filepath.suffix[1:].upper()
        bpy.context.scene.render.resolution_x = resolution[0]
        bpy.context.scene.render.resolution_y = resolution[1]
        bpy.ops.render.render(write_still=True)

        # TODO: detect IPython
        # return display.Image(str(filepath))

    def save(self, filepath="plot.blend"):
        """ Save the scene to a blend file """
        self.activate()

        filepath = pathlib.Path(filepath).with_suffix(".blend").resolve()
        filepath.parent.mkdir(exist_ok=True, parents=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(filepath))

    def load(self, filepath):
        """ Load a scene from a blend file """
        self.activate()

        filepath = pathlib.Path(filepath).with_suffix(".blend").resolve()
        bpy.ops.wm.open_mainfile(filepath=str(filepath))

    def open(self):
        """ Open the last saved scene in your locally installed Blender """
        self.activate()
        if not bpy.data.is_saved:
            temp_file = tempfile.TemporaryFile(suffix=".blend")
            self.save(str(temp_file))

        current_file = bpy.data.filepath
        subprocess.run(["blender", current_file])

    def scatter(self, *args, **kwargs):
        return bp.scatter(self, *args, **kwargs)
