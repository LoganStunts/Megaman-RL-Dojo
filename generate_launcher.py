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
    "# @markdown Install Linux dependencies and Godot Headless.\n",
    "\n",
    "!apt-get install -y libxcursor1 libxinerama1 libxrandr2 libxi6 libgl1-mesa-dev\n",
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
    "print(f\"✅ Switched to {TARGET_BRANCH} (Latest Version).\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# @title 4. Ignite Training\n",
    "import subprocess\n",
    "import time\n",
    "\n",
    "# 1. Clean up Zombies\n",
    "subprocess.run([\"pkill\", \"-f\", \"Godot\"])\n",
    "time.sleep(2)\n",
    "\n",
    "# 2. Import Assets (Headless)\n",
    "print(\"📦 Importing assets...\")\n",
    "with open(\"godot_import.log\", \"w\") as f:\n",
    "    # We use the FULL PATH to the binary\n",
    "    import_process = subprocess.Popen(\n",
    "        [\"./Godot_v4.5.1-stable_linux.x86_64\", \"--headless\", \"--editor\", \"--quit\"],\n",
    "        stdout=f, stderr=f\n",
    "    )\n",
    "    import_process.wait()\n",
    "\n",
    "# Check if import succeeded\n",
    "if import_process.returncode != 0:\n",
    "    print(\"❌ Import Failed! Checking logs...\")\n",
    "    !cat godot_import.log\n",
    "else:\n",
    "    print(\"✅ Assets imported.\")\n",
    "\n",
    "# 3. Launch Python Trainer\n",
    "print(\"🧠 Attaching Neural Interface...\")\n",
    "# We use the FULL PATH to the binary\n",
    "!gdrl --env_path=$(pwd)/Godot_v4.5.1-stable_linux.x86_64"
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