# -*- coding: utf-8 -*-
"""Render a few animation frames for QC."""
import bpy, os

BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
OUT = os.path.join(BASE, "renders", "anim_preview")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene

def o(n):
    return bpy.data.objects.get(n)

def hide(names):
    for n in names:
        x = o(n)
        if x:
            x.hide_render = True

# cutaway set: front, right side, top rail/front, base hidden to show electronics
hide(["GEO-FrontBottom", "GEO-FrontTop", "GEO-FrontLeft", "GEO-FrontRight",
      "GEO-Window", "GEO-DrawerHandle", "GEO-DrawerHandle2",
      "GEO-Side-R", "GEO-TopWall-R", "GEO-TopFront-B", "GEO-TopFront-T",
      "GEO-TopFront-L", "GEO-TopFront-R", "GEO-TopWindow", "GEO-TopRail",
      "GEO-MidFrame-F", "GEO-Base", "GEO-Logo", "GEO-LEDStrip"])

scene.render.resolution_x = 800
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 32
except Exception:
    pass
scene.camera = bpy.data.objects["CAM-Cutaway"]
frames = [1, 30, 90, 120, 135, 155, 180]
paths = []
for f in frames:
    scene.frame_set(f)
    scene.render.filepath = os.path.join(OUT, f"f{f:03d}.png")
    bpy.ops.render.render(write_still=True)
    paths.append(scene.render.filepath)
    print("FRAME", f)

print("DONE")
