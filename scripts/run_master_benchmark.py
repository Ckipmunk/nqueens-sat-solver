import os
import sys
import time
import json
import csv
import hashlib
import statistics
import psutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure src in path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from sat_solver import NQueensSATSolver
from pysat.solvers import Solver

def cnf_hash(clauses):
    sorted_clauses = [sorted(c) for c in clauses]
    sorted_clauses.sort()
    s = str(sorted_clauses).encode('utf-8')
    return hashlib.sha256(s).hexdigest()[:8]

def run_cadical_benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    n_values = [8, 16, 32, 64, 128]
    methods = ["pairwise", "sequential", "commander", "binary", "product"]

    results = []

    print("=" * 80)
    print("CHẠY MASTER BENCHMARK THỰC TẾ 3 LẦN CHO N in [8, 128] - CADICAL 1.9.5")
    print("=" * 80)

    for n in n_values:
        print(f"\n--- Kích thước bàn cờ N = {n} ---")
        for m in methods:
            run_times = []
            enc_times = []
            ram_peaks = []
            conflicts_list = []
            decisions_list = []
            props_list = []
            restarts_list = []
            c_hash = ""
            num_vars = 0
            num_clauses = 0

            for rep in range(1, 4):
                # Run instance
                p = psutil.Process(os.getpid())
                mem_before = p.memory_info().peak_wset / (1024 * 1024)

                start_enc = time.perf_counter()
                solver_model = NQueensSATSolver(n, amo_method=m)
                enc_t = time.perf_counter() - start_enc
                
                num_vars = solver_model.num_vars
                num_clauses = solver_model.num_clauses
                
                if rep == 1:
                    c_hash = cnf_hash(solver_model.clauses)

                # Solve with CaDiCaL
                slv = Solver(name='cadical195', bootstrap_with=solver_model.clauses)
                start_solv = time.perf_counter()
                is_sat = slv.solve()
                solv_t = time.perf_counter() - start_solv
                
                stats = slv.accum_stats()
                slv.delete()

                mem_after = p.memory_info().peak_wset / (1024 * 1024)
                peak_ram = max(mem_after, mem_before)

                enc_times.append(enc_t)
                run_times.append(solv_t)
                ram_peaks.append(peak_ram)
                conflicts_list.append(stats['conflicts'])
                decisions_list.append(stats['decisions'])
                props_list.append(stats['propagations'])
                restarts_list.append(stats.get('restarts', 0))

                print(f"  [{m:<11} N={n:>3} Run {rep}]: solv={solv_t:.4f}s, enc={enc_t*1000:.2f}ms, conf={stats['conflicts']}, dec={stats['decisions']}, RAM={peak_ram:.1f}MB")

            # Check determinism: conflicts and decisions must be identical across all 3 runs!
            assert len(set(conflicts_list)) == 1, f"Non-deterministic conflicts for {m} N={n}: {conflicts_list}"
            assert len(set(decisions_list)) == 1, f"Non-deterministic decisions for {m} N={n}: {decisions_list}"
            assert len(set(props_list)) == 1, f"Non-deterministic props for {m} N={n}: {props_list}"

            med_solv = statistics.median(run_times)
            std_solv = statistics.stdev(run_times)
            min_solv = min(run_times)
            max_solv = max(run_times)
            med_enc = statistics.median(enc_times)
            med_ram = statistics.median(ram_peaks)

            results.append({
                "N": n,
                "Method": m,
                "Vars": num_vars,
                "Clauses": num_clauses,
                "CNF_Hash": c_hash,
                "Run_1_s": run_times[0],
                "Run_2_s": run_times[1],
                "Run_3_s": run_times[2],
                "Min_s": min_solv,
                "Median_s": med_solv,
                "Max_s": max_solv,
                "Std_s": std_solv,
                "Enc_Time_s": med_enc,
                "Enc_Time_ms": med_enc * 1000.0,
                "Peak_RAM_MB": med_ram,
                "Conflicts": conflicts_list[0],
                "Decisions": decisions_list[0],
                "Propagations": props_list[0],
                "Restarts": restarts_list[0]
            })

    # Save to master CSV
    csv_file = os.path.join(data_dir, "master_cadical_runs.csv")
    fieldnames = list(results[0].keys())
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n[XONG] Đã lưu dữ liệu master vào {csv_file} thành công!")

if __name__ == "__main__":
    run_cadical_benchmark()
