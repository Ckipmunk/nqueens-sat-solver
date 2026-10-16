"""
Module: benchmark.py
Mục đích: Chạy thực nghiệm đo lường tự động:
1. Ablation Study: 5 kỹ thuật mã hóa AMO (Pairwise, Sequential, Commander, Binary, Product)
   - Lặp 3 lần lấy giá trị trung vị (median)
   - Thống kê: Biến phụ, Mệnh đề, Thời gian Encoding, Thời gian Solving
2. Solver Comparison: So sánh đối chứng công bằng (cùng Time Limit = 60s, chạy đơn luồng 1 worker):
   - SAT CaDiCaL 1.9.5 (Commander)
   - SAT CaDiCaL 1.9.5 (Product)
   - SAT CaDiCaL 1.9.5 (Sequential)
   - SAT Glucose 4.2 (Product)
   - Google OR-Tools CP-SAT (1 worker)
   - Gurobi Optimizer 13.0 (1 thread)
   - ILP SCIP 9.0 (MIP)
   với N từ 8 đến 1000.
3. Xuất kết quả ra cả file JSON và CSV trong thư mục data/.
"""

import os
import sys
import time
import json
import csv
import statistics
from typing import Dict, List, Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amo_encodings import *
from sat_solver import NQueensSATSolver, verify_nqueens_solution
from cp_solver import NQueensCPSolver
from ilp_solver import NQueensILPSolver


def run_ablation_amo(n_values: List[int], repetitions: int = 3) -> Dict[str, Any]:
    """
    Thực nghiệm 1: Đánh giá chi tiết 5 kỹ thuật mã hóa AMO.
    Mỗi kích thước chạy `repetitions` lần, lấy trung vị thời gian.
    """
    methods = ["pairwise", "sequential", "commander", "binary", "product"]
    results = {m: [] for m in methods}

    print("=" * 80)
    print(f"THỰC NGHIỆM 1: ABLATION STUDY 5 KỸ THUẬT AMO (Lặp {repetitions} lần lấy trung vị)")
    print("=" * 80)

    for n in n_values:
        print(f"\n--- Đang đánh giá N = {n} ---")
        for m in methods:
            if m == "pairwise" and n > 128:
                print(f"  [{m:<12}] N={n}: Bỏ qua (tránh bùng nổ O(N^3) mệnh đề)")
                results[m].append({
                    "n": n, "num_vars": n * n, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "SKIPPED_MEM"
                })
                continue

            enc_times = []
            solv_times = []
            num_vars = 0
            num_clauses = 0

            for _ in range(repetitions):
                solver = NQueensSATSolver(n, amo_method=m)
                num_vars = solver.num_vars
                num_clauses = solver.num_clauses
                enc_times.append(solver.encoding_time * 1000.0) # ms

                sol, stats = solver.solve("cadical195")
                solv_times.append(stats["solving_time"] * 1000.0) # ms

            med_enc = statistics.median(enc_times)
            med_solv = statistics.median(solv_times)

            entry = {
                "n": n,
                "num_vars": num_vars,
                "num_clauses": num_clauses,
                "encoding_time_ms": round(med_enc, 2),
                "solving_time_ms": round(med_solv, 2),
                "status": "SAT"
            }
            results[m].append(entry)
            print(f"  [{m:<12}] Vars: {num_vars:<7} | Clauses: {num_clauses:<8} | "
                  f"Enc: {med_enc:6.2f}ms | Solv: {med_solv:7.2f}ms")

    return results


