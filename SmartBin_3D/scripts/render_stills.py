# -*- coding: utf-8 -*-
"""Render stills from smartbin.blend (tuned lighting, cutaway sets)."""
import bpy, os
from mathutils import Vector

BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
OUT = os.path.join(BASE, "renders")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene

def obj(name):
    return bpy.data.objects.get(name)

def hide(names, state=True):
    for n in names:
        o = obj(n)
        if o:
            o.hide_render = state

def set_base(matname, rgba):
    m = bpy.data.materials.get(matname)
    if m and m.use_nodes:
        m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = rgba
        m.diffuse_color = rgba

# --- tone / palette tweaks -------------------------------------------------
set_base("MAT-Body", (0.58, 0.60, 0.58, 1))
set_base("MAT-BodyDark", (0.10, 0.13, 0.12, 1))
set_base("MAT-Floor", (0.48, 0.50, 0.48, 1))
scene.view_settings.exposure = -0.55
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
world = scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (0.55, 0.58, 0.55, 1)
    bg.inputs[1].default_value = 0.30
for name, energy in (("LGT-Key", 150), ("LGT-Fill", 55), ("LGT-Rim", 100), ("LGT-Top", 70)):
    o = obj(name)
    if o and o.data:
        o.data.energy = energy

# Workbench uses material.diffuse_color, not the shader node.
for m in bpy.data.materials:
    if m.use_nodes:
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs["Base Color"].default_value
            m.diffuse_color = (c[0], c[1], c[2], 1.0)

logo = obj("GEO-Logo")
if logo:
    logo.data.materials.clear()
    logo.data.materials.append(bpy.data.materials["MAT-Green"])

FRONT = ["GEO-FrontBottom", "GEO-FrontTop", "GEO-FrontLeft", "GEO-FrontRight",
         "GEO-Window", "GEO-DrawerHandle", "GEO-DrawerHandle2"]
LID = ["GEO-Lid", "GEO-LidHandle", "GEO-CameraPod", "GEO-CameraLens", "GEO-LEDRing",
       "GEO-LidReed"]
TOP = ["GEO-Lid", "GEO-LidHandle", "GEO-CameraPod", "GEO-CameraLens", "GEO-LEDRing",
       "GEO-TopFront-B", "GEO-TopFront-T", "GEO-TopFront-L", "GEO-TopFront-R",
       "GEO-TopWindow", "GEO-TopWall-L", "GEO-TopWall-R", "GEO-TopWall-B",
       "GEO-TopRail", "GEO-Logo", "GEO-LEDStrip", "GEO-Collar-L", "GEO-Collar-R", "GEO-Collar-F", "GEO-Collar-B"]
TRAY = ["GEO-WeighPlatform-L", "GEO-WeighPlatform-R", "GEO-WeighPlatform-F", "GEO-WeighPlatform-B",
        "GEO-TrapDoor", "GEO-MoisturePad", "GEO-LoadCell", "GEO-LoadCellBase",
        "GEO-MetalCoil", "GEO-Funnel", "GEO-TrayServo", "GEO-TrayServoHorn",
        "GEO-TrayLink", "GEO-DoorSpring"]
CUT = FRONT + LID + ["GEO-Side-R", "GEO-TopWall-R", "GEO-TopFront-B", "GEO-TopFront-T",
                     "GEO-TopFront-L", "GEO-TopFront-R", "GEO-TopWindow",
                     "GEO-MidFrame-F", "GEO-Logo", "GEO-LEDStrip", "GEO-Base", "GEO-TopRail",
               "GEO-Collar-F", "GEO-Collar-R"]
DETAIL_KEEP = ("GEO-WeighPlatform", "GEO-TrapDoor", "GEO-MoisturePad", "GEO-LoadCell",
               "GEO-MetalCoil", "GEO-Funnel", "GEO-Bearing", "GEO-Spout",
               "GEO-Stepper", "GEO-MotorPulley", "GEO-SpoutPulley", "GEO-Belt",
               "GEO-Home", "GEO-BIN", "GEO-Item", "GEO-MidFrame", "GEO-BasePlate",
               "GEO-PCB", "GEO-ESP32", "GEO-HX711", "GEO-A4988", "GEO-USB", "GEO-Wire",
               "GEO-DoorSpring", "GEO-TrayServo")

