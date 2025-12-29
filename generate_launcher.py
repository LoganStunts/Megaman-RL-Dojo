import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🤖 Megaman RL Training Facility (The Dojo)\n",
    "\n",
    "### 📋 Instructions\n",
    "1. **Runtime:** Ensure you are using **T4 GPU** (Runtime -> Change runtime type).\n",
    "2. **Run All:** Execute the cells below in order."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# @title 1. Initialize Dojo (Clone & Update)\n",
    "import os\n",
    "\n",
    "REPO_URL = \"https://github.com/LoganStunts/Megaman-RL-Dojo.git\"\n",
    "REPO_NAME = \"Megaman-RL-Dojo\"\n",
    "\n",
    "if not os.path.exists(REPO_NAME):\n",
    "    print(f\"📥 Cloning {REPO_NAME}...\")\n",
    "    !git clone {REPO_URL}\n",
    "else:\n",
    "    print(f\"🔄 Updating {REPO_NAME}...\")\n",
    "    %cd {REPO_NAME}\n",
    "    !git pull\n",
    "    %cd ..\n",
    "\n",
    "%cd {REPO_NAME}\n",
    "print(\"✅ Repo Ready.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# @title 2. Infrastructure Setup\n",
    "# @markdown Install Linux dependencies, XVFB (Virtual Display), and Godot Headless.\n",
    "\n",
    "!apt-get install -y libxcursor1 libxinerama1 libxrandr2 libxi6 libgl1-mesa-dev xvfb\n",
    "!pip install -r requirements.txt\n",
    "\n",
    "if not os.path.exists(\"Godot_v4.5.1-stable_linux.x86_64\"):\n",
    "    print(\"⬇️ Downloading Godot 4.5.1...\")\n",
    "    !wget https://github.com/godotengine/godot/releases/download/4.5.1-stable/Godot_v4.5.1-stable_linux.x86_64.zip\n",
    "    !unzip -o Godot_v4.5.1-stable_linux.x86_64.zip\n",
    "    !chmod +x Godot_v4.5.1-stable_linux.x86_64\n",
    "else:\n",
    "    print(\"✅ Godot binary found.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# @title 3. Payload Injection\n",
    "TARGET_BRANCH = \"payload/main\"\n",
    "\n",
    "!git fetch origin\n",
    "!git checkout {TARGET_BRANCH}\n",
    "!git pull origin {TARGET_BRANCH}\n",
    "print(f\"✅ Switched to {TARGET_BRANCH} (Latest Version).\" )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# @title 4. Ignite Training (XVFB Mode)\n",
    "import subprocess\n",
    "import time\n",
    "import sys\n",
    "import os\n",
    "\n",
    "# --- STEP 0: FORCE INSTALL (Self-Healing) ---",
    "try:\n",
    "    import godot_rl\n",
    "    print(\"✅ godot_rl is detected.\")\n",
    "except ImportError:\n",
    "    print(\"⚠️ godot_rl not found. Installing dependencies now...\")\n",
    "    !pip install godot-rl stable-baselines3 shimmy>=0.2.1 tensorboard huggingface_sb3 onnx\n",
    "    print(\"✅ Installation complete.\")\n",
    "\n",
    "# --- STEP 1: CLEANUP ---",
    "subprocess.run([\"pkill\", \"-f\", \"Godot\"])\n",
    "time.sleep(2)\n",
    "\n",
    "# --- STEP 2: DEFINE PORTS ---",
    "GODOT_BIN = \"/content/Megaman-RL-Dojo/Godot_v4.5.1-stable_linux.x86_64\"\n",
    "PROJECT_PATH = \"/content/Megaman-RL-Dojo\"\n",
    "\n",
    "# --- STEP 3: IMPORT ASSETS (With Virtual Display) ---",
    "print(\"📦 Importing assets (via XVFB)...")\n",
    "with open(\"godot_import.log\", \"w\") as f:\n",
    "    # We wrap the command in xvfb-run to fake a monitor\n",
    "    import_process = subprocess.Popen(",
    "        [\"xvfb-run\", \"-a\", GODOT_BIN, \"--headless\", \"--editor\", \"--quit\", \"--path\", PROJECT_PATH],",
    "        stdout=f, stderr=f
",
    "    )
",
    "    import_process.wait()
",
    "\n",
    "if import_process.returncode != 0:\n",
    "    print(\"❌ Import Failed! Logs:\")\n",
    "    !cat godot_import.log\n",
    "else:\n",
    "    print(\"✅ Assets imported.\")\n",
    "\n",
    "# --- STEP 4: TRAIN ---",
    "print(\"🧠 Attaching Neural Interface (XVFB Mode)...")\n",
    "# We use xvfb-run here too\n",
    "!xvfb-run -a python -m godot_rl.main --env_path={GODOT_BIN} --arg_args=\"--headless --path {PROJECT_PATH}\""
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

with open("C:/Users/logan/Documents/Megaman_Clean_Repo/Colab_Launcher.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)