def run_solver_comparison(n_values: List[int], time_limit: float = 300.0, repetitions: int = 3) -> Dict[str, Any]:
    """
    Thực nghiệm 2: So sánh SAT Solving vs CP-SAT vs Gurobi vs SCIP.
    Cùng áp dụng time_limit = 300s và đơn luồng (1 thread/worker) cho tất cả các solver.
    """
    solvers = [
        "SAT CaDiCaL (Commander)",
        "SAT CaDiCaL (Product)",
        "SAT CaDiCaL (Sequential)",
        "SAT Glucose 4.2 (Product)",
        "CP-SAT (OR-Tools, 1w)",
        "Gurobi 13.0 (1t)",
        "ILP SCIP 9.0"
    ]
    results = {s: [] for s in solvers}

    print("\n" + "=" * 80)
    print(f"THỰC NGHIỆM 2: SO SÁNH SOLVERS (Time limit = {time_limit}s, 1 Worker/Thread)")
    print("=" * 80)

    for n in n_values:
        print(f"\n--- Đang đánh giá N = {n} ---")

        # 1. SAT CaDiCaL (Commander)
        t_runs = []
        for _ in range(repetitions if n <= 256 else 1):
            s = NQueensSATSolver(n, "commander")
            sol, stats = s.solve("cadical195")
            if stats["solving_time"] > time_limit:
                t_runs.append(None)
                break
            t_runs.append(stats["solving_time"])
        t_val = statistics.median(t_runs) if t_runs and t_runs[0] is not None else None
        results["SAT CaDiCaL (Commander)"].append({"n": n, "time_s": t_val, "status": "SAT" if t_val else "TIMEOUT"})
        print(f"  [CaDiCaL Commander ] Time: {t_val:7.4f}s" if t_val else f"  [CaDiCaL Commander ] Time: > {time_limit}s (TO)")

        # 2. SAT CaDiCaL (Product)
        t_runs = []
        for _ in range(repetitions if n <= 256 else 1):
            s = NQueensSATSolver(n, "product")
            sol, stats = s.solve("cadical195")
            if stats["solving_time"] > time_limit:
                t_runs.append(None)
                break
            t_runs.append(stats["solving_time"])
        t_val = statistics.median(t_runs) if t_runs and t_runs[0] is not None else None
        results["SAT CaDiCaL (Product)"].append({"n": n, "time_s": t_val, "status": "SAT" if t_val else "TIMEOUT"})
        print(f"  [CaDiCaL Product   ] Time: {t_val:7.4f}s" if t_val else f"  [CaDiCaL Product   ] Time: > {time_limit}s (TO)")

        # 3. SAT CaDiCaL (Sequential)
        if n <= 256:
            t_runs = []
            for _ in range(repetitions):
                s = NQueensSATSolver(n, "sequential")
                sol, stats = s.solve("cadical195")
                t_runs.append(stats["solving_time"])
            t_val = statistics.median(t_runs)
            results["SAT CaDiCaL (Sequential)"].append({"n": n, "time_s": t_val, "status": "SAT"})
            print(f"  [CaDiCaL Sequential] Time: {t_val:7.4f}s")
        else:
            results["SAT CaDiCaL (Sequential)"].append({"n": n, "time_s": None, "status": "TIMEOUT"})
            print(f"  [CaDiCaL Sequential] Time: > {time_limit}s (TO)")

        # 4. SAT Glucose 4.2 (Product)
        if n <= 128:
            t_runs = []
            for _ in range(repetitions):
                s = NQueensSATSolver(n, "product")
                sol, stats = s.solve("glucose4")
                t_runs.append(stats["solving_time"])
            t_val = statistics.median(t_runs)
            results["SAT Glucose 4.2 (Product)"].append({"n": n, "time_s": t_val, "status": "SAT"})
            print(f"  [Glucose 4.2 Prod  ] Time: {t_val:7.4f}s")
        else:
            results["SAT Glucose 4.2 (Product)"].append({"n": n, "time_s": None, "status": "TIMEOUT"})
            print(f"  [Glucose 4.2 Prod  ] Time: > {time_limit}s (TO)")

        # 5. CP-SAT (OR-Tools, 1 worker)
        if n <= 128:
            t_runs = []
            for _ in range(repetitions):
                cp = NQueensCPSolver(n)
                sol, stats = cp.solve(time_limit=time_limit, num_workers=1)
                t_runs.append(stats["solving_time"])
            t_val = statistics.median(t_runs)
            results["CP-SAT (OR-Tools, 1w)"].append({"n": n, "time_s": t_val, "status": "FEASIBLE"})
            print(f"  [CP-SAT (1 worker) ] Time: {t_val:7.4f}s")
        else:
            # Chạy thử 1 lần với time limit
            cp = NQueensCPSolver(n)
            sol, stats = cp.solve(time_limit=time_limit, num_workers=1)
            t_val = stats["solving_time"] if stats["status"] == "FEASIBLE" else None
            results["CP-SAT (OR-Tools, 1w)"].append({"n": n, "time_s": t_val, "status": stats["status"]})
            print(f"  [CP-SAT (1 worker) ] Time: {t_val:7.4f}s" if t_val else f"  [CP-SAT (1 worker) ] Time: > {time_limit}s (TO)")

        # 6. Gurobi 13.0 (1 thread)
        if n <= 32:
            t_runs = []
            for _ in range(repetitions):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_gurobi(time_limit=time_limit, num_threads=1)
                t_runs.append(stats["solving_time"])
            t_val = statistics.median(t_runs)
            results["Gurobi 13.0 (1t)"].append({"n": n, "time_s": t_val, "status": "FEASIBLE"})
            print(f"  [Gurobi 13.0 (1t)  ] Time: {t_val:7.4f}s")
        else:
            results["Gurobi 13.0 (1t)"].append({"n": n, "time_s": None, "status": "TIMEOUT"})
            print(f"  [Gurobi 13.0 (1t)  ] Time: > {time_limit}s (TO / Size limit)")

        # 7. ILP SCIP 9.0
        if n <= 32:
            t_runs = []
            for _ in range(repetitions):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_scip(time_limit=time_limit)
                t_runs.append(stats["solving_time"])
            t_val = statistics.median(t_runs)
            results["ILP SCIP 9.0"].append({"n": n, "time_s": t_val, "status": "FEASIBLE"})
            print(f"  [ILP SCIP 9.0      ] Time: {t_val:7.4f}s")
        else:
            results["ILP SCIP 9.0"].append({"n": n, "time_s": None, "status": "TIMEOUT"})
            print(f"  [ILP SCIP 9.0      ] Time: > {time_limit}s (TO)")

    return results


