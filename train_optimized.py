import argparse
import glob
import os
import pathlib
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecNormalize, DummyVecEnv
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
from stable_baselines3.common.callbacks import CheckpointCallback

# 1. Parse Arguments (We keep it compatible with our Launcher)
parser = argparse.ArgumentParser()
parser.add_argument("--env_path", default=None, type=str, help="Path to Godot binary")
parser.add_argument("--speedup", default=1, type=int, help="Physics speedup multiplier")
parser.add_argument("--n_parallel", default=1, type=int, help="Number of parallel envs")
parser.add_argument("--save_path", default="./logs/checkpoints", type=str, help="Where to save models")
parser.add_argument("--timesteps", default=1000000, type=int, help="Total training steps")
args = parser.parse_args()

# 2. Define the Environment Factory
# This function is needed for the Vectorized Environment
def make_env():
    # We pass the arguments to the Godot Wrapper
    # Note: We hardcode --headless inside the arg_args for safety
    return StableBaselinesGodotEnv(
        env_path=args.env_path,
        show_window=False, # Headless
        speedup=args.speedup,
        n_parallel=1, # We handle parallelism via DummyVecEnv/SubprocVecEnv if needed, but GodotRL handles n_parallel internally usually.
        # WAIT: GodotRL's StableBaselinesGodotEnv handles parallelism internally via n_parallel.
        # But VecNormalize expects a VecEnv. StableBaselinesGodotEnv IS a VecEnv.
        # So we don't need DummyVecEnv wrapper if GodotRL does it.
        # Let's verify: Yes, StableBaselinesGodotEnv inherits from VecEnv.
    )

# 3. Create Environment
# We instantiate the env with the parallel setting
env = StableBaselinesGodotEnv(
    env_path=args.env_path,
    show_window=False, 
    speedup=args.speedup,
    n_parallel=args.n_parallel
)

# 4. NORMALIZATION (The Fix)
# We wrap the Godot Env in VecNormalize to fix the "Tiny Reward" bug.
# clip_obs=10.0 prevents extreme values from breaking the brain.
env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.0)

# 5. Define Callbacks (Auto-Save)
checkpoint_callback = CheckpointCallback(
    save_freq=50000, 
    save_path=args.save_path,
    name_prefix="megaman_slow"
)

# 6. Load Model (Fresh Start for Headcrab)
print("🧠 Starting fresh Megaman (Slow) neural network...")
model = PPO(
    "MultiInputPolicy", 
    env, 
    verbose=1,
    learning_rate=0.0003, # Slightly higher LR for initial learning
    clip_range=0.2,
    device="cpu", # FORCE CPU because RTX 5070 (sm_120) is too new for current PyTorch
    tensorboard_log=f"{args.save_path}/../tensorboard"
)

# 7. Train (Long Session)
TOTAL_STEPS = 10000000 # 10 Million Steps
print(f"🚀 Starting Marathon Training for {TOTAL_STEPS} steps...")
print(f"💾 Checkpoints saving to: {args.save_path}")

try:
    model.learn(total_timesteps=TOTAL_STEPS, callback=checkpoint_callback, reset_num_timesteps=False)
    model.save(f"{args.save_path}/megaman_slow_final")
    env.save(f"{args.save_path}/vec_normalize.pkl") # Save normalization stats!
    print("✅ Training Complete.")
except KeyboardInterrupt:
    print("⚠️ Training Interrupted. Saving emergency backup...")
    model.save(f"{args.save_path}/interrupted_model")
    env.save(f"{args.save_path}/vec_normalize.pkl")
finally:
    env.close()
