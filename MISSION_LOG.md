# MISSION LOG: OPERATION "CLOUD DOJO"

**Start Date:** Dec 29, 2025
**Objective:** Establish a robust, version-controlled training pipeline between Local Godot and Google Colab using GitHub as the relay.
**Status:** 🟡 **CALIBRATING** (Infrastructure Success, Logic Failure)

---

## 1. INCIDENT REPORT: "THE SILENT KILLER" (Dec 29, 14:00)
**Symptoms:**
*   `explained_variance` flatlined at 0.
*   `value_loss` infinitesimally small (2.6e-05).
*   `approx_kl` exploding (0.6+).

**Diagnosis:**
The agent suffered from **Signal Vanishing**. The rewards from Godot were likely too small (e.g., 0.001), causing the brain to treat them as zero. Without normalization, the PPO algorithm couldn't distinguish good actions from bad ones, leading to "thrashing" (random flailing).

**Corrective Action:**
We are abandoning the default `gdrl` CLI tool. We will inject a custom Python training script (`train_optimized.py`) that:
1.  Wraps the environment in `VecNormalize` (Auto-scales rewards/observations).
2.  Lowers `learning_rate` to `1e-4`.
3.  Tightens `clip_range` to `0.1` to stop thrashing.
4.  Implements auto-save checkpoints to Drive.

## 2. MANIFEST updates
*   **New File:** `train_optimized.py` (The Custom Trainer).
*   **Launcher Update:** `Colab_Launcher.ipynb` will now execute `python train_optimized.py` instead of `gdrl`.

**Status:** 🟢 **ACTIVE** (Scale Fixed, Rig Calibrated)



---



## 1. INCIDENT REPORT: "THE GIANT'S RETURN" - RESOLVED

**Fix Action:**

*   **Root Scale Rebake:** Modified `Tinpet_Male_New.glb.import` to use `root_scale = 0.02`.

*   **Scene Reset:** Set all scene-level transforms back to `1.0`.

*   **Rig Verification:** Confirmed bone alignment in the soles of the feet.



## 2. METRICS

*   **Speed:** ~900 FPS (Local i9).

*   **Parallelism:** 32 Instances.

*   **Environment:** Godot 4.5.1 Headless.



---

*Log updated. Resuming 2M step grind.*


