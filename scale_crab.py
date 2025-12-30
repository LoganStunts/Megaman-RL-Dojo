import bpy
import os

# Define paths
input_path = r"C:\Users\logan\Downloads\normal-headcrab\source\normal headcrab.glb"
output_path = r"C:\Users\logan\Downloads\normal-headcrab\source\normal headcrab_scaled.glb"

# 1. Clear the scenepy.ops.wm.read_factory_settings(use_empty=True)

# 2. Import the modelpy.ops.import_scene.gltf(filepath=input_path)

# 3. Select all and scalepy.ops.object.select_all(action='SELECT')py.ops.transform.resize(value=(0.01, 0.01, 0.01))

# 4. Apply Scale (The critical step to keep bones from exploding)py.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 5. Export back to GLBpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_apply=True)

print(f"Surgery Complete: {output_path}")
