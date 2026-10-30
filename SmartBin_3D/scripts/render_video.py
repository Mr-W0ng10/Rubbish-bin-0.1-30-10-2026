# -*- coding: utf-8 -*-
"""Render the 200-frame (24 fps, ~8.3 s) operation animation as PNG frames."""
import bpy, os

BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
OUT = os.path.join(BASE, "video", "frames")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene

def o(n):
    return bpy.data.objects.get(n)

def hide(names):
    for n in names:
        x = o(n)
        if x:
            x.hide_render = True

# cutaway set
hide(["GEO-FrontBottom", "GEO-FrontTop", "GEO-FrontLeft", "GEO-FrontRight",
      "GEO-Window", "GEO-DrawerHandle", "GEO-DrawerHandle2",
      "GEO-Side-R", "GEO-TopWall-R", "GEO-TopFront-B", "GEO-TopFront-T",
      "GEO-TopFront-L", "GEO-TopFront-R", "GEO-TopWindow", "GEO-TopRail",
      "GEO-MidFrame-F", "GEO-Base", "GEO-Logo", "GEO-LEDStrip",
      "GEO-Collar-F", "GEO-Collar-R"])

scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 220
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.filepath = os.path.join(OUT, "f_")
scene.render.use_overwrite = False
scene.render.use_placeholder = True
scene.camera = bpy.data.objects["CAM-Cutaway"]
scene.render.engine = 'BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples = 32
except Exception:
    pass
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
bpy.ops.render.render(animation=True)
print("DONE_FRAMES", OUT)
