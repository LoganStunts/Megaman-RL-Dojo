import os
import subprocess
import shutil
import json
from datetime import datetime

# Config
BRANCH_NAME = "results/headcrab" 
ENCRYPTION_PASS = "Headcrab_2025"
LIBRARY_ROOT = "_brain/_LIBRARY"
LOG_FILE = "BRAIN_LOG.json"

# Concept Mapping: Branch -> (ModelName, Concept)
CONCEPT_MAP = {
    "results/headcrab": ("Headcrab", "RayCast"),
    "results/megaman_slow": ("Megaman", "SlowTeacher")
}

def run_command(cmd):
    print(f"🔧 Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, shell=True)

def get_timestamp():
    return datetime.now().strftime("%m-%d-%H%M")

def update_log(entry_key, data):
    library = {}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                library = json.load(f)
        except:
            print("⚠️ Could not read existing log, starting fresh.")
    
    library[entry_key] = data
    
    with open(LOG_FILE, "w") as f:
        json.dump(library, f, indent=4)
    print(f"📖 Log updated: {entry_key}")

def main():
    print("📡 Scanning for orbital drop...")
    
    # 1. Fetch Remote
    run_command(["git", "fetch", "origin"])
    run_command(["git", "checkout", BRANCH_NAME])
    run_command(["git", "pull", "origin", BRANCH_NAME])
    
    # 2. Locate Payload
    zip_candidates = [f for f in os.listdir('.') if f.endswith("_secure.7z")]
    if not zip_candidates:
        print(f"❌ Error: No secure payload found on branch {BRANCH_NAME}!")
        return
    
    zip_file = zip_candidates[0]
    print(f"📦 Found payload: {zip_file}")

    # 3. Determine Identity
    model_name, concept = CONCEPT_MAP.get(BRANCH_NAME, ("Unknown", "Experimental"))
    timestamp = get_timestamp()
    final_name = f"{model_name}_{concept}_{timestamp}"
    
    # Destination: _brain/_LIBRARY/Headcrab/Headcrab_RayCast_12-30-0930/
    dest_path = os.path.join(LIBRARY_ROOT, model_name, final_name)

    # 4. Decrypt & Extract
    print(f"🔓 Decrypting payload to {dest_path}...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.makedirs(dest_path, exist_ok=True)
    
    try:
        # Decrypt (No Password)
        cmd = f"7z x -y -o{dest_path} {zip_file}"
        run_command(cmd)
        
        # Rename inner zip
        final_zip_path = ""
        for root, dirs, files in os.walk(dest_path):
            for file in files:
                if file.endswith(".zip"):
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, f"{final_name}.zip")
                    os.rename(old_path, new_path)
                    final_zip_path = new_path
                    print(f"🏷️ Renamed inner file to: {final_name}.zip")

        # 5. Log It
        log_entry = {
            "model": model_name,
            "concept": concept,
            "timestamp": timestamp,
            "path": dest_path,
            "zip_file": final_zip_path,
            "origin_branch": BRANCH_NAME
        }
        update_log(final_name, log_entry)

        print("✅ Archive Complete.")
        print(f"🧠 Brain shelved at: {dest_path}")
        print(f"👉 Run: python preview_crab.py --model_path \"{final_zip_path}\"")
        
    except Exception as e:
        print(f"⚠️ Extraction failed: {e}")

if __name__ == "__main__":
    main()
