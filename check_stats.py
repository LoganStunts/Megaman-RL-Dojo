import os
import glob
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

def get_latest_stats():
    # Find the newest PPO_* folder
    log_dirs = glob.glob(os.path.join(r"C:\Users\logan\Documents\Megaman_Clean_Repo\logs", "PPO_*"))
    if not log_dirs:
        print("No PPO log folders found.")
        return None
    
    latest_dir = max(log_dirs, key=os.path.getmtime)
    event_files = glob.glob(os.path.join(latest_dir, "events.out.tfevents.*"))
    
    if not event_files:
        print(f"No event files in {latest_dir}")
        return None
        
    ea = EventAccumulator(event_files[0])
    ea.Reload()
    
    metrics = {}
    for tag in ea.Tags()['scalars']:
        metrics[tag] = ea.Scalars(tag)[-1].value
    return metrics, latest_dir

stats_data = get_latest_stats()
if stats_data:
    stats, path = stats_data
    print(f"--- Latest Stats from {os.path.basename(path)} ---")
    for k, v in stats.items():
        print(f"{k}: {v}")