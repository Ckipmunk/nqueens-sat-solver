import os
import sys
import time
import json
import csv
import statistics

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "src"))

from cp_solver import NQueensCPSolver
from ilp_solver import NQueensILPSolver
from sat_solver import NQueensSATSolver
from pysat.solvers import Solver
import psutil

data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)
csv_out = os.path.join(data_dir, "master_multisolver_runs.csv")

def main():
    print("=" * 80)
    print("BẮT ĐẦU CHẠY THỰC NGHIỆM ĐA BỘ GIẢI (GUROBI, SCIP, CP-SAT, GLUCOSE) 3 LẦN THỰC TẾ")
    print("=" * 80)

    records = []

    # 1. Gurobi 13.0 (1 thread) for N in [8, 16, 32]
    print("\n--- GUROBI 13.0 (1 thread) ---")
    for n in [8, 16, 32]:
        solver = NQueensILPSolver(n)
        for rep in [1, 2, 3]:
            t0 = time.perf_counter()
            _, stats = solver.solve_gurobi(time_limit=300.0, num_threads=1)
            t_solv = stats["solving_time"]
            print(f"  Gurobi N={n} Run {rep}: {t_solv:.4f}s")
            records.append({
                "solver": "Gurobi 13.0",
                "n": n,
                "config": "ILP (1 thread)",
                "run_id": rep,
                "time_s": f"{t_solv:.4f}",
                "status": "Optimal"
            })

    # 2. SCIP 9.0 (1 thread) for N in [8, 16, 32]
    print("\n--- SCIP 9.0 (1 thread) ---")
    for n in [8, 16, 32]:
        solver = NQueensILPSolver(n)
        for rep in [1, 2, 3]:
            t0 = time.perf_counter()
            _, stats = solver.solve_scip(time_limit=300.0)
            t_solv = stats["solving_time"]
            print(f"  SCIP N={n} Run {rep}: {t_solv:.4f}s")
            records.append({
                "solver": "ILP SCIP 9.0",
                "n": n,
                "config": "MIP (1 thread)",
                "run_id": rep,
                "time_s": f"{t_solv:.4f}",
                "status": "Optimal"
            })

    # 3. CP-SAT (OR-Tools, 1 worker) for N in [8, 16, 32, 64, 128]
    print("\n--- CP-SAT (1 worker) ---")
    for n in [8, 16, 32, 64, 128]:
        solver = NQueensCPSolver(n)
        for rep in [1, 2, 3]:
            _, stats = solver.solve(time_limit=300.0, num_workers=1)
            t_solv = stats["solving_time"]
            print(f"  CP-SAT N={n} Run {rep}: {t_solv:.4f}s")
            records.append({
                "solver": "CP-SAT (OR-Tools)",
                "n": n,
                "config": "AllDifferent (1 worker)",
                "run_id": rep,
                "time_s": f"{t_solv:.4f}",
                "status": "Feasible"
            })

    # 4. Glucose 4.2 (Product AMO) for N in [8, 16, 32, 64, 128]
    print("\n--- GLUCOSE 4.2 (Product AMO) ---")
    for n in [8, 16, 32, 64, 128]:
        sat_model = NQueensSATSolver(n, amo_method="product")
        for rep in [1, 2, 3]:
            slv = Solver(name='glucose42', bootstrap_with=sat_model.clauses)
            t0 = time.perf_counter()
            is_sat = slv.solve()
            t_solv = time.perf_counter() - t0
            slv.delete()
            print(f"  Glucose N={n} Run {rep}: {t_solv:.4f}s")
            records.append({
                "solver": "Glucose 4.2",
                "n": n,
                "config": "Product AMO",
                "run_id": rep,
                "time_s": f"{t_solv:.4f}",
                "status": "SAT"
            })

    # 5. Measure Sequential N=500 encoding time & peak RAM
    print("\n--- Sequential N=500 Encoding & RAM measurement ---")
    p = psutil.Process(os.getpid())
    t0 = time.perf_counter()
    seq500 = NQueensSATSolver(500, amo_method="sequential")
    enc500 = time.perf_counter() - t0
    ram500 = p.memory_info().peak_wset / (1024 * 1024)
    print(f"  Sequential N=500: enc={enc500:.4f}s, RAM={ram500:.1f}MB")
    with open(os.path.join(data_dir, "seq500_measured.json"), "w", encoding="utf-8") as f:
        json.dump({"encoding_time_s": enc500, "peak_ram_mb": ram500}, f)

    # Save to CSV
    fieldnames = ["solver", "n", "config", "run_id", "time_s", "status"]
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\nĐã lưu dữ liệu đa bộ giải thực tế tại: {csv_out}")

if __name__ == "__main__":
    main()
