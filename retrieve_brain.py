import os
import subprocess
import shutil

# Config
BRANCH_NAME = "results/megaman_slow"
FILE_NAME = "megaman_slow_final"
ENCRYPTION_PASS = "Megaman_Slow_2025"
DEST_DIR = "_brain/megaman_slow_v1"

def run_command(cmd):
    print(f"🔧 Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, shell=True)

def main():
    print("📡 Scanning for orbital drop...")
    
    # 1. Fetch Remote
    run_command(["git", "fetch", "origin"])
    
    # 2. Checkout the Results Branch
    # We force checkout to overwrite local changes if any
    run_command(["git", "checkout", BRANCH_NAME])
    run_command(["git", "pull", "origin", BRANCH_NAME])
    
    # 3. Locate Payload
    zip_file = f"{FILE_NAME}_secure.7z"
    if not os.path.exists(zip_file):
        print(f"❌ Error: Payload {zip_file} not found on branch {BRANCH_NAME}!")
        return

    # 4. Decrypt & Extract
    print(f"🔓 Decrypting payload to {DEST_DIR}...")
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR, exist_ok=True)
    
    # 7z x -p{PASS} -o{DEST} {FILE}
    # Assuming 7z is in your PATH. If not, we might need a full path or a python lib.
    # Windows typically doesn't have 7z in PATH by default.
    # Let's try to use the py7zr library or assume standard 7z executable.
    
    try:
        cmd = f"7z x -p{ENCRYPTION_PASS} -y -o{DEST_DIR} {zip_file}"
        run_command(cmd)
        print("✅ Extraction Complete.")
        print(f"🧠 Brain located at: {DEST_DIR}")
        print("👉 Run: python preview_crab.py --model_path " + DEST_DIR)
        
    except Exception as e:
        print("⚠️ 7-Zip failed (is it in PATH?). Attempting manual python unzip (Note: Python zipfile doesn't support 7z encryption well usually).")
        print("Please install 7-Zip and ensure '7z' is in your system PATH, or manually extract.")
        print(f"File location: {os.path.abspath(zip_file)}")

if __name__ == "__main__":
    main()
