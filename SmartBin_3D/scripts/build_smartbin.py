# -*- coding: utf-8 -*-
"""Build a low-cost 4-stream smart bin concept model in Blender 5.x.

Run in Blender (GUI or headless). Saves .blend and .glb, and sets up
cameras, lights and a simple 200-frame operation animation.
"""
import bpy, bmesh, math, os
from mathutils import Vector, Euler

try:
    BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
except NameError:
    BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
BLEND = os.path.join(BASE, "smartbin.blend")
GLB = os.path.join(BASE, "smartbin.glb")

# ---------------- clean ----------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for b in list(block):
        if b.users == 0:
            block.remove(b)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 1400
scene.render.resolution_y = 1400
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.fps = 20
scene.frame_start = 1
scene.frame_end = 220
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass

# ---------------- collections ----------------
def col(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
    return c

COL_BODY = col("GEO_Body")
COL_IN = col("GEO_Internals")
COL_BINS = col("GEO_Bins")
COL_MOTION = col("GEO_Motion")
COL_ELEC = col("GEO_Electronics")
COL_LABELS = col("GEO_Labels")
COL_LIGHT = col("LIGHTS")
COL_CAM = col("CAMERAS")
COL_STAGE = col("STAGE")


def move(obj, c):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    c.objects.link(obj)
    return obj


# ---------------- materials ----------------
def mat(name, color, rough=0.4, metallic=0.0, alpha=1.0, emission=None):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = 'BLENDED'
        except Exception:
            pass
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission[0], 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission[1]
    return m


M_BODY = mat("MAT-Body", (0.78, 0.80, 0.78), 0.38)
M_BODY_D = mat("MAT-BodyDark", (0.16, 0.20, 0.18), 0.45)
M_GREEN = mat("MAT-Green", (0.045, 0.18, 0.13), 0.38)
M_GREEN_L = mat("MAT-GreenLight", (0.30, 0.48, 0.30), 0.45)
M_BLUE = mat("MAT-Plastic", (0.18, 0.42, 0.64), 0.40)
M_YELLOW = mat("MAT-Metal", (0.82, 0.58, 0.12), 0.38)
M_WET = mat("MAT-Wet", (0.30, 0.52, 0.32), 0.46)
M_GREY = mat("MAT-Other", (0.52, 0.56, 0.58), 0.48)
M_METAL = mat("MAT-Steel", (0.55, 0.58, 0.60), 0.25, 0.85)
M_DARK = mat("MAT-Dark", (0.035, 0.04, 0.04), 0.55)
M_RUBBER = mat("MAT-Rubber", (0.02, 0.02, 0.02), 0.85)
M_ORANGE = mat("MAT-Orange", (0.85, 0.28, 0.06), 0.35)
M_PCB = mat("MAT-PCB", (0.03, 0.22, 0.10), 0.5)
M_WHITE = mat("MAT-White", (0.92, 0.92, 0.88), 0.35)
M_GLASS = mat("MAT-Smoke", (0.03, 0.06, 0.055), 0.08, 0.0, 0.30)
M_LED = mat("MAT-LED", (0.9, 0.95, 0.85), 0.2, 0.0, 1.0, emission=((0.75, 1.0, 0.75), 5.0))
M_BIN_LABEL = mat("MAT-BinLabel", (0.95, 0.95, 0.92), 0.3)
M_FLOOR = mat("MAT-Floor", (0.72, 0.74, 0.72), 0.7)

# ---------------- helpers ----------------
def add_cube(name, size, loc, material, bevel=0.004, rot=(0, 0, 0), c=COL_BODY):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = size
    obj.rotation_euler = Euler(rot)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        md = obj.modifiers.new("Bevel", "BEVEL")
        md.width = bevel
        md.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=md.name)
    obj.data.materials.append(material)
    move(obj, c)
    return obj


def add_cyl(name, r, depth, loc, material, rot=(0, 0, 0), vertices=32, bevel=0.0015, c=COL_MOTION):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=depth, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    if bevel:
        md = obj.modifiers.new("Bevel", "BEVEL")
        md.width = bevel
        md.segments = 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=md.name)
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.data.materials.append(material)
    move(obj, c)
    return obj


def add_torus(name, major, minor, loc, material, rot=(0, 0, 0), c=COL_MOTION):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=48, minor_segments=10,
                                     location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.data.materials.append(material)
    move(obj, c)
    return obj


