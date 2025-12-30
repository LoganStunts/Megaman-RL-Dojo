extends SceneTree

func _init():
	var path = "res://_body/headcrab_scaled.glb"
	var scene = load(path)
	if not scene:
		print("Failed to load model at: ", path)
		quit()
		return
		
	var inst = scene.instantiate()
	var skeleton: Skeleton3D = inst.find_child("Skeleton3D", true, false)
	
	if skeleton:
		print("--- BONE LIST ---")
		for i in range(skeleton.get_bone_count()):
			print(i, ": ", skeleton.get_bone_name(i))
	else:
		print("No Skeleton3D found in model.")
		
	inst.free()
	quit()
