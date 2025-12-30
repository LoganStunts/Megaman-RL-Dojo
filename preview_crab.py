import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecNormalize
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
import os

# 1. Config
MODEL_PATH = "_brain/headcrab_v1" # This is the folder containing policy.pth etc
VEC_NORM_PATH = os.path.join(MODEL_PATH, "vec_normalize.pkl")
PORT = 11008 # Standard GodotRL Port

# 2. Create the environment (Connect to Godot)
env = StableBaselinesGodotEnv(
    env_path=None, 
    show_window=True,
    speedup=1,
    port=PORT
)

# Fix: Patch the missing render_mode attribute to satisfy VecNormalize/Gymnasium
if not hasattr(env, "render_mode"):
    env.render_mode = None

print(f"DEBUG: Godot Env Obs Space: {env.observation_space}")

# 3. Apply Normalization (CRITICAL for trained brains)
if os.path.exists(VEC_NORM_PATH):
    print(f"📈 Loading Normalization Stats: {VEC_NORM_PATH}")
    # Load and check pkl
    temp_env = VecNormalize.load(VEC_NORM_PATH, env)
    print(f"DEBUG: Pkl Obs Space: {temp_env.observation_space}")
    env = temp_env
    # Important: In evaluation mode, we don't update stats
    env.training = False
    env.norm_reward = False 
else:
    print("⚠️ Warning: vec_normalize.pkl not found! AI might behave erratically.")

# 4. Load the Brain
print(f"🧠 Loading Brain: {MODEL_PATH}")
model = PPO.load(MODEL_PATH, env=env)

print("🚀 Headcrab Dojo Initialized.")
print("👉 Press PLAY in Godot (Headcrab_Gym.tscn must be open!)")

obs = env.reset()

try:
    while True:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        if any(terminated) or any(truncated):
            obs = env.reset()

except KeyboardInterrupt:
    print("Preview stopped.")
    env.close()
