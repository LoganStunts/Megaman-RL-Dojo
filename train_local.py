import argparse
import os
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecNormalize
from godot_rl.wrappers.stable_baselines_wrapper import StableBaselinesGodotEnv
from stable_baselines3.common.callbacks import CheckpointCallback

from stable_baselines3.common.callbacks import CheckpointCallback, BaseCallback

class SaveVecNormalizeCallback(BaseCallback):
    def __init__(self, save_path: str, verbose=0):
        super(SaveVecNormalizeCallback, self).__init__(verbose)
        self.save_path = save_path

    def _on_step(self) -> bool:
        if self.n_calls % (50000 // self.training_env.num_envs) == 0:
            self.training_env.save(os.path.join(self.save_path, "vec_normalize_local.pkl"))
        return True

# --- CONFIGURATION ---
GODOT_BIN = r"C:\Users\logan\_MEGAMAN_CORE\Tools\Godot_v4.5.1-stable_win64_console.exe"
PROJECT_PATH = r"C:\Users\logan\Documents\Megaman_Clean_Repo"
LOG_DIR = "./logs"
CHECKPOINT_DIR = "./logs/checkpoints"

# Ensure directories exist
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# --- ENVIRONMENT SETUP ---
print("🚀 Initializing Local Dojo Engine...")
print(f"💻 Hardware: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU (WARNING)'}")

# We use 32 parallel environments for your 24-core i9 (Turbo Mode)
n_parallel = 32

env = StableBaselinesGodotEnv(
    env_path=GODOT_BIN,
    show_window=False, # We keep it headless for speed
    speedup=8,         # 8x speed physics
    n_parallel=n_parallel,
    # Additional arguments for Godot
    arg_args=["--path", PROJECT_PATH, "--headless"]
)

# NORMALIZATION (The Fix for the 'Silent Killer')
env = VecNormalize(env, norm_obs=True, norm_reward=True, clip_obs=10.0)

# --- CALLBACKS ---
# Save every 50k steps
checkpoint_callback = CheckpointCallback(
    save_freq=50000 // n_parallel, 
    save_path=CHECKPOINT_DIR,
    name_prefix="megaman_local"
)
save_vec_callback = SaveVecNormalizeCallback(save_path=LOG_DIR)

# --- MODEL ---
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    learning_rate=1e-4, # Stable learning rate
    clip_range=0.1,    # Prevent policy thrashing
    batch_size=128,    # Optimized for your CPU memory
    tensorboard_log=LOG_DIR,
    device="cpu"       # FORCE CPU MODE DUE TO GPU INCOMPATIBILITY
)

# --- START ---
print(f"🧠 Training on {n_parallel} instances. Neural Interface Engaged.")
print("📈 Launch TensorBoard to watch progress: tensorboard --logdir ./logs")

try:
    model.learn(total_timesteps=2000000, callback=[checkpoint_callback, save_vec_callback])
    model.save(f"{LOG_DIR}/megaman_final_local")
    env.save(f"{LOG_DIR}/vec_normalize_local.pkl")
    print("✅ Training Complete. Megaman has graduated.")
except KeyboardInterrupt:
    print("🛑 Training Interrupted. Saving latest weights...")
    model.save(f"{LOG_DIR}/megaman_interrupted")
    env.save(f"{LOG_DIR}/vec_normalize_local.pkl")
finally:
    env.close()
