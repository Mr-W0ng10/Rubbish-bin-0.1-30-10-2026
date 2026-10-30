import bpy, os
BASE = r"C:\Users\princ\OneDrive\桌面\Final Year Project\SmartBin_3D"
bpy.ops.export_scene.fbx(filepath=os.path.join(BASE, "smartbin.fbx"), use_selection=False, apply_scale_options='FBX_SCALE_ALL')
try:
    bpy.ops.wm.obj_export(filepath=os.path.join(BASE, "smartbin.obj"), export_selected_objects=False, export_materials=True)
except Exception as e:
    print("OBJ export failed:", e)
print("EXPORTED")