def add_curve(name, pts, radius, material, c=COL_MOTION):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = 16
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (p[0], p[1], p[2], 1.0)
    obj = bpy.data.objects.new(name, cu)
    c.objects.link(obj)
    obj.data.materials.append(material)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj = bpy.context.active_object
    obj.name = name
    return obj


def add_text(name, body, size, loc, rot, material=M_BIN_LABEL, c=COL_LABELS):
    cu = bpy.data.curves.new(name, 'FONT')
    cu.body = body
    cu.size = size
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.extrude = 0.0008
    obj = bpy.data.objects.new(name, cu)
    c.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = Euler(rot)
    obj.data.materials.append(material)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj = bpy.context.active_object
    obj.name = name
    return obj


def empty(name, loc, c=COL_MOTION):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = 'PLAIN_AXES'
    e.empty_display_size = 0.03
    e.location = loc
    c.objects.link(e)
    return e


def parent_keep(obj, piv):
    # make sure piv.matrix_world is current before computing the inverse
    bpy.context.view_layer.update()
    obj.parent = piv
    obj.matrix_parent_inverse = piv.matrix_world.inverted()
    return obj

# ---------------- stage ----------------
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "STAGE-Floor"
floor.data.materials.append(M_FLOOR)
move(floor, COL_STAGE)

# world
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs[0].default_value = (0.78, 0.81, 0.78, 1)
bg.inputs[1].default_value = 0.45

# ---------------- main shell ----------------
W, D, H = 0.42, 0.42, 0.78
# feet
for sx in (-0.17, 0.17):
    for sy in (-0.17, 0.17):
        add_cyl(f"GEO-Foot-{sx}-{sy}", 0.018, 0.02, (sx, sy, 0.01), M_RUBBER, vertices=20, c=COL_BODY)
# base / plinth
add_cube("GEO-Base", (W, D, 0.09), (0, 0, 0.065), M_BODY_D, 0.008)
add_cube("GEO-BasePlate", (W - 0.03, D - 0.03, 0.006), (0, 0, 0.020), M_BODY_D, 0.002)
# side walls
add_cube("GEO-Side-L", (0.012, D, 0.68), (-0.204, 0, 0.44), M_BODY, 0.006)
add_cube("GEO-Side-R", (0.012, D, 0.68), (0.204, 0, 0.44), M_BODY, 0.006)
# back
add_cube("GEO-Back", (W, 0.012, 0.68), (0, 0.204, 0.44), M_BODY, 0.006)
# bottom / top rails
add_cube("GEO-BottomRail", (W, D, 0.012), (0, 0, 0.10), M_BODY_D, 0.004)
add_cube("GEO-TopRail", (W, D, 0.012), (0, 0, 0.735), M_BODY_D, 0.004)
# front lower strips around window (drawer front)
add_cube("GEO-FrontBottom", (W, 0.012, 0.035), (0, -0.204, 0.115), M_BODY, 0.004)
add_cube("GEO-FrontTop", (W, 0.012, 0.38), (0, -0.204, 0.555), M_BODY, 0.004)
add_cube("GEO-FrontLeft", (0.025, 0.012, 0.285), (-0.1975, -0.204, 0.27), M_BODY, 0.004)
add_cube("GEO-FrontRight", (0.025, 0.012, 0.285), (0.1975, -0.204, 0.27), M_BODY, 0.004)
add_cube("GEO-Window", (0.36, 0.003, 0.285), (0, -0.201, 0.27), M_GLASS, 0.002)
# handle
add_cube("GEO-DrawerHandle", (0.14, 0.018, 0.018), (0, -0.218, 0.155), M_BODY_D, 0.005)
add_cube("GEO-DrawerHandle2", (0.12, 0.012, 0.012), (0, -0.228, 0.155), M_METAL, 0.003)

# mid frame with central opening (4 strips)
add_cube("GEO-MidFrame-F", (W, 0.07, 0.025), (0, -0.175, 0.485), M_BODY_D, 0.004)
add_cube("GEO-MidFrame-B", (W, 0.07, 0.025), (0, 0.175, 0.485), M_BODY_D, 0.004)
add_cube("GEO-MidFrame-L", (0.07, 0.28, 0.025), (-0.175, 0, 0.485), M_BODY_D, 0.004)
add_cube("GEO-MidFrame-R", (0.07, 0.28, 0.025), (0.175, 0, 0.485), M_BODY_D, 0.004)

