import os
import time
import subprocess

def get_stats():
    # Use a single PowerShell command to get everything at once
    try:
        cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize; (Get-CimInstance Win32_Processor).LoadPercentage"'
        output = subprocess.check_output(cmd, shell=True).decode()
        # Parse output
        lines = [l.strip() for l in output.split('\n') if l.strip()]
        # Typically: Header, Data line, CPU value
        # We search specifically for digits
        nums = []
        for line in lines:
            for part in line.split():
                if part.isdigit():
                    nums.append(int(part))
        
        if len(nums) >= 3:
            free = nums[0] / 1024 # MB
            total = nums[1] / 1024 # MB
            used = total - free
            ram_p = (used / total) * 100
            cpu_p = nums[2]
            return cpu_p, used, total, ram_p
    except:
        pass
    return 0, 0, 0, 0

def count_godot():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Godot_v4.5.1-stable_win64_console.exe"', shell=True).decode()
        return output.count("Godot_v4.5.1")
    except:
        return 0

def main():
    print("🖥️  MEGAMAN DOJO: HARDWARE SENTINEL (V2)")
    print("---------------------------------------")
    try:
        while True:
            cpu, used, total, ram_p = get_stats()
            instances = count_godot()
            
            ram_status = "🟢 SAFE" if ram_p < 85 else "🟡 CAUTION" if ram_p < 95 else "🔴 CRITICAL"
            
            status = f"\r[CPU: {cpu}%] [RAM: {ram_p:.1f}% ({used/1024:.1f}GB/{total/1024:.1f}GB)] [GODOT: {instances}] [{ram_status}]"
            print(status, end="", flush=True)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n Standing down.")

if __name__ == "__main__":
    main()