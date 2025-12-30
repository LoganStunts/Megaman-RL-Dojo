extends SceneTree

func _init():
	print("--- BONE INSPECTION START ---")
	var tinpet_path = "res://Tinpet_Male_New.glb"
	var anim_path = "res://drunk_walk.fbx" # We will copy this in a second
	
	var tinpet = load(tinpet_path).instantiate()
	var skel = tinpet.find_child("Skeleton3D", true, false)
	
	if skel:
		print("Tinpet Bones:")
		for i in range(skel.get_bone_count()):
			print("  - ", skel.get_bone_name(i))
	else:
		print("ERROR: No skeleton found in Tinpet!")
		
	quit()