# top chamber walls (above mid frame)
add_cube("GEO-TopWall-L", (0.012, 0.40, 0.22), (-0.198, 0, 0.615), M_BODY, 0.004)
add_cube("GEO-TopWall-R", (0.012, 0.40, 0.22), (0.198, 0, 0.615), M_BODY, 0.004)
add_cube("GEO-TopWall-B", (0.40, 0.012, 0.22), (0, 0.198, 0.615), M_BODY, 0.004)
# front top window frame
add_cube("GEO-TopFront-B", (0.40, 0.012, 0.06), (0, -0.198, 0.545), M_BODY, 0.004)
add_cube("GEO-TopFront-T", (0.40, 0.012, 0.06), (0, -0.198, 0.705), M_BODY, 0.004)
add_cube("GEO-TopFront-L", (0.08, 0.012, 0.10), (-0.16, -0.198, 0.625), M_BODY, 0.004)
add_cube("GEO-TopFront-R", (0.08, 0.012, 0.10), (0.16, -0.198, 0.625), M_BODY, 0.004)
add_cube("GEO-TopWindow", (0.24, 0.003, 0.10), (0, -0.196, 0.625), M_GLASS, 0.002)
# 120 mm riser collar: gives clearance for an upright 500 mL bottle
add_cube("GEO-Collar-L", (0.012, 0.40, 0.12), (-0.198, 0, 0.785), M_GREEN, 0.004)
add_cube("GEO-Collar-R", (0.012, 0.40, 0.12), (0.198, 0, 0.785), M_GREEN, 0.004)
add_cube("GEO-Collar-B", (0.40, 0.012, 0.12), (0, 0.198, 0.785), M_GREEN, 0.004)
add_cube("GEO-Collar-F", (0.40, 0.012, 0.12), (0, -0.198, 0.785), M_GREEN, 0.004)

# top logo / LED strip
add_text("GEO-Logo", "SMART SORT", 0.030, (0, -0.211, 0.722), (math.pi / 2, 0, 0), M_WHITE)
add_cube("GEO-LEDStrip", (0.16, 0.004, 0.006), (0, -0.212, 0.700), M_LED, 0.002)
for i, (x, mm) in enumerate(zip((-0.12, -0.04, 0.04, 0.12), (M_BLUE, M_YELLOW, M_WET, M_GREY))):
    add_cube(f"GEO-Chip{i}", (0.045, 0.004, 0.012), (x, -0.211, 0.688), mm, 0.002)

# OLED status display on the front panel
add_cube("GEO-OLED-Bezel", (0.084, 0.006, 0.042), (0, -0.232, 0.648), M_DARK, 0.002)
add_cube("GEO-OLED", (0.070, 0.004, 0.030), (0, -0.236, 0.648), M_LED, 0.001)

# ---------------- bins ----------------
bin_defs = [
    ("PLASTIC", "BIN 1", -0.10, -0.10, M_BLUE),
    ("METAL", "BIN 2", 0.10, -0.10, M_YELLOW),
    ("WET", "BIN 3", -0.10, 0.10, M_WET),
    ("OTHER", "BIN 4", 0.10, 0.10, M_GREY),
]
for label, name, x, y, material in bin_defs:
    add_cube(f"GEO-{name}", (0.17, 0.17, 0.30), (x, y, 0.25), material, 0.007, c=COL_BINS)
    # dark recessed top to read as an open bin
    add_cube(f"GEO-{name}-Top", (0.135, 0.135, 0.008), (x, y, 0.396), M_DARK, 0.003, c=COL_BINS)
    add_text(f"GEO-{name}-Label", label, 0.014, (x, y - 0.086, 0.22), (math.pi / 2, 0, 0), M_BIN_LABEL)
    add_text(f"GEO-{name}-Num", str(bin_defs.index((label, name, x, y, material)) + 1), 0.012, (x, y, 0.405), (0, 0, 0), M_BIN_LABEL)
    # handle strip
    add_cube(f"GEO-{name}-Handle", (0.06, 0.006, 0.012), (x, y - 0.088, 0.15), M_DARK, 0.002, c=COL_BINS)

# vertical dividers
add_cube("GEO-Divider-X", (0.008, 0.36, 0.30), (0, 0, 0.25), M_BODY_D, 0.002)
add_cube("GEO-Divider-Y", (0.36, 0.008, 0.30), (0, 0, 0.25), M_BODY_D, 0.002)

