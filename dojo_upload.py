import os
import subprocess
import argparse

# Configuration
BRANCH_NAME = "results/headcrab"
FILE_NAME = "headcrab_final"
ENCRYPTION_PASS = "Headcrab_2025" # Simple password for now (we can make this a secret later)
USER_NAME = "Dojo Bot"
USER_EMAIL = "dojo@megaman.ai"

def run_command(cmd, shell=False):
    print(f"🔧 Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        subprocess.check_call(cmd, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        exit(1)

def main():
    print("🚀 Initiating Secure Uplink...")

    # 1. Locate Files
    source_model = f"logs/checkpoints/{FILE_NAME}.zip"
    source_norm = "logs/checkpoints/vec_normalize.pkl"
    
    if not os.path.exists(source_model):
        print(f"❌ Critical: {source_model} not found!")
        exit(1)

    # 2. Encrypt & Zip
    # We use 7zip (installed on Colab by default) to create a password-protected zip
    output_zip = f"{FILE_NAME}_secure.7z"
    print(f"🔒 Encrypting payload to {output_zip}...")
    
    # -y answers yes to prompts
    cmd = f"7z a -t7z -y {output_zip} {source_model} {source_norm}"
    run_command(cmd, shell=True)

    # 3. Git Configuration
    print("☁️ Configuring Git...")
    run_command(["git", "config", "--global", "user.name", USER_NAME])
    run_command(["git", "config", "--global", "user.email", USER_EMAIL])

    # 4. Switch/Create Results Branch
    # We fetch first to see if it exists
    run_command(["git", "fetch", "origin"])
    try:
        run_command(["git", "checkout", BRANCH_NAME])
    except:
        print(f"🌱 Creating new branch: {BRANCH_NAME}")
        run_command(["git", "checkout", "-b", BRANCH_NAME])

    # 5. Commit & Push
    run_command(["git", "add", output_zip])
    run_command(["git", "commit", "-m", f"📦 Dojo Delivery: {FILE_NAME} (Encrypted)"])
    
    print("📤 Pushing to Remote...")
    # We rely on the git credentials already set in the Colab Launcher environment
    run_command(["git", "push", "-f", "origin", BRANCH_NAME])

    print("✅ Uplink Complete. Secure payload delivered.")

if __name__ == "__main__":
    main()
