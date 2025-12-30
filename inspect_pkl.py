import pickle
import os

path = "_brain/headcrab_v1/vec_normalize.pkl"

if not os.path.exists(path):
    print("❌ File not found.")
    exit()

with open(path, "rb") as f:
    data = pickle.load(f)

print("🔍 Inspecting vec_normalize.pkl...")
if hasattr(data, "observation_space"):
    print(f"Observation Space: {data.observation_space}")
else:
    print("⚠️ No observation_space found in pickle data.")
