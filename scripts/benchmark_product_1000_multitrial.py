import subprocess
import sys
import json
import os
import psutil
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
python_exe = sys.executable
worker_script = os.path.join(base_dir, "scripts", "isolated_run_worker.py")
output_file = os.path.join(data_dir, "product_1000_multitrial.json")

def run_multitrial(trials=5, timeout=300):
    results = []
    print(f"Starting {trials} independent trials of Product N=1000 (Time Limit: {timeout}s)...")
    
    for t in range(1, trials + 1):
        mem_before = psutil.virtual_memory().available / (1024 * 1024)
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
        start_t = time.time()
        print(f"\n[Trial {t}/{trials}] Avail RAM: {mem_before:.1f} MB, CPU Freq: {cpu_freq:.1f} MHz")
        
        try:
            cmd = [python_exe, worker_script, "1000", "product", str(t), str(timeout)]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 20)
            wall_time = time.time() - start_t
            
            try:
                data = json.loads(proc.stdout.strip())
            except Exception:
                data = {"status": "TIMEOUT" if wall_time >= timeout else "ERROR", "solving_time": min(timeout, wall_time), "raw_stdout": proc.stdout, "raw_stderr": proc.stderr}
            
            data["trial"] = t
            data["avail_ram_before_mb"] = mem_before
            data["cpu_freq_mhz"] = cpu_freq
            data["wall_time_s"] = wall_time
            results.append(data)
            print(f"Result Trial {t}: Status={data.get('status')}, SolvingTime={data.get('solving_time'):.2f}s, PeakRAM={data.get('peak_ram_mb', 0):.1f}MB")
        except subprocess.TimeoutExpired:
            wall_time = time.time() - start_t
            data = {
                "trial": t,
                "status": "TIMEOUT",
                "solving_time": timeout,
                "wall_time_s": wall_time,
                "avail_ram_before_mb": mem_before,
                "cpu_freq_mhz": cpu_freq
            }
            results.append(data)
            print(f"Result Trial {t}: TIMEOUT ({timeout}s)")
        except Exception as e:
            print(f"Trial {t} error: {e}")
        
        # Save intermediate
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
            
    # Summary
    success = [r for r in results if r.get("status") == "SAT"]
    print(f"\nCompleted {trials} trials: {len(success)}/{trials} SAT ({len(success)/trials*100:.1f}% success rate).")
    if success:
        times = [r["solving_time"] for r in success]
        print(f"Successful times: min={min(times):.2f}s, max={max(times):.2f}s, avg={sum(times)/len(times):.2f}s")

if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    run_multitrial(trials=trials, timeout=300)