# ---------------- funnel & spout ----------------
# square funnel as four quads + solidify
def make_funnel():
    top = [(-0.11, -0.10, 0.55), (0.11, -0.10, 0.55), (0.11, 0.10, 0.55), (-0.11, 0.10, 0.55)]
    bottom = [(-0.0375, -0.0375, 0.462), (0.0375, -0.0375, 0.462), (0.0375, 0.0375, 0.462), (-0.0375, 0.0375, 0.462)]
    mesh = bpy.data.meshes.new("GEO-FunnelMesh")
    bm = bmesh.new()
    vt = [bm.verts.new(p) for p in top]
    vb = [bm.verts.new(p) for p in bottom]
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vt[i], vt[j], vb[j], vb[i]))
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("GEO-Funnel", mesh)
    COL_IN.objects.link(obj)
    obj.data.materials.append(M_BODY)
    md = obj.modifiers.new("Solidify", "SOLIDIFY")
    md.thickness = 0.003
    md.offset = 0
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=md.name)
    return obj

make_funnel()
# bearing ring
add_torus("GEO-Bearing", 0.055, 0.006, (0, 0, 0.456), M_METAL, c=COL_MOTION)
# spout pivot and elbow
PIV_SPOUT = empty("PIV-Spout", (0, 0, 0.456))
spout = add_curve("GEO-Spout", [(0, 0, 0.456), (0, 0, 0.438), (0.045, 0, 0.428), (0.100, 0, 0.408)], 0.036, M_ORANGE)
parent_keep(spout, PIV_SPOUT)
# collar
collar = add_cyl("GEO-SpoutCollar", 0.050, 0.020, (0, 0, 0.456), M_GREEN_L, c=COL_MOTION)
# NEMA 17 + A4988 + 3:1 GT2 belt (reliable torque, still under budget)
add_cube("GEO-Stepper", (0.043, 0.043, 0.040), (0.150, 0.140, 0.478), M_DARK, 0.003, c=COL_MOTION)
add_cyl("GEO-StepperShaft", 0.005, 0.055, (0.150, 0.140, 0.505), M_METAL, c=COL_MOTION)
add_cube("GEO-StepperMount", (0.060, 0.060, 0.006), (0.150, 0.140, 0.455), M_BODY_D, 0.002, c=COL_MOTION)
add_torus("GEO-MotorPulley", 0.018, 0.004, (0.150, 0.140, 0.490), M_METAL, c=COL_MOTION)
add_torus("GEO-SpoutPulley", 0.052, 0.004, (0, 0, 0.470), M_METAL, c=COL_MOTION)
# belt: a simple belt loop between the two pulleys
belt = add_curve("GEO-Belt", [(0.150, 0.140, 0.490), (0.100, 0.100, 0.490), (0.050, 0.050, 0.490), (0.0, 0.0, 0.490)], 0.002, M_RUBBER)
# home switch
add_cube("GEO-HomeSwitch", (0.03, 0.025, 0.018), (0.12, 0.0, 0.50), M_DARK, 0.003, c=COL_MOTION)
add_cube("GEO-HomeLever", (0.035, 0.008, 0.004), (0.10, 0.0, 0.505), M_METAL, 0.001, c=COL_MOTION)

