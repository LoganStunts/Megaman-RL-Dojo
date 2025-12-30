import bpy
import os

# Use full escaped paths
input_path = r"C:\Users\logan\Downloads\normal-headcrab\source\normal headcrab.glb"
output_path = r"C:\Users\logan\Documents\Megaman_Clean_Repo\_body\headcrab_scaled.glb"

# Ensure target directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 1. Clear the scenepy.ops.wm.read_factory_settings(use_empty=True)

# 2. Import the modelpy.ops.import_scene.gltf(filepath=input_path)

# 3. Select all and scalepy.ops.object.select_all(action='SELECT')py.ops.transform.resize(value=(0.01, 0.01, 0.01))

# 4. Apply All Transforms (This also recalculates animations)py.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 5. Export back to GLBpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')

print(f"--- SUCCESS ---")
print(f"File saved to: {output_path}")
print("Animations:")
for action in bpy.data.actions:
    print(f" - {action.name}")
