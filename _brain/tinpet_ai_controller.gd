extends AIController3D

var skeleton: Skeleton3D
var simulator: PhysicalBoneSimulator3D
var head_bone: PhysicalBone3D

var physical_bones: Array[PhysicalBone3D] = []
var pb_cache = {}
var pelvis_bone: PhysicalBone3D
var reward_calculator

func _ready():
	super._ready()
	
	# --- ROBUST SKELETON FINDER ---
	# Search from self upwards to find the first Skeleton3D in this branch
	var n = self
	while n and not skeleton:
		skeleton = n.find_child("Skeleton3D", true, false)
		if skeleton: break
		n = n.get_parent()
			
	if not skeleton:
		print("CRITICAL ERROR: AIController could not find Skeleton3D in hierarchy!")
		# Fallback: Print tree to debug
		_print_tree_recursive(get_tree().current_scene, 0)
		return

	print("AIController: Found Skeleton at " + str(skeleton.get_path()))

	# 2. Setup Procedural Ragdoll
	_setup_ragdoll()
	
	# 3. Setup AI Components
	# Cache all physical bones for control
	for child in simulator.get_children():
		if child is PhysicalBone3D:
			physical_bones.append(child)
	
	# Find head for observation
	if pb_cache.has("bip_head"):
		head_bone = pb_cache["bip_head"]
	else:
		if physical_bones.size() > 0:
			head_bone = physical_bones[0]

	# Load Reward Function from the correct folder
	var reward_path = "res://_brain/reward_function.gd"
	if FileAccess.file_exists(reward_path):
		reward_calculator = load(reward_path).new()
		reward_calculator.setup(self)
		print("AIController: Loaded reward function from " + reward_path)
	else:
		print("AIController: WARNING - Reward function not found at " + reward_path)

func _setup_ragdoll():
	# Check if simulator already exists (cleanup from previous runs or editor)
	# Important for re-running in editor or quick resets
	var existing_sim = skeleton.find_child("PhysicalBoneSimulator3D")
	if existing_sim:
		existing_sim.name = "PhysicalBoneSimulator3D_Old"
		existing_sim.queue_free()
	
	# Create Simulator
	simulator = PhysicalBoneSimulator3D.new()
	simulator.name = "PhysicalBoneSimulator3D"
	skeleton.add_child(simulator)
	
	# --- Build Body ---
	# We use the names found in Tinpet_Male_New.fbx
	
	# Root
	create_physical_bone("bip_pelvis")
	if pb_cache.has("bip_pelvis"):
		pelvis_bone = pb_cache["bip_pelvis"]
	
	# Lower Body
	create_limb("bip_hip_L", "bip_pelvis")
	create_limb("bip_knee_0_L", "bip_hip_L")
	create_limb("bip_foot_L", "bip_knee_0_L")
	
	create_limb("bip_hip_R", "bip_pelvis")
	create_limb("bip_knee_0_R", "bip_hip_R")
	create_limb("bip_foot_R", "bip_knee_0_R")
	
	# Upper Body
	create_limb("bip_spine_0", "bip_pelvis")
	create_limb("bip_spine_1", "bip_spine_0")
	create_limb("bip_neck", "bip_spine_1")
	create_limb("bip_head", "bip_neck")
	
	# Arms
	create_limb("bip_collar_L", "bip_spine_1")
	create_limb("bip_upperArm_L", "bip_collar_L")
	create_limb("bip_lowerArm_0_L", "bip_upperArm_L")
	create_limb("bip_hand_L", "bip_lowerArm_0_L")
	
	create_limb("bip_collar_R", "bip_spine_1")
	create_limb("bip_upperArm_R", "bip_collar_R")
	create_limb("bip_lowerArm_0_R", "bip_upperArm_R")
	create_limb("bip_hand_R", "bip_lowerArm_0_R")

	# Start Simulation
	simulator.physical_bones_start_simulation()
	skeleton.physical_bones_start_simulation()
	print("AIController: Ragdoll simulation started.")

