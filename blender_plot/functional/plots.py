
import bpy
import numpy as np
import bmesh

from .utils import load_material


def scatter(data: np.ndarray, radius: float = 0.1, material: str = "rainbow"):
    mesh = bpy.data.meshes.new(f"mesh")
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    # mesh.from_pydata(data.tolist(), (), ())

    bm = bmesh.new()

    # TODO: no loop?
    for i, point in enumerate(data):
        bm.verts.new(point.tolist())

    bm.to_mesh(mesh)
    bm.free()

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

    # material = load_material(material)
    # obj.data.materials.append(material)