# ---------------- fixed weigh platform + bottom trapdoor ----------------
# The platform is fixed to the load cell. Only the small trapdoor moves, so the
# load cell never carries the servo/hinge side-load while measuring.
add_cube("GEO-WeighPlatform-L", (0.020, 0.180, 0.008), (-0.100, 0.0, 0.635), M_BODY, 0.003, c=COL_IN)
add_cube("GEO-WeighPlatform-R", (0.020, 0.180, 0.008), (0.100, 0.0, 0.635), M_BODY, 0.003, c=COL_IN)
add_cube("GEO-WeighPlatform-F", (0.220, 0.020, 0.008), (0.0, -0.080, 0.635), M_BODY, 0.003, c=COL_IN)
add_cube("GEO-WeighPlatform-B", (0.220, 0.020, 0.008), (0.0, 0.080, 0.635), M_BODY, 0.003, c=COL_IN)
# trapdoor, hinged at the back
PIV_DOOR = empty("PIV-Door", (0, 0.070, 0.632))
door = add_cube("GEO-TrapDoor", (0.176, 0.136, 0.006), (0, 0.0, 0.632), M_BODY, 0.003, c=COL_IN)
parent_keep(door, PIV_DOOR)
pad = add_cube("GEO-MoisturePad", (0.120, 0.080, 0.002), (0, -0.015, 0.637), M_BLUE, 0.001, c=COL_IN)
parent_keep(pad, PIV_DOOR)
# single 5 kg load cell under the fixed platform
add_cube("GEO-LoadCell", (0.050, 0.030, 0.012), (0, 0.0, 0.612), M_METAL, 0.002, c=COL_IN)
add_cube("GEO-LoadCellBase", (0.070, 0.050, 0.010), (0, 0.0, 0.602), M_BODY_D, 0.002, c=COL_IN)
# fixed metal-detector coil under the platform (not on the load cell)
add_torus("GEO-MetalCoil", 0.080, 0.004, (0, 0.0, 0.598), M_ORANGE, c=COL_IN)
# MG996R servo at the side, spring-assisted door
add_cube("GEO-TrayServo", (0.045, 0.025, 0.040), (0.145, -0.100, 0.620), M_BLUE, 0.003, c=COL_MOTION)
add_cyl("GEO-TrayServoHorn", 0.012, 0.006, (0.125, -0.100, 0.635), M_WHITE, c=COL_MOTION)
add_cube("GEO-TrayLink", (0.055, 0.006, 0.006), (0.100, -0.100, 0.640), M_METAL, 0.001, c=COL_MOTION)
add_cyl("GEO-DoorSpring", 0.004, 0.030, (0.070, 0.060, 0.635), M_METAL, rot=(0, math.pi/2, 0), c=COL_MOTION)
# IR safety beam across the mouth
add_cube("GEO-IRBeam-L", (0.012, 0.012, 0.012), (-0.130, -0.150, 0.700), M_DARK, 0.002, c=COL_MOTION)
add_cube("GEO-IRBeam-R", (0.012, 0.012, 0.012), (0.130, -0.150, 0.700), M_DARK, 0.002, c=COL_MOTION)
add_cyl("GEO-IRBeam", 0.0015, 0.260, (0, -0.150, 0.700), M_LED, rot=(0, math.pi/2, 0), c=COL_MOTION)
# thin scanning light line across the tray (visual feedback during capture)
scan = add_cube("GEO-ScanLine", (0.200, 0.004, 0.002), (0, -0.02, 0.665), M_LED, 0.001, c=COL_MOTION)
scan.scale = (0, 0, 0)
scan.keyframe_insert(data_path="scale", frame=1)
scan.location = (-0.100, -0.02, 0.665)
scan.keyframe_insert(data_path="location", frame=1)
scan.scale = (0, 0, 0)
scan.keyframe_insert(data_path="scale", frame=77)
scan.scale = (1, 1, 1)
scan.keyframe_insert(data_path="scale", frame=80)
scan.location = (-0.100, -0.02, 0.665)
scan.keyframe_insert(data_path="location", frame=82)
scan.location = (0.100, -0.02, 0.665)
scan.keyframe_insert(data_path="location", frame=100)
scan.scale = (0, 0, 0)
scan.keyframe_insert(data_path="scale", frame=106)
# four bin-full IR sensors under the mid-frame
for i, (x, y) in enumerate(((-0.10, -0.10), (0.10, -0.10), (-0.10, 0.10), (0.10, 0.10))):
    add_cube(f"GEO-BinIR{i}", (0.022, 0.018, 0.016), (x, y, 0.445), M_DARK, 0.002, c=COL_MOTION)

# ---------------- camera / lid ----------------
PIV_LID = empty("PIV-Lid", (0, 0.20, 0.865))
lid = add_cube("GEO-Lid", (0.42, 0.42, 0.040), (0, 0, 0.880), M_GREEN, 0.010, c=COL_BODY)
parent_keep(lid, PIV_LID)
# lid handle
handle = add_cube("GEO-LidHandle", (0.13, 0.025, 0.016), (0, -0.185, 0.905), M_BODY_D, 0.004, c=COL_BODY)
parent_keep(handle, PIV_LID)
# camera pod
pod = add_cube("GEO-CameraPod", (0.12, 0.10, 0.035), (0, -0.02, 0.902), M_BODY_D, 0.006, c=COL_BODY)
# ESP32-S3-CAM antenna + microSD slot
add_cube("GEO-Antenna", (0.035, 0.008, 0.004), (0.045, -0.02, 0.922), M_PCB, 0.001, c=COL_BODY)
add_cube("GEO-SD", (0.018, 0.002, 0.010), (0.064, -0.02, 0.902), M_METAL, 0.001, c=COL_BODY)
parent_keep(pod, PIV_LID)
lens = add_cyl("GEO-CameraLens", 0.025, 0.020, (0, -0.02, 0.882), M_DARK, c=COL_BODY)
parent_keep(lens, PIV_LID)
ring = add_torus("GEO-LEDRing", 0.040, 0.006, (0, -0.02, 0.878), M_LED, c=COL_BODY)
parent_keep(ring, PIV_LID)
# hinge cylinders
for x in (-0.15, 0.15):
    add_cyl(f"GEO-Hinge{x}", 0.012, 0.06, (x, 0.202, 0.865), M_METAL, rot=(0, math.pi / 2, 0), c=COL_BODY)
