import bpy
# Using absolute path with forward slashes to avoid any ambiguity
path = "C:/Users/logan/Downloads/normal-headcrab/source/normal headcrab_scaled.glb"
bpy.ops.import_scene.gltf(filepath=path)
print("--- ANIMATION LIST ---")
for action in bpy.data.actions:
    print(f"Action Found: {action.name}")
