extends Node

var agent
var target_node
var last_dist = 0.0

func setup(agent_node):
	agent = agent_node
	# Find the target in the gym
	target_node = agent.get_tree().current_scene.find_child("Target", true, false)

func calculate_reward() -> float:
	if not agent.head_bone or not agent.pelvis_bone:
		return 0.0
	
	var head_y = agent.head_bone.global_position.y
	var reward = 0.0
	
	# 1. Survival Reward (Height)
	if head_y > 0.5:
		reward += 1.0
	else:
		reward -= 1.0 # Heavier penalty for falling
		
	# 2. Upright Reward (Balance)
	var head_up = agent.head_bone.global_transform.basis.y
	var alignment = head_up.dot(Vector3.UP)
	reward += alignment * 0.5
	
	# 3. Movement Reward (Ambition)
	if target_node:
		var current_dist = agent.pelvis_bone.global_position.distance_to(target_node.global_position)
		
		# Breadcrumb for getting closer
		if current_dist < last_dist:
			reward += 0.2
		
		# Jackpot for reaching target
		if current_dist < 1.5:
			reward += 20.0
			agent.needs_reset = true # Success reset!
			
		last_dist = current_dist
	
	return reward