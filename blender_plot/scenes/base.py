import mathutils

import blender_plot as bp

import bpy
# from IPython import display
import pathlib

import numpy as np


class Scene:
    """ Base Scene, empty by default """
    def __init__(self):
        # create new blender scene
        bpy.context.window.scene = bpy.data.scenes.new(self.__class__.__name__)
        self.clear()

    def clear(self):
        """ Return the Scene to its default state """
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o, do_unlink=True)

        # bpy.context.window.scene = bpy.data.scenes.new("Scene")
        # print(list(bpy.data.objects))

        # create a new camera
        camera_data = bpy.data.cameras.new("Camera")
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
        filepath = pathlib.Path(filepath).resolve()
        filepath.parent.mkdir(exist_ok=True, parents=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(filepath))

    def scatter(self, data: np.ndarray, radius: float = 0.1, material: str = "rainbow", alpha: float = 1.0):
        match data.shape:
            case (n, 3):
                pass
            case shape:
                raise ValueError(f"Data has incorrect shape: {shape}")

        mesh = bpy.data.meshes.new(f"mesh")
        obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.scene.collection.objects.link(obj)

        mesh.from_pydata(data.tolist(), (), ())

        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=radius,
        )
        # TODO: improve getting icosphere
        icosphere = bpy.data.objects.get("Icosphere")
        bpy.ops.object.shade_smooth()
        icosphere.hide_set(True)
        icosphere.hide_render = True

        node_group = bpy.data.node_groups.new("GeometryNodes", "GeometryNodeTree")

        in_node = node_group.nodes.new("NodeGroupInput")
        in_node.location = (0, 0)

        out_node = node_group.nodes.new("NodeGroupOutput")
        out_node.location = (600, 0)

        points_node = node_group.nodes.new("GeometryNodeInstanceOnPoints")
        points_node.location = (200, 0)

        object_info = node_group.nodes.new("GeometryNodeObjectInfo")
        object_info.location = (0, -200)
        object_info.inputs[0].default_value = icosphere

        realize = node_group.nodes.new("GeometryNodeRealizeInstances")
        realize.location = (400, 0)

        node_group.links.new(in_node.outputs[0], points_node.inputs["Points"])

        node_group.links.new(object_info.outputs["Geometry"], points_node.inputs["Instance"])
        node_group.links.new(object_info.outputs["Scale"], points_node.inputs["Scale"])

        node_group.links.new(points_node.outputs["Instances"], realize.inputs["Geometry"])

        node_group.links.new(realize.outputs["Geometry"], out_node.inputs[0])

        modifier = obj.modifiers.new("GeometryNodes", "NODES")
        modifier.node_group = node_group

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="GeometryNodes")

        material = bp.utils.load_material(material)
        obj.material_slots[0].material = material

        # Set transparency
        material.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = alpha
