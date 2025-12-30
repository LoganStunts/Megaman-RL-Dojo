extends AIController3D

var skeleton: Skeleton3D
var simulator: PhysicalBoneSimulator3D
var root_bone: PhysicalBone3D

var physical_bones: Array[PhysicalBone3D] = []
var pb_cache = {}
var target_node: Node3D

func _ready():
	super._ready()
	
	# 1. Find Skeleton
	var n = self
	while n and not skeleton:
		skeleton = n.find_child("Skeleton3D", true, false)
		if skeleton: break
		n = n.get_parent()
			
	if not skeleton:
		print("CRITICAL ERROR: Headcrab AI could not find Skeleton3D!")
		return

	# 2. Setup Ragdoll
	_setup_ragdoll()
	
	# 3. Cache target
	target_node = get_parent().find_child("Target", true, false)

func _setup_ragdoll():
	simulator = PhysicalBoneSimulator3D.new()
	simulator.name = "PhysicalBoneSimulator3D"
	skeleton.add_child(simulator)
	
	# Mapping key jumper bones
	create_physical_bone("root")
	create_limb("frontLeg_0_L", "root")
	create_limb("frontLeg_1_L", "frontLeg_0_L")
	create_limb("frontLeg_0_R", "root")
	create_limb("frontLeg_1_R", "frontLeg_0_R")
	create_limb("backLeg_0_L", "root")
	create_limb("backLeg_1_L", "backLeg_0_L")
	create_limb("backLeg_0_R", "root")
	create_limb("backLeg_1_R", "backLeg_0_R")

	# Add all created bones to the AI list
	for child in simulator.get_children():
		if child is PhysicalBone3D:
			physical_bones.append(child)
			if child.bone_name == "root": root_bone = child

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
	
	# Collision Shape
	var shape = CollisionShape3D.new()
	var sphere = SphereShape3D.new()
	sphere.radius = 0.05
	shape.shape = sphere
	pb.add_child(shape)
	return pb

func create_limb(bone_name: String, parent_bone_name: String):
	var pb = create_physical_bone(bone_name)
	if pb: pb.joint_type = PhysicalBone3D.JOINT_TYPE_6DOF

func get_obs() -> Dictionary:
	var obs: Array[float] = []
	
	# 1. Position/Velocity relative to Target
	if root_bone and target_node:
		var rel_target = target_node.global_position - root_bone.global_position
		obs.append_array([rel_target.x, rel_target.y, rel_target.z])
		obs.append_array([root_bone.linear_velocity.x, root_bone.linear_velocity.y, root_bone.linear_velocity.z])
	else:
		obs.append_array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

	# 2. State of legs
	for bone in physical_bones:
		var q = bone.global_transform.basis.get_rotation_quaternion()
		obs.append_array([q.x, q.y, q.z, q.w])

	# Target size 128 (padding)
	while obs.size() < 128: obs.append(0.0)
	if obs.size() > 128: obs.resize(128)
	
	return {"obs": obs}

func get_reward() -> float:
	if not root_bone or not target_node: return 0.0
	
	var dist = root_bone.global_position.distance_to(target_node.global_position)
	var reward = 0.0
	
	# Reward for proximity
	reward += (5.0 - dist) * 0.1
	
	# Bonus for speed toward target
	var velocity_dot = root_bone.linear_velocity.dot((target_node.global_position - root_bone.global_position).normalized())
	reward += velocity_dot * 0.5
	
	# Massive bonus for contact
	if dist < 0.2:
		reward += 10.0
		
	# Penalty for upside down
	if root_bone.global_transform.basis.y.dot(Vector3.UP) < 0.0:
		reward -= 1.0
		
	return reward

func get_action_space() -> Dictionary:
	return {"action": {"size": physical_bones.size() * 3, "action_type": "continuous"}}

func set_action(action):
	var force_mult = 20.0
	for i in range(physical_bones.size()):
		var bone = physical_bones[i]
		var idx = i * 3
		if idx + 2 < action.size():
			var torque = Vector3(action[idx], action[idx+1], action[idx+2])
			bone.apply_torque_impulse(torque * force_mult)
