import bpy

# 1. Load factory settings
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Import original big crab
input_path = r"C:\Users\logan\Downloads\normal-headcrab\source\normal headcrab.glb"
bpy.ops.import_scene.gltf(filepath=input_path)

print("--- DEEP SCAN START ---")

# 3. Find the Armature
armature = None
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        armature = obj
        print(f"Target Armature Found: {obj.name}")

# 4. List ALL actions in the file (even unassigned ones)
if not bpy.data.actions:
    print("No global actions found.")
else:
    for action in bpy.data.actions:
        print(f"Found Action: {action.name} (Frames: {action.frame_range[1]})")
        # Assign it to the armature to "wake it up"
        if armature:
            if not armature.animation_data:
                armature.animation_data_create()
            armature.animation_data.action = action

# 5. Scale and Apply
bpy.ops.object.select_all(action='SELECT')
bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 6. Export with explicit animation settings
output_path = r"C:\Users\logan\Documents\Megaman_Clean_Repo\_body\headcrab_scaled.glb"
bpy.ops.export_scene.gltf(
    filepath=output_path, 
    export_format='GLB',
    export_animations=True,
    export_animation_mode='ACTIONS', # Force all actions to export
    export_apply=True
)

print(f"Deep Surgery Complete: {output_path}")
