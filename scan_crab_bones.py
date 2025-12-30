import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"C:\Users\logan\Documents\Megaman_Clean_Repo\_body\headcrab_scaled.glb")
armature = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
print("--- BONE HIERARCHY ---")
if armature:
    for bone in armature.data.bones:
        print(f"Bone: {bone.name}")
else:
    print("No Armature found.")
