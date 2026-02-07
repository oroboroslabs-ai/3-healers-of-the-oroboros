# Blender Python script to procedurally create 3 stylized android MDs and render a 2560x1440 banner
import bpy
import math
import os

# Output path inside container
output_dir = '/output'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'blender_banner.png')

# Clean default
bpy.ops.wm.read_factory_settings(use_empty=True)

# Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
# Prefer GPU if available; fallback to CPU
try:
    prefs = bpy.context.preferences
    cycles_prefs = prefs.addons['cycles'].preferences
    cycles_prefs.compute_device_type = 'CUDA'
    scene.cycles.device = 'GPU'
except Exception:
    scene.cycles.device = 'CPU'
scene.render.resolution_x = 2560
scene.render.resolution_y = 1440
scene.render.resolution_percentage = 100
# Higher sample count for high-quality render
scene.cycles.samples = 1024
scene.cycles.preview_samples = 128
scene.cycles.use_denoising = True
scene.render.filepath = output_file

# Camera
cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = (0.0, -6.5, 1.6)
cam.rotation_euler = (math.radians(75), 0, 0)

# Lights
light_data = bpy.data.lights.new(name='Key', type='AREA')
light_data.energy = 1200
light_data.size = 1.6
light = bpy.data.objects.new(name='Key', object_data=light_data)
light.location = (2.5, -4.0, 3.5)
scene.collection.objects.link(light)

rim_data = bpy.data.lights.new(name='Rim', type='AREA')
rim_data.energy = 300
rim = bpy.data.objects.new(name='Rim', object_data=rim_data)
rim.location = (-3.5, -2.0, 2.8)
scene.collection.objects.link(rim)

# Ground/backdrop plane
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 2.5, -1.2))
plane = bpy.context.active_object
mat_bg = bpy.data.materials.new('BG')
mat_bg.use_nodes = True
nodes = mat_bg.node_tree.nodes
links = mat_bg.node_tree.links
nodes.clear()
# simple dark gradient using emission shader
em = nodes.new(type='ShaderNodeEmission')
em.inputs['Color'].default_value = (0.04, 0.04, 0.06, 1)
output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(em.outputs[0], output.inputs[0])
plane.data.materials.append(mat_bg)

# Utility: create principled material
def make_material(name, base_color, metallic=0.5, roughness=0.35):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    # Principled setup with slight subsurface for a softer anime look
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    try:
        bsdf.inputs['Subsurface'].default_value = 0.08
        bsdf.inputs['Subsurface Radius'].default_value = (0.8, 0.5, 0.4)
    except Exception:
        # older/newer Blender may not expose these inputs by name; ignore if unavailable
        pass
    out = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

# Create stylized android MD at x position, color scheme
def make_android(x, color):
    # Use smoother, subdivided shapes for higher-quality anime look
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(x, 0, 0.0))
    body = bpy.context.active_object
    body.scale[2] = 0.9
    # Subdivision for smoothness
    sub = body.modifiers.new(name='Subdiv', type='SUBSURF')
    sub.levels = 3
    bpy.ops.object.shade_smooth()
    body_mat = make_material(f'BodyMat_{x}', color, metallic=0.15, roughness=0.25)
    body.data.materials.append(body_mat)

    # Head: smooth ping-pong styled (slightly glossy)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.36, location=(x, 0, 0.9))
    head = bpy.context.active_object
    head_mat = make_material(f'HeadMat_{x}', (1.0,1.0,1.0), metallic=0.0, roughness=0.08)
    head.data.materials.append(head_mat)
    head.modifiers.new(name='SubdivH', type='SUBSURF').levels = 2
    head.select_set(True)
    bpy.ops.object.shade_smooth()

    # Eyes: small flat discs with glossy dark material
    eye_mat = make_material('EyeMat', (0.02,0.02,0.02), metallic=0.0, roughness=0.02)
    for ex in (-0.08, 0.08):
        bpy.ops.mesh.primitive_circle_add(radius=0.045, fill_type='NGON', location=(x+ex, 0.29, 0.95))
        e = bpy.context.active_object
        e.rotation_euler = (math.radians(90), 0, 0)
        e.data.materials.append(eye_mat)

    # Small accessories: stethoscope (simple tubes)
    bpy.ops.mesh.primitive_torus_add(location=(x, -0.16, 0.75), major_radius=0.16, minor_radius=0.012, rotation=(math.radians(65),0,0))
    st = bpy.context.active_object
    st_mat = make_material('StethMat', (0.06,0.06,0.06), metallic=0.9, roughness=0.15)
    st.data.materials.append(st_mat)

    return (body, head)

    # Head (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(x, 0, 0.9))
    head = bpy.context.active_object
    head_mat = make_material(f'HeadMat_{x}', (1,1,1), metallic=0.05, roughness=0.35)
    head.data.materials.append(head_mat)

    # Visor (emissive)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(x, 0.18, 0.9))
    visor = bpy.context.active_object
    visor.scale[0] = 1.3
    visor_mat = bpy.data.materials.new('VisorMat')
    visor_mat.use_nodes = True
    nodes = visor_mat.node_tree.nodes
    links = visor_mat.node_tree.links
    nodes.clear()
    em = nodes.new(type='ShaderNodeEmission')
    em.inputs['Color'].default_value = (*color, 1.0)
    em.inputs['Strength'].default_value = 6.0
    out = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(em.outputs[0], out.inputs[0])
    visor.data.materials.append(visor_mat)

    # Simple neck connector
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.2, location=(x,0,0.55))
    neck = bpy.context.active_object
    neck.data.materials.append(body_mat)

    # Small shoulders
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(x-0.4, 0, 0.3))
    s1 = bpy.context.active_object; s1.data.materials.append(body_mat)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(x+0.4, 0, 0.3))
    s2 = bpy.context.active_object; s2.data.materials.append(body_mat)

    return (body, head, visor)

# Create three androids with distinct colors inside the safe area center
# Safe area centered horizontally at 1280 screen px; map to Blender camera view roughly centered at x positions -1.6..1.6
pos_x = [-1.6, 0.0, 1.6]
colors = [(0.06,0.73,0.51), (0.54,0.36,0.96), (0.23,0.51,0.94)]  # green, purple, blue
for px, col in zip(pos_x, colors):
    make_android(px, col)

# Oroboros ring on left inside safe area
bpy.ops.mesh.primitive_torus_add(location=(-3.0, -0.6, 0.3), major_radius=0.45, minor_radius=0.08, rotation=(math.radians(45), 0, 0))
ring = bpy.context.active_object
ring_mat = make_material('RingMat', (0.06,0.73,0.51), metallic=1.0, roughness=0.15)
ring.data.materials.append(ring_mat)
# mouth ball
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(-2.65, -0.25, 0.55))
mb = bpy.context.active_object
mb_mat = make_material('MouthMat', (0.06,0.73,0.51), metallic=0.8, roughness=0.1)
mb.data.materials.append(mb_mat)

# Composition: ensure all objects are visible to camera
for obj in bpy.context.scene.objects:
    obj.hide_render = False

# Render
bpy.ops.render.render(write_still=True)
print('Rendered to', output_file)