# lid reed switch
add_cube("GEO-LidReed", (0.025, 0.015, 0.010), (0.16, -0.19, 0.858), M_METAL, 0.002, c=COL_BODY)

# ---------------- electronics ----------------
add_cube("GEO-PCB", (0.18, 0.12, 0.008), (0, -0.02, 0.055), M_PCB, 0.002, c=COL_ELEC)
add_cube("GEO-ESP32", (0.055, 0.028, 0.012), (-0.04, -0.02, 0.065), M_DARK, 0.002, c=COL_ELEC)
add_cube("GEO-HX711", (0.035, 0.022, 0.008), (0.04, -0.02, 0.063), M_WHITE, 0.002, c=COL_ELEC)
add_cube("GEO-A4988", (0.035, 0.025, 0.008), (0.04, -0.06, 0.063), M_PCB, 0.002, c=COL_ELEC)
add_cube("GEO-USB", (0.012, 0.010, 0.006), (-0.04, -0.065, 0.063), M_METAL, 0.001, c=COL_ELEC)
# a few wires
for i, x in enumerate((-0.06, -0.02, 0.02)):
    add_curve(f"GEO-Wire{i}", [(x, -0.02, 0.065), (x, 0.02, 0.09), (x, 0.06, 0.14)], 0.0015, M_ORANGE if i == 0 else M_DARK, c=COL_ELEC)
# vent slots on side
for i in range(5):
    add_cube(f"GEO-Vent{i}", (0.002, 0.12, 0.006), (-0.211, 0.05, 0.05 + i * 0.012), M_DARK, 0.001, c=COL_BODY)

# ---------------- item ----------------
# small bottle: body + neck + cap
item_body = add_cyl("GEO-Item", 0.028, 0.105, (0, -0.02, 0.690), M_BLUE, c=COL_MOTION)
item_neck = add_cyl("GEO-ItemNeck", 0.012, 0.030, (0, -0.02, 0.758), M_BLUE, c=COL_MOTION)
item_cap = add_cyl("GEO-ItemCap", 0.014, 0.012, (0, -0.02, 0.779), M_WHITE, c=COL_MOTION)
# group item under empty for easy animation
item_piv = empty("PIV-Item", (0, -0.02, 0.690))
for o in (item_body, item_neck, item_cap):
    parent_keep(o, item_piv)
item_piv.location = (0, -0.02, 0.690)

# ---------------- frame corner posts ----------------
for x in (-0.195, 0.195):
    for y in (-0.195, 0.195):
        add_cube(f"GEO-Post{x}{y}", (0.012, 0.012, 0.76), (x, y, 0.48), M_BODY_D, 0.002)

# ---------------- cameras / lights ----------------
def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def add_camera(name, loc, target, lens=55, ortho=None):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    if ortho:
        cam_data.type = 'ORTHO'
        cam_data.ortho_scale = ortho
    cam = bpy.data.objects.new(name, cam_data)
    COL_CAM.objects.link(cam)
    cam.location = loc
    look_at(cam, target)
    return cam


CAM_HERO = add_camera("CAM-Hero", (1.10, -1.30, 0.95), (0, 0, 0.38), 58)
CAM_CUT = add_camera("CAM-Cutaway", (0.95, -1.15, 0.95), (0, 0, 0.38), 62)
CAM_TOP = add_camera("CAM-Top", (0, 0, 1.65), (0, 0, 0.38), 50, ortho=0.52)
CAM_CAD = add_camera("CAM-CAD", (1.05, -1.05, 0.92), (0, 0, 0.38), 50, ortho=0.86)
scene.camera = CAM_HERO


