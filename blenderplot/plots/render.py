
import blenderplot as bp

import bpy
import bmesh
import numpy as np
import pathlib

from IPython import display


Path = str | pathlib.Path


def make_node_group():
    """
    Create a new empty node group that can be used in a GeometryNodes modifier
    """
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=0.05,
    )
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

    return node_group


class RenderPlot:
    def __init__(self):
        self.scene = bpy.context.scene

    def scatter(self, points: np.ndarray, size: float = 1.0, material=None):
        mesh = bpy.data.meshes.new(f"mesh")
        obj = bpy.data.objects.new(mesh.name, mesh)
        self.scene.collection.objects.link(obj)

        bm = bmesh.new()

        # TODO: no loop?
        for i, point in enumerate(points):
            bm.verts.new(point.tolist())

        bm.to_mesh(mesh)
        bm.free()

        node_group = make_node_group()

        modifier = obj.modifiers.new("GeometryNodes", "NODES")
        modifier.node_group = node_group

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="GeometryNodes")

        if material is not None:
            obj.data.materials.append(material)

    def render(self, filepath: Path = "render.png", resolution=(800, 600), device="gpu", samples=16):
        """
        Render the current scene to an image
        Parameters
        ----------
        path: pathlib.Path to the file
        resolution: tuple of image (width, height)
        device: gpu or cpu
        samples: number of render samples to use. higher values improve quality, at the cost of computation time
        """
        filepath = bp.base_path / filepath

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

    def save(self, filepath: Path = "plot.blend"):
        filepath = bp.base_path / filepath
        bpy.ops.wm.save_as_mainfile(filepath=str(filepath))
