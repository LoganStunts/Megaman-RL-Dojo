import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecNormalize
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
import os

# Define paths
MODEL_PATH = "_brain/megaman_v1.zip"
VEC_NORM_PATH = "_brain/megaman_v1/vec_normalize.pkl"
PORT = 11008

# Create the environment (Visual Mode)
env = StableBaselinesGodotEnv(
    env_path=None, 
    show_window=True,
    speedup=1,
    port=PORT
)

# Patch render_mode for Gymnasium compatibility
if not hasattr(env, "render_mode"):
    env.render_mode = None

# Apply Normalization
if os.path.exists(VEC_NORM_PATH):
    print(f"📈 Loading Normalization Stats: {VEC_NORM_PATH}")
    env = VecNormalize.load(VEC_NORM_PATH, env)
    env.training = False
    env.norm_reward = False 
else:
    print("⚠️ Warning: vec_normalize.pkl not found! AI might behave erratically.")

# Load the model
try:
    model = PPO.load(MODEL_PATH, env=env, device="cpu")
    print("🧠 11-Million Step Brain Loaded Successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Run the Loop
reset_result = env.reset()
if isinstance(reset_result, tuple):
    obs = reset_result[0]
else:
    obs = reset_result

print("Starting Preview Loop...")

try:
    while True:
        action, _ = model.predict(obs, deterministic=False)
        step_result = env.step(action)
        
        # Handle the result being either (obs, reward, done, info) or (obs, reward, terminated, truncated, info)
        obs = step_result[0]
        done = step_result[2] or (step_result[3] if len(step_result) > 4 else False)
        
        if done:
            reset_result = env.reset()
            if isinstance(reset_result, tuple):
                obs = reset_result[0]
            else:
                obs = reset_result

except KeyboardInterrupt:
    print("Preview stopped by user.")
    env.close()