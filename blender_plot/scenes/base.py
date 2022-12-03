import mathutils

import blender_plot as bp
import blender_plot.functional as bpf

import bpy
from IPython import display
import pathlib


class Scene:
    """ Base Scene, empty by default """

    def __init__(self):
        super().__init__()
        self.clear()

    def clear(self):
        """ Return the Scene to its default state """

        # create new empty scene
        # TODO: check validity
        bpy.context.window.scene = bpy.data.scenes.new("Scene")
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)

        # bpy.context.window.scene = bpy.data.scenes.new("Scene")
        # print(list(bpy.data.objects))


        # create a new camera
        camera_data = bpy.data.cameras.new("Camera")
        camera_object = bpy.data.objects.new(camera_data.name, camera_data)

        # look at data from positive quadrant
        camera_object.location = (5, 5, 5)

        # link the object
        bpy.context.collection.objects.link(camera_object)

        # set as active camera
        bpy.context.scene.camera = camera_object

        # look at origin
        origin = mathutils.Vector()
        bpf.look_at(origin)


    def render(self, filepath="render.png", resolution=(800, 600), device="gpu", samples=16):
        """ Render the scene to an image or video """
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
        return display.Image(str(filepath))

    def save(self, filepath="plot.blend"):
        """ Save the scene to a blend file """
        filepath = pathlib.Path(filepath).resolve()
        filepath.parent.mkdir(exist_ok=True, parents=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(filepath))
