
import blender_plot as bp

import bpy
import numpy as np


def scatter(scene: bp.scenes.Scene, data: np.array, radius: float = 0.1, material: str = "rainbow", hue: float | np.ndarray = None, alpha: float | np.ndarray = None):
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

    # Setup material
    material = bp.utils.get_material(material)
    material.apply_to(obj, hue, alpha)
    material.blender_material.use_backface_culling = True
    material.blender_material.blend_method = "BLEND"

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

    material_node = node_group.nodes.new("GeometryNodeSetMaterial")
    material_node.location = (400, 0)
    material_node.inputs[2].default_value = material.blender_material

    # realize = node_group.nodes.new("GeometryNodeRealizeInstances")
    # realize.location = (400, 200)
    # material_node = realize

    node_group.links.new(in_node.outputs[0], points_node.inputs["Points"])
    node_group.links.new(object_info.outputs["Geometry"], points_node.inputs["Instance"])
    node_group.links.new(object_info.outputs["Scale"], points_node.inputs["Scale"])
    node_group.links.new(points_node.outputs["Instances"], material_node.inputs["Geometry"])
    node_group.links.new(material_node.outputs["Geometry"], out_node.inputs[0])

    modifier = obj.modifiers.new("GeometryNodes", "NODES")
    modifier.node_group = node_group

    bpy.context.view_layer.objects.active = obj

    # Set material shading in 3D viewport
    area = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D'][0]
    area.spaces.active.shading.type = 'MATERIAL'
