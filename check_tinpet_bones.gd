extends SceneTree

func _init():
	var glb = load("res://Tinpet_Male_New.glb")
	if not glb:
		print("❌ Could not load GLB")
		quit()
		
	var inst = glb.instantiate()
	var skeleton = inst.find_child("Skeleton3D", true, false)
	if skeleton:
		print("🦴 Bone List for Tinpet:")
		for i in range(skeleton.get_bone_count()):
			print("- ", skeleton.get_bone_name(i))
	else:
		print("❌ Skeleton3D not found in GLB")
	
	inst.free()
	quit()
