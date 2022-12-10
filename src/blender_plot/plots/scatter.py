
import blender_plot as bp

import bpy
import numpy as np


def scatter(scene: bp.scenes.Scene, data: np.array, radius: float = 0.1, material: str = "rainbow", alpha: float = None):
    scene.activate()

    match data.shape:
        case (n, 3):
            pass
        case shape:
            raise ValueError(f"Data has incorrect shape: {shape}")

    # center the data
    data = (data - data.mean(axis=0)) / data.std(axis=0)

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
    node_group.use_fake_user = True

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

    blender_material = bp.utils.get_material(material).blender_material
    obj.material_slots[0].material = blender_material

    # Set transparency
    if alpha is not None:
        try:
            blender_material.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = alpha
        except AttributeError:
            raise RuntimeError(f"Material {material} does not support alpha.")
