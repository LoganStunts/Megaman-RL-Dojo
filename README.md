# Megaman RL Training Facility (The Dojo)

This repository hosts the **Distributed Nervous System Training Pipeline** for the Megaman AI Agent. It is designed to allow modular skill acquisition (Dodge, Jump, Dash) via branch-based curriculum learning on Google Colab.

## 🌳 Architecture: The "Loader" vs. "Payload"

This repository is split into two distinct operational layers:

### 1. The Loader (This Branch)
*   **Role:** The Infrastructure.
*   **Contains:** 
    *   `Colab_Launcher.ipynb`: The master key to the training rig.
    *   `requirements.txt`: Python dependencies for the Linux environment.
    *   `setup_env.sh`: Automation scripts to prep the headless Godot engine.
*   **Workflow:** You clone *this* branch to Colab to set up the machine.

### 2. The Payloads (Other Branches)
*   **Role:** The Curriculum.
*   **Branches:**
    *   `payload/main`: The Generalist Gym (Walking, Balance).
    *   `payload/dodge`: High-penalty environment for projectile avoidance.
    *   `payload/dash`: Velocity-focused environment.
*   **Workflow:** The `Colab_Launcher` will ask you: *"Which Skill do you want to train?"* and will checkout the corresponding branch to run.

## 🚀 How to Train (Colab)

1.  Open `Colab_Launcher.ipynb` in Google Colab.
2.  Set your **Target Branch** (e.g., `payload/dodge`).
3.  Run All Cells.
    *   *The script will pull the specific Godot project for that skill.*
    *   *It will download the correct Godot 4.5.1 Headless binary.*
    *   *It will begin training and stream logs to Drive.*

## 🛠 Local Development

To work on a specific skill locally:

```bash
# To work on Dodging
git checkout payload/dodge
# Open project in Godot, edit Gym, Push.
```

## ⚠️ Protocol

*   **Do NOT** push the `.godot/` folder. It is ignored for a reason.
*   **Do NOT** push large binary assets (>100MB) to the `loader` branch. Keep them in the specific payload branches if necessary.
