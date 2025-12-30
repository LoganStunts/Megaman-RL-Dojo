# 🎮 MEGAMAN DOJO: MISSION CONTROL

This is your master dashboard for local training. Use the commands below to operate the Dojo.

---

## 🛠️ 1. SETUP (First time each session)
Open PowerShell in this folder and run:
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 🏋️ 2. THE TRAINING ENGINE (`train_local.py`)
*   **Purpose:** Trains the brain using your **RTX 5070 GPU** and **16 parallel Godot instances**.
*   **Action:**
    ```powershell
    python train_local.py
    ```
*   **Tip:** Press `Ctrl + C` at any time to save and stop.

---

## 🎬 3. THE PEEP HOLE (`preview_brain.py`)
*   **Purpose:** Opens a **visible** Godot window to watch Megaman's current progress.
*   **Action:**
    ```powershell
    python preview_brain.py
    ```
*   **Note:** This automatically loads the latest checkpoint. You can run this **WHILE the trainer is running** to check on him!

---

## 📊 4. THE DASHBOARD (TensorBoard)
*   **Purpose:** View real-time graphs of Reward, Loss, and Speed in your browser.
*   **Action:**
    ```powershell
    tensorboard --logdir ./logs
    ```
*   **URL:** Open [http://localhost:6006](http://localhost:6006) in Chrome/Edge.

---

## 🌳 5. REPO MANAGEMENT
*   **Payload Branch:** `payload/main` (Project Assets & Local Scripts)
*   **Loader Branch:** `main` (Colab Notebook only)

### To Sync with GitHub:
```powershell
git add .
git commit -m "Update Dojo progress"
git push origin payload/main
```

---

## ⚠️ PROTOCOLS
1. **Always use the venv:** If you see "ModuleNotFoundError", you forgot to run the Activate script.
2. **Thermal Safety:** Your i9-14900HX is powerful but will get hot. Ensure your laptop is on a hard surface with good airflow during training.
3. **One at a time:** Close the Training engine before running the Preview script to avoid GPU memory conflicts.
