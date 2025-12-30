extends AIController3D

var skeleton: Skeleton3D
var simulator: PhysicalBoneSimulator3D
var head_bone: PhysicalBone3D

var physical_bones: Array[PhysicalBone3D] = []
var pb_cache = {}
var pelvis_bone: PhysicalBone3D
var reward_calculator
var current_energy_usage = 0.0

# --- GHOST TEACHER SYSTEM ---
var teacher_skeleton: Skeleton3D
var anim_player: AnimationPlayer
var current_anim_name = ""

func _ready():
	super._ready()
	
	# 1. Find the real skeleton
	var n = self
	while n and not skeleton:
		skeleton = n.find_child("Skeleton3D", true, false)
		if skeleton: break
		n = n.get_parent()
			
	if not skeleton:
		print("CRITICAL ERROR: AIController could not find Skeleton3D!")
		return

	# 2. Setup Procedural Ragdoll
	_setup_ragdoll()
	
	# 3. Setup AI Components
	for child in simulator.get_children():
		if child is PhysicalBone3D:
			physical_bones.append(child)
	
	if pb_cache.has("bip_head"):
		head_bone = pb_cache["bip_head"]
	if pb_cache.has("bip_pelvis"):
		pelvis_bone = pb_cache["bip_pelvis"]

	# 4. SETUP GHOST TEACHER
	_setup_teacher()

	# 5. Load Reward Function
	var reward_path = "res://_brain/reward_function.gd"
	if FileAccess.file_exists(reward_path):
		reward_calculator = load(reward_path).new()
		reward_calculator.setup(self)

func _setup_teacher():
	teacher_skeleton = skeleton.duplicate()
	teacher_skeleton.name = "GhostTeacher"
	teacher_skeleton.visible = false
	get_parent().add_child.call_deferred(teacher_skeleton)
	
	anim_player = AnimationPlayer.new()
	anim_player.name = "TeacherAnimPlayer"
	teacher_skeleton.add_child.call_deferred(anim_player)
	
	var library = AnimationLibrary.new()
	
	# Helper function to extract mixamo anim from FBX scene
	var extract_anim = func(path: String, new_name: String):
		var scene = load(path)
		if scene:
			var inst = scene.instantiate()
			var ap = inst.find_child("AnimationPlayer", true, false)
			if ap:
				var anim_list = ap.get_animation_list()
				if anim_list.size() > 0:
					var anim = ap.get_animation(anim_list[0])
					if anim:
						library.add_animation(new_name, anim)
			inst.free() # Clean up temp instance

	extract_anim.call("res://animations/standing_belly.fbx", "stand_belly")
	extract_anim.call("res://animations/standing_back.fbx", "stand_back")
	
	anim_player.add_animation_library("", library)

func reset_teacher():
	# Pick a random starting state
	var roll = randf()
	if roll < 0.5:
		current_anim_name = "stand_belly"
	else:
		current_anim_name = "stand_back"
	
	if anim_player:
		anim_player.speed_scale = 0.5 # SLOW MOTION TRAINING
		anim_player.play(current_anim_name)
		anim_player.seek(0.0, true) # Start at beginning

func _setup_ragdoll():
	var existing_sim = skeleton.find_child("PhysicalBoneSimulator3D")
	if existing_sim:
		existing_sim.queue_free()
	
	simulator = PhysicalBoneSimulator3D.new()
	simulator.name = "PhysicalBoneSimulator3D"
	skeleton.add_child(simulator)
	
	create_physical_bone("bip_pelvis")
	create_limb("bip_hip_L", "bip_pelvis")
	create_limb("bip_knee_0_L", "bip_hip_L")
	create_limb("bip_foot_L", "bip_knee_0_L")
	create_limb("bip_hip_R", "bip_pelvis")
	create_limb("bip_knee_0_R", "bip_hip_R")
	create_limb("bip_foot_R", "bip_knee_0_R")
	create_limb("bip_spine_0", "bip_pelvis")
	create_limb("bip_spine_1", "bip_spine_0")
	create_limb("bip_neck", "bip_spine_1")
	create_limb("bip_head", "bip_neck")
	create_limb("bip_collar_L", "bip_spine_1")
	create_limb("bip_upperArm_L", "bip_collar_L")
	create_limb("bip_lowerArm_0_L", "bip_upperArm_L")
	create_limb("bip_hand_L", "bip_lowerArm_0_L")
	create_limb("bip_collar_R", "bip_spine_1")
	create_limb("bip_upperArm_R", "bip_collar_R")
	create_limb("bip_lowerArm_0_R", "bip_upperArm_R")
	create_limb("bip_hand_R", "bip_lowerArm_0_R")

	simulator.physical_bones_start_simulation()
	skeleton.physical_bones_start_simulation()

