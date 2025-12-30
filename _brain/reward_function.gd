extends Node

var agent
var last_score = 0.0

func setup(agent_node):
	agent = agent_node

func calculate_reward() -> float:
	if not agent.skeleton or not agent.teacher_skeleton:
		return 0.0
	
	var reward = 0.0
	var pose_match = 0.0
	
	# 1. POSE IMITATION (The "Mirror" Reward)
	# We compare every bone rotation between the Student and the Ghost Teacher
	var bones_to_track = [
		"bip_pelvis", "bip_spine_1", "bip_head",
		"bip_hip_L", "bip_knee_0_L", "bip_foot_L",
		"bip_hip_R", "bip_knee_0_R", "bip_foot_R",
		"bip_upperArm_L", "bip_lowerArm_0_L",
		"bip_upperArm_R", "bip_lowerArm_0_R"
	]
	
	for bone_name in bones_to_track:
		var b_idx = agent.skeleton.find_bone(bone_name)
		if b_idx != -1:
			# Get rotation quaternions
			var student_q = agent.skeleton.get_bone_pose_rotation(b_idx)
			var teacher_q = agent.teacher_skeleton.get_bone_pose_rotation(b_idx)
			
			# Calculate similarity (1.0 = identical, 0.0 = opposite)
			var similarity = student_q.dot(teacher_q)
			pose_match += similarity
	
	# Reward for posing like the teacher
	reward += (pose_match / bones_to_track.size()) * 5.0
	
	# 2. HEIGHT PROGRESSION (The "Rising" Reward)
	var head_y = agent.head_bone.global_position.y
	reward += head_y * 2.0
	
	# 3. SUCCESS CONDITION (The Jackpot)
	if head_y > 1.2: # He is standing!
		reward += 100.0
		agent.needs_reset = true # Victory reset
		
	# 4. SURVIVAL PENALTY (Optional - keeps him moving)
	reward -= 0.1
	
	# 5. EFFICIENCY PENALTY (Stop Vibrating!)
	if "current_energy_usage" in agent:
		reward -= agent.current_energy_usage * 0.001
	
	return reward