scene.render.resolution_x = 1600
scene.render.resolution_y = 1600
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.frame_set(1)
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 64
except Exception:
    pass


def reset_visible():
    for n in set(FRONT + LID + TOP + TRAY + ["GEO-Base"]):
        o = obj(n)
        if o:
            o.hide_render = False


def show_item():
    piv = obj("PIV-Item")
    if piv:
        piv.scale = (1, 1, 1)
        piv.location = (0, -0.02, 0.66)


def render(name, cam, hide_list=(), workbench=False, frame=1, item=False):
    scene.frame_set(frame)
    reset_visible()
    if item:
        show_item()
    hide(hide_list, True)
    scene.camera = bpy.data.objects[cam]
    scene.render.filepath = os.path.join(OUT, name)
    if workbench:
        scene.render.engine = 'BLENDER_WORKBENCH'
        sh = scene.display.shading
        sh.light = 'STUDIO'
        sh.color_type = 'MATERIAL'
        sh.show_shadows = True
        sh.show_cavity = True
        sh.cavity_type = 'BOTH'
        sh.show_object_outline = True
        sh.object_outline_color = (0.08, 0.08, 0.08)
        sh.background_type = 'VIEWPORT'
        sh.background_color = (0.92, 0.93, 0.91)
        try:
            sh.studio_light = 'paint.sl'
        except Exception:
            pass
    else:
        scene.render.engine = 'BLENDER_EEVEE'
        try:
            scene.eevee.taa_render_samples = 64
        except Exception:
            pass
    bpy.ops.render.render(write_still=True)
    print("RENDERED", scene.render.filepath)


# 1 hero exterior, lid closed
render("01_hero.png", "CAM-Hero", hide_list=(), workbench=False, frame=90)
# 2 cutaway interior, item on tray, lid hidden
render("02_cutaway.png", "CAM-Cutaway", hide_list=CUT, workbench=False, frame=30, item=True)
# 3 top internal: hide tray/funnel so the spout and four bins are visible
render("03_top_internal.png", "CAM-Top", hide_list=FRONT + TOP + TRAY, workbench=False, frame=1)
# 4 CAD-style orthographic, cutaway
render("04_cad_iso.png", "CAM-CAD", hide_list=CUT, workbench=True, frame=1)

# 5 detail: hide everything except the mechanism / bin / electronics
for o in bpy.data.objects:
    if o.type == 'MESH' and o.name.startswith("GEO-"):
        o.hide_render = not any(o.name.startswith(k) for k in DETAIL_KEEP)
scene.frame_set(30)
show_item()
cam_data = bpy.data.cameras.new("CAM-Detail2")
cam = bpy.data.objects.new("CAM-Detail2", cam_data)
scene.collection.objects.link(cam)
cam.location = (0.52, -0.72, 0.86)
target = Vector((0, 0, 0.57))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam_data.lens = 68
scene.camera = cam
scene.render.filepath = os.path.join(OUT, "05_detail.png")
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 64
except Exception:
    pass
bpy.ops.render.render(write_still=True)
print("RENDERED", scene.render.filepath)
print("DONE")


# 06 electronics bay detail: hide shell/bins, show MCU + driver + HX711
for o in bpy.data.objects:
    if o.type == 'MESH' and o.name.startswith("GEO-"):
        keep = any(o.name.startswith(k) for k in ("GEO-BasePlate", "GEO-PCB", "GEO-ESP32", "GEO-HX711", "GEO-A4988", "GEO-USB", "GEO-Wire", "GEO-Post"))
        o.hide_render = not keep
cam_data = bpy.data.cameras.new("CAM-Electronics")
cam = bpy.data.objects.new("CAM-Electronics", cam_data)
scene.collection.objects.link(cam)
cam.location = (0.48, -0.78, 0.42)
target = Vector((0, 0, 0.06))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
cam_data.lens = 70
scene.camera = cam
scene.frame_set(90)
scene.render.filepath = os.path.join(OUT, "08_electronics.png")
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 64
except Exception:
    pass
bpy.ops.render.render(write_still=True)
print("RENDERED", scene.render.filepath)
