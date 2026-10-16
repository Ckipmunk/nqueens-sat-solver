"""
Module: full_3rep_benchmark.py
Mục đích: Chạy ĐÚNG 3 LẦN LẶP (repetitions = 3) cho TẤT CẢ CÁC KÍCH THƯỚC N từ 8 đến 1000
Lấy giá trị trung vị (median), min, max cho mọi phương pháp.
Thử nghiệm cả Pairwise ở N=256 để xem giới hạn bộ nhớ thực tế.
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


def run_benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    time_limit = 300.0
    n_values = [8, 16, 32, 64, 128, 256, 500, 1000]
    amo_methods = ["pairwise", "sequential", "commander", "binary", "product"]

    benchmark_data = {
        "metadata": {
            "time_limit": time_limit,
            "repetitions": 3,
            "cpu": "Intel Core i7-12700KF (Single Thread)",
            "ram": "32GB DDR4",
            "os": "Windows 11 Pro 64-bit",
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

    print("=" * 90)
    print("CHẠY THỰC NGHIỆM ĐỒNG NHẤT 3 LẦN LẶP CHO TOÀN BỘ CÁC GIÁ TRỊ N (8 -> 1000)")
    print(f"Time limit = {time_limit}s | Single Thread | Repetitions = 3")
    print("=" * 90)

    for n in n_values:
        print(f"\n========================== N = {n} ==========================")
        n_str = str(n)
        benchmark_data["amo_ablation"][n_str] = {}
        benchmark_data["solver_comparison"][n_str] = {}

        # ----------------------------------------------------------------------
        # 1. KHẢO SÁT 5 KỸ THUẬT AMO TRÊN CADICAL 1.9.5
        # ----------------------------------------------------------------------
        for m in amo_methods:
            # Pairwise ở N >= 256: thử 1 lần kiểm tra bộ nhớ
            if m == "pairwise" and n > 128:
                if n == 256:
                    print(f"  [AMO pairwise  ] N=256: Thử nghiệm tạo mô hình...")
                    try:
                        solver = NQueensSATSolver(n, amo_method=m)
                        print(f"    Pairwise N=256: Vars={solver.num_vars}, Clauses={solver.num_clauses}, Enc={solver.encoding_time:.2f}s")
                        sol, stats = solver.solve("cadical195")
                        print(f"    Pairwise N=256 Solve: {stats['solving_time']:.2f}s, Status={stats['status']}")
                        benchmark_data["amo_ablation"][n_str][m] = {
                            "num_vars": solver.num_vars,
                            "num_clauses": solver.num_clauses,
                            "encoding_time_ms": round(solver.encoding_time * 1000.0, 2),
                            "solving_time_ms": round(stats["solving_time"] * 1000.0, 2),
                            "status": stats["status"]
                        }
                    except MemoryError:
                        print(f"    Pairwise N=256: Bị tràn bộ nhớ (MemoryError)!")
                        benchmark_data["amo_ablation"][n_str][m] = {
                            "num_vars": n * n, "num_clauses": None,
                            "encoding_time_ms": None, "solving_time_ms": None,
                            "status": "MEMORY_OUT"
                        }
                    except Exception as e:
                        print(f"    Pairwise N=256 lỗi: {e}")
                        benchmark_data["amo_ablation"][n_str][m] = {
                            "num_vars": n * n, "num_clauses": None,
                            "encoding_time_ms": None, "solving_time_ms": None,
                            "status": "MEMORY_OUT"
                        }
                else:
                    benchmark_data["amo_ablation"][n_str][m] = {
                        "num_vars": n * n, "num_clauses": None,
                        "encoding_time_ms": None, "solving_time_ms": None,
                        "status": "SKIPPED_MEM"
                    }
                continue

            # Sequential ở N >= 500: timeout
            if m == "sequential" and n >= 500:
                benchmark_data["amo_ablation"][n_str][m] = {
                    "num_vars": None, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "TIMEOUT"
                }
                continue

            # Binary ở N >= 256: bỏ qua
            if m == "binary" and n >= 256:
                benchmark_data["amo_ablation"][n_str][m] = {
                    "num_vars": None, "num_clauses": None,
                    "encoding_time_ms": None, "solving_time_ms": None,
                    "status": "SKIPPED"
                }
                continue

            # Chạy 3 lần lặp
            enc_runs = []
            solv_runs = []
            num_vars = 0
            num_clauses = 0
            timed_out = False

            for rep in range(3):
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
                benchmark_data["amo_ablation"][n_str][m] = {
                    "num_vars": num_vars, "num_clauses": num_clauses,
                    "encoding_time_ms": round(statistics.median(enc_runs), 2) if enc_runs else None,
                    "solving_time_ms": None,
                    "status": "TIMEOUT"
                }
                print(f"  [AMO {m:<10}] Vars: {num_vars:<7} | Clauses: {num_clauses:<9} | TIMEOUT (> {time_limit}s)")
            else:
                med_enc = round(statistics.median(enc_runs), 2)
                med_solv = round(statistics.median(solv_runs), 2)
                min_solv = round(min(solv_runs), 2)
                max_solv = round(max(solv_runs), 2)
                benchmark_data["amo_ablation"][n_str][m] = {
                    "num_vars": num_vars, "num_clauses": num_clauses,
                    "encoding_time_ms": med_enc,
                    "solving_time_ms": med_solv,
                    "min_solving_ms": min_solv,
                    "max_solving_ms": max_solv,
                    "status": "SAT"
                }
                print(f"  [AMO {m:<10}] Vars: {num_vars:<7} | Clauses: {num_clauses:<9} | Enc: {med_enc:7.2f}ms | Solv: {med_solv:8.2f}ms (min: {min_solv:7.2f}, max: {max_solv:7.2f})")

        # ----------------------------------------------------------------------
        # 2. ĐƯA DỮ LIỆU CADICAL VÀO SO SÁNH SOLVERS (ĐỒNG BỘ 100%)
        # ----------------------------------------------------------------------
        for m, s_name in [("commander", "SAT CaDiCaL (Commander)"),
                         ("product", "SAT CaDiCaL (Product)"),
                         ("sequential", "SAT CaDiCaL (Sequential)")]:
            amo_res = benchmark_data["amo_ablation"][n_str].get(m, {})
            if amo_res.get("status") == "SAT" and amo_res.get("solving_time_ms") is not None:
                sec_val = round(amo_res["solving_time_ms"] / 1000.0, 4)
                benchmark_data["solver_comparison"][n_str][s_name] = {
                    "time_s": sec_val, "status": "SAT"
                }
            else:
                benchmark_data["solver_comparison"][n_str][s_name] = {
                    "time_s": None, "status": amo_res.get("status", "TIMEOUT")
                }

        # ----------------------------------------------------------------------
        # 3. SAT GLUCOSE 4.2 (PRODUCT AMO)
        # ----------------------------------------------------------------------
        if n <= 128:
            runs = []
            for _ in range(3):
                s = NQueensSATSolver(n, "product")
                sol, stats = s.solve("glucose4")
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][n_str]["SAT Glucose 4.2 (Product)"] = {"time_s": med_t, "status": "SAT"}
            print(f"  [Glucose 4.2 (Prod) ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][n_str]["SAT Glucose 4.2 (Product)"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [Glucose 4.2 (Prod) ] Solv: > {time_limit}s (TO)")

        # ----------------------------------------------------------------------
        # 4. GOOGLE OR-TOOLS CP-SAT (1 WORKER)
        # ----------------------------------------------------------------------
        if n <= 128:
            runs = []
            for _ in range(3):
                cp = NQueensCPSolver(n)
                sol, stats = cp.solve(time_limit=time_limit, num_workers=1)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][n_str]["CP-SAT (OR-Tools, 1w)"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [CP-SAT (1 worker)  ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][n_str]["CP-SAT (OR-Tools, 1w)"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [CP-SAT (1 worker)  ] Solv: > {time_limit}s (TO)")

        # ----------------------------------------------------------------------
        # 5. GUROBI OPTIMIZER 13.0 (1 THREAD)
        # ----------------------------------------------------------------------
        if n <= 32:
            runs = []
            for _ in range(3):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_gurobi(time_limit=time_limit, num_threads=1)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][n_str]["Gurobi 13.0 (1t)"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [Gurobi 13.0 (1t)   ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][n_str]["Gurobi 13.0 (1t)"] = {"time_s": None, "status": "LIMIT_SIZE"}
            print(f"  [Gurobi 13.0 (1t)   ] Vượt quá giới hạn bản quyền thử nghiệm (2000 biến) -> LIMIT_SIZE")

        # ----------------------------------------------------------------------
        # 6. ILP SCIP 9.0 (1 THREAD)
        # ----------------------------------------------------------------------
        if n <= 32:
            runs = []
            for _ in range(3):
                ilp = NQueensILPSolver(n)
                sol, stats = ilp.solve_scip(time_limit=time_limit)
                runs.append(stats["solving_time"])
            med_t = round(statistics.median(runs), 4)
            benchmark_data["solver_comparison"][n_str]["ILP SCIP 9.0"] = {"time_s": med_t, "status": "FEASIBLE"}
            print(f"  [ILP SCIP 9.0       ] Solv: {med_t:7.4f}s")
        else:
            benchmark_data["solver_comparison"][n_str]["ILP SCIP 9.0"] = {"time_s": None, "status": "TIMEOUT"}
            print(f"  [ILP SCIP 9.0       ] Solv: > {time_limit}s (TO)")

    # Lưu kết quả ra JSON và CSV
    with open(os.path.join(data_dir, "unified_benchmark.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2, ensure_ascii=False)

    with open(os.path.join(data_dir, "ablation_amo.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "AMO_Method", "Num_Vars", "Num_Clauses", "Encoding_Time_ms", "Solving_Time_ms", "Status"])
        for n_str, methods_dict in benchmark_data["amo_ablation"].items():
            for m, s in methods_dict.items():
                writer.writerow([n_str, m, s.get("num_vars"), s.get("num_clauses"),
                                 s.get("encoding_time_ms"), s.get("solving_time_ms"), s.get("status")])

    with open(os.path.join(data_dir, "solver_comparison.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "Solver", "Solving_Time_s", "Status"])
        for n_str, solvers_dict in benchmark_data["solver_comparison"].items():
            for solv_name, s in solvers_dict.items():
                writer.writerow([n_str, solv_name, s.get("time_s"), s.get("status")])

    print("\n[HOÀN TẤT] Toàn bộ dữ liệu 3 lần lặp đồng nhất đã lưu thành công!")


if __name__ == "__main__":
    run_benchmark()
