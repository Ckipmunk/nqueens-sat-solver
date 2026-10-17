import os
import sys
import time
import json
import csv
import subprocess
import statistics

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

master_csv = os.path.join(data_dir, "master_cadical_runs.csv")
worker_script = os.path.join(base_dir, "scripts", "isolated_run_worker.py")
log_file = os.path.join(data_dir, "benchmark_execution.log")

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted, flush=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def run_single(n, method, run_id, timeout=300):
    cmd = [sys.executable, worker_script, str(n), method, str(run_id), str(timeout)]
    try:
        t0 = time.perf_counter()
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
        wall_t = time.perf_counter() - t0
        
        if proc.returncode != 0:
            log(f"  ERROR returncode {proc.returncode} for N={n} {method} Run {run_id}: {proc.stderr[:200]}")
            return None
        
        out = proc.stdout.strip()
        # Find last JSON line in stdout
        for line in reversed(out.splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                data = json.loads(line)
                return data
        log(f"  No valid JSON in stdout for N={n} {method} Run {run_id}: {out[:200]}")
        return None
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT expired (> {timeout}s) for N={n} {method} Run {run_id}")
        return {
            "n": n, "method": method, "run_id": run_id, "status": "TIMEOUT",
            "num_vars": 0, "num_clauses": 0, "cnf_hash": "-",
            "encoding_time": 0.0, "solving_time": float(timeout),
            "peak_ram_mb": 0.0, "conflicts": 0, "decisions": 0,
            "propagations": 0, "restarts": 0
        }
    except Exception as e:
        log(f"  EXCEPTION for N={n} {method} Run {run_id}: {str(e)}")
        return None

def main():
    log("=" * 80)
    log("BẮT ĐẦU CHẠY MASTER BENCHMARK TOÀN DIỆN VỚI TIẾN TRÌNH CON ĐỘC LẬP (SUBPROCESS)")
    log("=" * 80)

    # Define all planned runs
    # 1. AMO Ablation: N in [8, 16, 32, 64, 128] for 5 methods, 3 reps each
    ablation_plans = []
    for n in [8, 16, 32, 64, 128]:
        for m in ["pairwise", "sequential", "commander", "binary", "product"]:
            for rep in [1, 2, 3]:
                ablation_plans.append(("AMO Ablation", n, m, rep))

    # 2. Scale Evaluation: N in [256, 500, 1000]
    scale_plans = []
    # N=256: Commander, Product, Sequential, Pairwise (3 reps each)
    for m in ["commander", "product", "sequential", "pairwise"]:
        for rep in [1, 2, 3]:
            scale_plans.append(("Scale Evaluation", 256, m, rep))

    # N=500: Commander, Product (3 reps each)
    for m in ["commander", "product"]:
        for rep in [1, 2, 3]:
            scale_plans.append(("Scale Evaluation", 500, m, rep))

    # N=1000: Commander, Product (3 reps each)
    for m in ["commander", "product"]:
        for rep in [1, 2, 3]:
            scale_plans.append(("Scale Evaluation", 1000, m, rep))

    all_plans = ablation_plans + scale_plans
    log(f"Tổng số lần chạy theo kế hoạch: {len(all_plans)} lượt đo đạc độc lập")

    fieldnames = [
        "experiment", "n", "method", "run_id", "status",
        "num_vars", "num_clauses", "cnf_hash",
        "encoding_time_s", "solving_time_s", "peak_ram_mb",
        "conflicts", "decisions", "propagations", "restarts"
    ]

    with open(master_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    completed_count = 0
    start_total = time.perf_counter()

    for exp, n, method, rep in all_plans:
        log(f"Chạy [{completed_count+1}/{len(all_plans)}]: {exp} | N={n:<4} | {method:<10} | Run {rep}...")
        res = run_single(n, method, rep)
        if res is None:
            log(f"  -> THẤT BẠI: Không nhận được kết quả hợp lệ.")
            continue
        
        row = {
            "experiment": exp,
            "n": n,
            "method": method,
            "run_id": rep,
            "status": res["status"],
            "num_vars": res["num_vars"],
            "num_clauses": res["num_clauses"],
            "cnf_hash": res["cnf_hash"],
            "encoding_time_s": f"{res['encoding_time']:.4f}",
            "solving_time_s": f"{res['solving_time']:.4f}",
            "peak_ram_mb": f"{res['peak_ram_mb']:.2f}",
            "conflicts": res["conflicts"],
            "decisions": res["decisions"],
            "propagations": res["propagations"],
            "restarts": res["restarts"]
        }

        with open(master_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)

        completed_count += 1
        log(f"  -> OK: Solv={res['solving_time']:.4f}s, Enc={res['encoding_time']:.4f}s, RAM={res['peak_ram_mb']:.2f}MB, Conf={res['conflicts']}, Hash={res['cnf_hash']}")

    total_time = time.perf_counter() - start_total
    log("=" * 80)
    log(f"HOÀN TẤT TOÀN BỘ MASTER BENCHMARK! Tổng thời gian: {total_time:.2f}s ({total_time/60:.2f} phút)")
    log(f"Dữ liệu đã được lưu an toàn tại: {master_csv}")
    log("=" * 80)

if __name__ == "__main__":
    main()