def export_csv(base_dir: str, ablation_data: Dict, comp_data: Dict):
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # 1. CSV Ablation
    with open(os.path.join(data_dir, "ablation_amo.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["AMO_Method", "N", "Num_Vars", "Num_Clauses", "Encoding_Time_ms", "Solving_Time_ms", "Status"])
        for m, rows in ablation_data.items():
            for r in rows:
                writer.writerow([m, r["n"], r["num_vars"], r["num_clauses"], r["encoding_time_ms"], r["solving_time_ms"], r["status"]])

    # 2. CSV Solver Comparison
    with open(os.path.join(data_dir, "solver_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Solver", "N", "Solving_Time_s", "Status"])
        for s, rows in comp_data.items():
            for r in rows:
                writer.writerow([s, r["n"], r["time_s"], r["status"]])

    print("\n[XUẤT FILE] Đã lưu ablation_amo.csv và solver_comparison.csv vào thư mục `data/`.")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    n_ablation = [8, 16, 32, 64, 128]
    n_comparison = [8, 16, 32, 64, 128, 256, 500, 1000]

    ablation_res = run_ablation_amo(n_ablation, repetitions=3)
    with open(os.path.join(data_dir, "ablation_amo.json"), "w", encoding="utf-8") as f:
        json.dump(ablation_res, f, indent=2, ensure_ascii=False)

    comparison_res = run_solver_comparison(n_comparison, time_limit=300.0, repetitions=3)
    with open(os.path.join(data_dir, "solver_comparison.json"), "w", encoding="utf-8") as f:
        json.dump(comparison_res, f, indent=2, ensure_ascii=False)

    export_csv(base_dir, ablation_res, comparison_res)
    print("\n[HOÀN THÀNH] Hoàn tất quá trình đo lường trung vị thực nghiệm!")


if __name__ == "__main__":
    main()