func create_physical_bone(bone_name: String) -> PhysicalBone3D:
	var bone_idx = skeleton.find_bone(bone_name)
	if bone_idx == -1: return null
	var pb = PhysicalBone3D.new()
	pb.name = "PB_" + bone_name
	pb.bone_name = bone_name
	simulator.add_child(pb)
	var bone_global_pose = skeleton.get_bone_global_pose(bone_idx)
	pb.global_transform = skeleton.global_transform * bone_global_pose
	pb_cache[bone_name] = pb
	
	var shape = CollisionShape3D.new()
	var col_shape
	
	# --- SMART COLLISION SIZING ---
	if "pelvis" in bone_name:
		col_shape = BoxShape3D.new()
		col_shape.size = Vector3(0.15, 0.1, 0.1) # Wide hips
	elif "foot" in bone_name:
		col_shape = BoxShape3D.new()
		col_shape.size = Vector3(0.06, 0.03, 0.12) # Flat soles for balance
	elif "head" in bone_name:
		col_shape = SphereShape3D.new()
		col_shape.radius = 0.08
	elif "spine" in bone_name:
		col_shape = CapsuleShape3D.new()
		col_shape.radius = 0.08
		col_shape.height = 0.2
	else:
		# Standard Limbs
		col_shape = CapsuleShape3D.new()
		col_shape.radius = 0.025
		col_shape.height = 0.15
	
	shape.shape = col_shape
	pb.add_child(shape)
	return pb

func create_limb(bone_name: String, parent_bone_name: String):
	var pb = create_physical_bone(bone_name)
	if pb: pb.joint_type = PhysicalBone3D.JOINT_TYPE_6DOF

func get_obs() -> Dictionary:
	var obs: Array[float] = []
	if pelvis_bone:
		obs.append(pelvis_bone.global_position.y)
		var rot = pelvis_bone.global_transform.basis.get_rotation_quaternion()
		obs.append_array([rot.x, rot.y, rot.z, rot.w])
		obs.append(pelvis_bone.linear_velocity.length())
		obs.append(pelvis_bone.angular_velocity.length())
	else:
		obs.append_array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])

	for bone in physical_bones:
		var rel_pos = self.global_transform.affine_inverse() * bone.global_position
		obs.append_array([rel_pos.x, rel_pos.y, rel_pos.z])
		var q = bone.global_transform.basis.get_rotation_quaternion()
		obs.append_array([q.x, q.y, q.z, q.w])
		var lv = bone.linear_velocity
		obs.append_array([lv.x, lv.y, lv.z])
		var av = bone.angular_velocity
		obs.append_array([av.x, av.y, av.z])

	var target_size = 317
	while obs.size() < target_size: obs.append(0.0)
	if obs.size() > target_size: obs.resize(target_size)
	return {"obs": obs}

func get_reward() -> float:
	if reward_calculator:
		return reward_calculator.calculate_reward()
	return 0.0

func get_action_space() -> Dictionary:
	return {"action": {"size": 159, "action_type": "continuous"}}

func set_action(action):
	var torque_multiplier = 50.0 # Give him real muscle power
	current_energy_usage = 0.0
	
	for i in range(physical_bones.size()):
		var bone = physical_bones[i]
		var idx = i * 3
		if idx + 2 < action.size():
			var torque = Vector3(action[idx], action[idx+1], action[idx+2])
			bone.apply_torque_impulse(torque * torque_multiplier)
			current_energy_usage += torque.length()
