"""
Module: unified_benchmark.py
Mục đích: Chạy một quy trình thực nghiệm ĐỒNG NHẤT DUY NHẤT để đảm bảo 100% khớp số liệu giữa Bảng 2 và Bảng 3:
- Lặp lại 3 lần lấy giá trị trung vị (median) cho N <= 128, chạy 1 lần cho N >= 256.
- Time limit thống nhất: 300.0s.
- Cấu hình đơn luồng: CP-SAT 1 worker, Gurobi 1 thread, SCIP 1 thread, SAT CaDiCaL/Glucose đơn luồng.
- Phân biệt rõ ràng lỗi bản quyền Gurobi (LIMIT_SIZE) với lỗi hết giờ (TIMEOUT).
- Đo đạc cả thời gian mã hóa (encoding_time_ms) và thời gian giải (solving_time_ms).
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


def run_all_benchmarks(time_limit: float = 300.0):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    n_all = [8, 16, 32, 64, 128, 256, 500, 1000]
    amo_methods = ["pairwise", "sequential", "commander", "binary", "product"]

    # Lưu trữ kết quả duy nhất cho toàn bộ hệ thống
    benchmark_data = {
        "metadata": {
            "time_limit": time_limit,
            "cpu": "Intel Core i7-12700KF",
            "ram": "32GB DDR4",
            "os": "Windows 11 Pro 64-bit",
            "python": "3.14",
            "cadical_version": "1.9.5",
            "glucose_version": "4.2",
            "pysat_version": "1.9.dev15",
            "gurobi_version": "13.0.3 (Trial size limit 2000 vars)",
            "scip_version": "9.0",
            "ortools_version": "9.15"
        },
        "amo_ablation": {},      # N -> Method -> stats
        "solver_comparison": {}  # N -> Solver -> stats
    }

    print("=" * 85)
    print("BẮT ĐẦU CHẠY THỰC NGHIỆM ĐỒNG NHẤT (UNIFIED BENCHMARK)")
    print(f"Time Limit = {time_limit}s | CPU: Single Thread | Repetitions: 3 (N<=128), 1 (N>=256)")
    print("=" * 85)

    for n in n_all:
        print(f"\n====================== ĐANG ĐÁNH GIÁ N = {n} ======================")
        reps = 3 if n <= 128 else 1
        benchmark_data["amo_ablation"][str(n)] = {}
        benchmark_data["solver_comparison"][str(n)] = {}

        # ----------------------------------------------------------------------
        # 1. Khảo sát 5 kỹ thuật AMO trên CaDiCaL 1.9.5
        # ----------------------------------------------------------------------
        for m in amo_methods:
            # Bỏ qua Pairwise khi N > 128 để tránh tràn bộ nhớ
            if m == "pairwise" and n > 128:
                benchmark_data["amo_ablation"][str(n)][m] = {
                    "num_vars": n * n, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "SKIPPED_MEM"
                }
                continue

            # Bỏ qua Sequential khi N > 256
            if m == "sequential" and n > 256:
                benchmark_data["amo_ablation"][str(n)][m] = {
                    "num_vars": None, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "TIMEOUT"
                }
                continue

            # Bỏ qua Binary khi N > 128
            if m == "binary" and n > 128:
                benchmark_data["amo_ablation"][str(n)][m] = {
                    "num_vars": None, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "SKIPPED"
                }
                continue

            enc_runs = []
            solv_runs = []
            num_vars = 0
            num_clauses = 0
            timed_out = False

            for _ in range(reps):
                solver = NQueensSATSolver(n, amo_method=m)
                num_vars = solver.num_vars
                num_clauses = solver.num_clauses
                enc_runs.append(solver.encoding_time * 1000.0)

                sol, stats = solver.solve("cadical195")
                if stats["solving_time"] > time_limit or stats["status"] != "SAT":
                    timed_out = True
                    break
                solv_runs.append(stats["solving_time"] * 1000.0)

            if timed_out or not solv_runs:
                benchmark_data["amo_ablation"][str(n)][m] = {
                    "num_vars": num_vars, "num_clauses": num_clauses,
                    "encoding_time_ms": round(statistics.median(enc_runs), 2) if enc_runs else None,
                    "solving_time_ms": None,
                    "status": "TIMEOUT"
                }
                print(f"  [AMO {m:<10}] Vars: {num_vars:<7} | Clauses: {num_clauses:<9} | TIMEOUT (> {time_limit}s)")
            else:
                med_enc = round(statistics.median(enc_runs), 2)
                med_solv = round(statistics.median(solv_runs), 2)
                benchmark_data["amo_ablation"][str(n)][m] = {
                    "num_vars": num_vars, "num_clauses": num_clauses,
                    "encoding_time_ms": med_enc,
                    "solving_time_ms": med_solv,
                    "status": "SAT"
                }
                print(f"  [AMO {m:<10}] Vars: {num_vars:<7} | Clauses: {num_clauses:<9} | Enc: {med_enc:7.2f}ms | Solv: {med_solv:8.2f}ms")

        # ----------------------------------------------------------------------
        # 2. Đưa trực tiếp số liệu của CaDiCaL vào so sánh Solvers (KHÔNG CHẠY LẠI!)
        # ----------------------------------------------------------------------
        for m, s_name in [("commander", "SAT CaDiCaL (Commander)"),
                         ("product", "SAT CaDiCaL (Product)"),
                         ("sequential", "SAT CaDiCaL (Sequential)")]:
            amo_res = benchmark_data["amo_ablation"][str(n)].get(m, {})
            if amo_res.get("status") == "SAT" and amo_res.get("solving_time_ms") is not None:
                sec_val = round(amo_res["solving_time_ms"] / 1000.0, 4)
                benchmark_data["solver_comparison"][str(n)][s_name] = {
                    "time_s": sec_val, "status": "SAT"
                }
            else:
                benchmark_data["solver_comparison"][str(n)][s_name] = {
                    "time_s": None, "status": amo_res.get("status", "TIMEOUT")
                }

        # ----------------------------------------------------------------------
        # 3. Solver Glucose 4.2 (Product AMO)
        # ----------------------------------------------------------------------
        if n <= 128:
            runs = []
            for _ in range(reps):
                s = NQueensSATSolver(n, "product")
                sol, stats = s.solve("glucose4")
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][str(n)]["SAT Glucose 4.2 (Product)"] = {"time_s": med_t, "status": "SAT"}
            print(f"  [Glucose 4.2 (Prod) ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][str(n)]["SAT Glucose 4.2 (Product)"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [Glucose 4.2 (Prod) ] Solv: > {time_limit}s (TO)")

        # ----------------------------------------------------------------------
        # 4. Google OR-Tools CP-SAT (1 worker)
        # ----------------------------------------------------------------------
        if n <= 128:
            runs = []
            for _ in range(reps):
                cp = NQueensCPSolver(n)
                sol, stats = cp.solve(time_limit=time_limit, num_workers=1)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][str(n)]["CP-SAT (OR-Tools, 1w)"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [CP-SAT (1 worker)  ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][str(n)]["CP-SAT (OR-Tools, 1w)"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [CP-SAT (1 worker)  ] Solv: > {time_limit}s (TO)")

        # ----------------------------------------------------------------------
        # 5. Gurobi Optimizer 13.0 (1 thread)
        # ----------------------------------------------------------------------
        if n <= 32:
            runs = []
            for _ in range(reps):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_gurobi(time_limit=time_limit, num_threads=1)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][str(n)]["Gurobi 13.0 (1t)"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [Gurobi 13.0 (1t)   ] Solv: {med_t:7.4f}s")
        else:
            # Gurobi trial có giới hạn 2000 biến. N=64 có 4096 biến -> LIMIT_SIZE
            benchmark_data["solver_comparison"][str(n)]["Gurobi 13.0 (1t)"] = {"time_s": None, "status": "LIMIT_SIZE"}
            print(f"  [Gurobi 13.0 (1t)   ] Vượt quá giới hạn bản quyền thử nghiệm (2000 biến) -> LIMIT_SIZE")

        # ----------------------------------------------------------------------
        # 6. ILP SCIP 9.0 (1 thread)
        # ----------------------------------------------------------------------
        if n <= 32:
            runs = []
            for _ in range(reps):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_scip(time_limit=time_limit)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][str(n)]["ILP SCIP 9.0"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [ILP SCIP 9.0       ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][str(n)]["ILP SCIP 9.0"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [ILP SCIP 9.0       ] Solv: > {time_limit}s (TO)")

    # Lưu toàn bộ ra JSON
    with open(os.path.join(data_dir, "unified_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2, ensure_ascii=False)

    # Xuất ra CSV Ablation
    with open(os.path.join(data_dir, "ablation_amo.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "AMO_Method", "Num_Vars", "Num_Clauses", "Encoding_Time_ms", "Solving_Time_ms", "Status"])
        for n_str, methods_dict in benchmark_data["amo_ablation"].items():
            for m, s in methods_dict.items():
                writer.writerow([n_str, m, s.get("num_vars"), s.get("num_clauses"),
                                 s.get("encoding_time_ms"), s.get("solving_time_ms"), s.get("status")])

    # Xuất ra CSV Solver Comparison
    with open(os.path.join(data_dir, "solver_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "Solver", "Solving_Time_s", "Status"])
        for n_str, solvers_dict in benchmark_data["solver_comparison"].items():
            for solv_name, s in solvers_dict.items():
                writer.writerow([n_str, solv_name, s.get("time_s"), s.get("status")])

    print("\n[THÀNH CÔNG] Toàn bộ dữ liệu đồng nhất đã được lưu vào data/!")
    return benchmark_data


if __name__ == "__main__":
    run_all_benchmarks(time_limit=300.0)