def add_area(name, loc, energy, size, color=(1, 1, 1)):
    ld = bpy.data.lights.new(name, 'AREA')
    ld.energy = energy
    ld.shape = 'DISK'
    ld.size = size
    ld.color = color
    obj = bpy.data.objects.new(name, ld)
    COL_LIGHT.objects.link(obj)
    obj.location = loc
    look_at(obj, (0, 0, 0.35))
    return obj

add_area("LGT-Key", (1.5, -2.0, 2.0), 280, 1.8, (1.0, 0.96, 0.9))
add_area("LGT-Fill", (-2.0, -1.0, 1.2), 110, 1.5, (0.85, 0.92, 1.0))
add_area("LGT-Rim", (0.8, 2.0, 1.8), 220, 1.3, (0.9, 1.0, 0.9))
# top softbox
add_area("LGT-Top", (0, 0, 2.4), 160, 1.2, (1, 1, 1))

# ---------------- animation ----------------
# Lid starts open: the video begins with the item being thrown in.
PIV_LID.rotation_mode = 'XYZ'
for f, a in ((1, -math.radians(78)), (45, -math.radians(78)), (70, 0), (220, 0)):
    PIV_LID.rotation_euler.x = a
    PIV_LID.keyframe_insert(data_path="rotation_euler", index=0, frame=f)

# Trapdoor: opens 140-160, spring returns 180
PIV_DOOR.rotation_mode = 'XYZ'
for f, a in ((1, 0), (138, 0), (160, math.radians(75)), (180, math.radians(75)), (196, 0), (220, 0)):
    PIV_DOOR.rotation_euler.x = a
    PIV_DOOR.keyframe_insert(data_path="rotation_euler", index=0, frame=f)

# Spout: home 45 deg, rotate to -45 (metal front-right) at 100-120, hold, home 175
PIV_SPOUT.rotation_mode = 'XYZ'
for f, a in ((1, math.radians(45)), (105, math.radians(45)), (130, math.radians(-45)), (170, math.radians(-45)), (195, math.radians(45)), (220, math.radians(45))):
    PIV_SPOUT.rotation_euler.z = a
    PIV_SPOUT.keyframe_insert(data_path="rotation_euler", index=2, frame=f)

# Item: appear above tray, drop to tray, wait, fall through spout, rest in bin 2
item_piv.scale = (0, 0, 0)
for f, loc, s in (
    (1, (0, -0.02, 1.05), (1, 1, 1)),
    (18, (0, -0.02, 0.98), (1, 1, 1)),
    (32, (0, -0.02, 0.66), (1, 1, 1)),
    (148, (0, -0.02, 0.66), (1, 1, 1)),
    (162, (0, -0.07, 0.54), (1, 1, 1)),
    (174, (0.075, -0.075, 0.34), (1, 1, 1)),
    (220, (0.075, -0.075, 0.34), (1, 1, 1)),
):
    item_piv.location = loc
    item_piv.scale = s
    item_piv.keyframe_insert(data_path="location", frame=f)
    item_piv.keyframe_insert(data_path="scale", frame=f)

# LED ring pulse (object color via material is harder; use scale pulse)
for f, s in ((1, 1.0), (78, 1.0), (86, 1.18), (94, 1.0), (220, 1.0)):
    ring.scale = (s, s, s)
    ring.keyframe_insert(data_path="scale", frame=f)

# set interpolation: Blender 5.2 uses layered actions; leave default Bezier.
# (Item motion is short and slow enough that default interpolation is acceptable.)

# subtle camera push-in for a more elegant video
CAM_CUT.location = (0.98, -1.22, 0.98)
CAM_CUT.keyframe_insert(data_path="location", frame=1)
CAM_CUT.location = (0.90, -1.14, 0.94)
CAM_CUT.keyframe_insert(data_path="location", frame=220)

# ---------------- metadata / save ----------------
scene["design"] = "Low-cost 4-stream smart bin, 420 x 420 x 900 mm, target BOM <= HK$1000"
scene["units"] = "meters; 1 BU = 1 m"
scene["author"] = "DSH concept model"
scene.camera = CAM_HERO
bpy.ops.wm.save_as_mainfile(filepath=BLEND)

# export GLB (visible objects; include cameras/lights is optional)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=GLB, export_format='GLB', use_selection=False)
print("SAVED", BLEND, GLB)
print("OBJECTS", len(bpy.data.objects))