func create_physical_bone(bone_name: String) -> PhysicalBone3D:
	var bone_idx = skeleton.find_bone(bone_name)
	if bone_idx == -1:
		# print("Ragdoll Gen: Bone not found: " + bone_name)
		return null
		
	var pb = PhysicalBone3D.new()
	pb.name = "PB_" + bone_name
	pb.bone_name = bone_name
	simulator.add_child(pb)
	
	# ALIGNMENT: Match the physical bone to the skeleton's bone pose
	var bone_global_pose = skeleton.get_bone_global_pose(bone_idx)
	var world_transform = skeleton.global_transform * bone_global_pose
	pb.global_transform = world_transform
	
	# Cache for joint creation
	pb_cache[bone_name] = pb
	
	# Physics Shape (Capsule is best for limbs)
	var shape = CollisionShape3D.new()
	var capsule = CapsuleShape3D.new()
	capsule.radius = 0.03
	capsule.height = 0.1
	shape.shape = capsule
	pb.add_child(shape)
	
	# Debug Mesh (Red capsules)
	var mesh_inst = MeshInstance3D.new()
	var mesh = CapsuleMesh.new()
	mesh.radius = 0.03
	mesh.height = 0.1
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color.RED
	mat.no_depth_test = true # See through mesh
	mesh.material = mat
	mesh_inst.mesh = mesh
	# mesh_inst.visible = false # Toggle this to hide red capsules
	pb.add_child(mesh_inst)
	
	return pb

func create_limb(bone_name: String, parent_bone_name: String):
	var pb = create_physical_bone(bone_name)
	if not pb: return
	
	var parent_pb_node = pb_cache.get(parent_bone_name)
	if not parent_pb_node:
		return
	
	# Joint connection
	pb.joint_type = PhysicalBone3D.JOINT_TYPE_6DOF

func get_obs() -> Dictionary:
	var obs: Array[float] = []
	
	# 1. Root Data (7 floats)
	if pelvis_bone:
		obs.append(pelvis_bone.global_position.y) # Height
		var rot = pelvis_bone.global_transform.basis.get_rotation_quaternion()
		obs.append(rot.x)
		obs.append(rot.y)
		obs.append(rot.z)
		obs.append(rot.w)
		obs.append(pelvis_bone.linear_velocity.length())
		obs.append(pelvis_bone.angular_velocity.length())
	else:
		obs.append_array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])

	# 2. Bone Data (Physical Bones)
	# We need to reach 317 total. 
	# Current Strategy: Dump everything we know about every bone.
	for bone in physical_bones:
		# Relative Position (3)
		var rel_pos = self.global_transform.affine_inverse() * bone.global_position
		obs.append(rel_pos.x)
		obs.append(rel_pos.y)
		obs.append(rel_pos.z)
		
		# Rotation (4)
		var q = bone.global_transform.basis.get_rotation_quaternion()
		obs.append(q.x)
		obs.append(q.y)
		obs.append(q.z)
		obs.append(q.w)
		
		# Velocity (3)
		var lv = bone.linear_velocity
		obs.append(lv.x)
		obs.append(lv.y)
		obs.append(lv.z)
		
		# Angular Velocity (3)
		var av = bone.angular_velocity
		obs.append(av.x)
		obs.append(av.y)
		obs.append(av.z)

	# 3. Padding to hit 317
	var current_size = obs.size()
	var target_size = 317
	
	if current_size < target_size:
		var diff = target_size - current_size
		# print("Padding obs with " + str(diff) + " zeros.")
		for i in range(diff):
			obs.append(0.0)
	elif current_size > target_size:
		# print("Truncating obs from " + str(current_size) + " to " + str(target_size))
		obs.resize(target_size)
		
	return {"obs": obs}

func get_reward() -> float:
	if reward_calculator:
		return reward_calculator.calculate_reward()
	return 0.0

func get_action_space() -> Dictionary:
	return {
		"action": {
			"size": 159, 
			"action_type": "continuous"
		}
	}

func set_action(action):
	# Apply torques to physical bones
	# The brain sends 159 actions, but we only have ~19 bones (57 actions).
	# We map the first 57 actions to our bones and ignore the rest.
	for i in range(physical_bones.size()):
		var bone = physical_bones[i]
		var idx = i * 3
		if idx + 2 < action.size():
			var torque = Vector3(action[idx], action[idx+1], action[idx+2])
			bone.angular_velocity += torque * 0.1

func _print_tree_recursive(node, indent):
	var s = ""
	for i in range(indent): s += "  "
	print(s + node.name + " (" + node.get_class() + ")")
	for child in node.get_children():
		_print_tree_recursive(child, indent + 1)